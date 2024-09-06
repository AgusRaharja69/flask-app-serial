from flask import Flask, render_template, jsonify
import serial
import threading
import atexit

app = Flask(__name__)
serial_data = {"frequency": 0}
ser = None

def open_serial_port():
    global ser
    try:
        ser = serial.Serial('COM11', 115200)
        print("Serial port opened successfully.")
    except serial.SerialException as e:
        print(f"Error opening serial port: {e}")
        ser = None

def read_serial():
    global serial_data
    while True:
        if ser and ser.in_waiting > 0:
            try:
                line = ser.readline().decode('utf-8').strip()
                values = line.split(',')
                if len(values) == 4:
                    try:
                        ax, ay, az, frequency = map(float, values)
                        serial_data["frequency"] = frequency
                        print(frequency)
                    except ValueError:
                        pass
            except UnicodeDecodeError:
                pass
            except ValueError:
                pass

def close_serial_port():
    if ser:
        ser.close()
        print("Serial port closed.")

atexit.register(close_serial_port)

@app.route('/')
def index():
    return render_template('index1.html')

@app.route('/data')
def data():
    return jsonify(serial_data)

if __name__ == '__main__':
    open_serial_port()
    if ser:
        serial_thread = threading.Thread(target=read_serial)
        serial_thread.daemon = True
        serial_thread.start()

        # Run Flask without debug mode to avoid issues with serial port
        app.run(debug=False)
    else:
        print("Failed to open serial port. Flask will not start.")
