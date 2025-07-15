import serial
import tkinter as tk
import threading

# Replace with your Arduino's COM port
serial_port = 'COM3'
baud_rate = 9600

# Open the serial connection
ser = serial.Serial(serial_port, baud_rate)

# GUI Window
window = tk.Tk()
window.title("Distance Visualizer")
canvas = tk.Canvas(window, width=400, height=400)
canvas.pack()

# Initial box
box_size = 50
box = canvas.create_rectangle(200-box_size, 200-box_size, 200+box_size, 200+box_size, fill='blue')

def update_box_size(sensor_value):
    global box
    # Map sensor_value (0 to 1023) to box size (10 to 150)
    min_val, max_val = 0, 1023
    min_size, max_size = 10, 150

    size = min_size + (max_val - sensor_value) / (max_val - min_val) * (max_size - min_size)
    size = max(min_size, min(size, max_size))

    # Update rectangle
    canvas.coords(box, 200-size, 200-size, 200+size, 200+size)

def read_serial():
    while True:
        try:
            if ser.in_waiting:
                data = ser.readline().decode('utf-8').strip()
                print(f"Sensor: {data}")
                sensor_value = int(data)
                window.after(0, update_box_size, sensor_value)
        except Exception as e:
            print("Error reading serial:", e)

# Run serial reading in a separate thread
threading.Thread(target=read_serial, daemon=True).start()

window.mainloop()
