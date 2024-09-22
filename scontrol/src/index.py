import cv2
from PIL import Image, ImageTk
import tkinter as tk
import serial
import time
import threading
import os
import platform

# Import platform-specific libraries for printing
if platform.system() == "Windows":
    import win32print
    import win32api
elif platform.system() == "Linux":
    import cups


class CameraApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Camera App")

        # Set the window to fullscreen
        self.root.attributes("-fullscreen", True)

        arduino_port = '/dev/ttyUSB1'  # For Linux, change to 'COM3' or similar for Windows
        baud_rate = 9600  # Should match the baud rate set in the Arduino code

        ser = serial.Serial(arduino_port, baud_rate, timeout=1)
        time.sleep(2)  # Wait for Arduino to reset

        # Try different camera indices if needed
        self.camera = cv2.VideoCapture(0)  # Change the index if necessary
        if not self.camera.isOpened():
            print("Error: Camera could not be opened.")
            self.root.quit()

        # Get screen width and height
        self.screen_width = self.root.winfo_screenwidth()
        self.screen_height = self.root.winfo_screenheight()

        self.canvas = tk.Canvas(root, width=self.screen_width, height=self.screen_height)
        self.canvas.pack()

        # Run the function to check for ping on pin 13 on a separate thread
        threading.Thread(target=self.check_button, args=(ser,)).start()

        self.root.bind("<Escape>", lambda event: self.root.attributes("-fullscreen", False))
        self.root.bind("<F11>", lambda event: self.root.attributes("-fullscreen", True))
        
        self.update_frame()

    def update_frame(self):
        ret, frame = self.camera.read()
        if ret:
            # Resize the frame to fit the screen size
            frame = cv2.resize(frame, (self.screen_width, self.screen_height))

            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            image = Image.fromarray(frame)
            photo = ImageTk.PhotoImage(image=image)

            self.canvas.create_image(0, 0, image=photo, anchor=tk.NW)
            self.canvas.image = photo  # Keep a reference to avoid garbage collection
            self.root.after(10, self.update_frame)
        else:
            print("Failed to grab frame")
            self.root.after(10, self.update_frame)

    def take_snapshot(self):
        ret, frame = self.camera.read()
        if ret:
            snapshot_path = "snapshot.jpg"
            cv2.imwrite(snapshot_path, frame)
            print("Snapshot saved as 'snapshot.jpg'")
            self.send_snapshot_to_printer(snapshot_path)
        else:
            print("Failed to grab frame")

    def send_snapshot_to_printer(self, snapshot_path):
        if os.path.exists(snapshot_path):
            # For Windows
            if platform.system() == "Windows":
                printer_name = win32print.GetDefaultPrinter()
                print(f"Sending {snapshot_path} to printer {printer_name}...")
                win32api.ShellExecute(
                    0,
                    "print",
                    snapshot_path,
                    f'/d:"{printer_name}"',
                    ".",
                    0
                )

            # For Linux
            elif platform.system() == "Linux":
                conn = cups.Connection()
                printers = conn.getPrinters()
                printer_name = list(printers.keys())[0]
                print(f"Sending {snapshot_path} to printer {printer_name}...")
                conn.printFile(printer_name, snapshot_path, "Image Print", {})

            else:
                print("Unsupported platform for printing")
        else:
            print("Snapshot does not exist. Please take a snapshot first.")

    def check_button(self, ser):
        try:
            while True:
                if ser.in_waiting > 0:
                    line = ser.readline().decode('utf-8').rstrip()  # Read and decode the line
                    if line == "Button pressed":
                        time.sleep(4)  # Delay before taking a snapshot
                        self.take_snapshot()

        except KeyboardInterrupt:
            print("Program stopped by user.")

        finally:
            ser.close()  # Close the serial connection when done

    def __del__(self):
        self.camera.release()


if __name__ == "__main__":
    root = tk.Tk()
    app = CameraApp(root)
    root.mainloop()
