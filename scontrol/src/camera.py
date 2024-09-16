import cv2
from PIL import Image, ImageTk
import tkinter as tk
import pyfirmata
import time
import threading


class CameraApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Camera App")

        self.board = pyfirmata.Arduino("/dev/ttyUSB0")
        self.it = pyfirmata.util.Iterator(self.board)
        self.it.start()

        pin_13 = self.board.get_pin("d:13:i")

        # Try different camera indices if needed
        self.camera = cv2.VideoCapture(0)  # Change the index if necessary
        if not self.camera.isOpened():
            print("Error: Camera could not be opened.")
            self.root.quit()

        self.canvas = tk.Canvas(root, width=640, height=480)
        self.canvas.pack()

        # Run the function to check for ping on pin 13 on a separate thread
        threading.Thread(target=self.check_ping, args=(pin_13,)).start()

        self.update_frame()

    def update_frame(self):
        ret, frame = self.camera.read()
        if ret:
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
            cv2.imwrite("snapshot.jpg", frame)
            print("Snapshot saved as 'snapshot.jpg'")
        else:
            print("Failed to grab frame")

    def send_snapshot_to_printer(self):
        # Code to send the snapshot to the printer
        print("Sending snapshot to printer...")

    def check_ping(self, pin_13):
        print("Waiting for a ping on pin 13...")

        while True:
            pin_13_value = pin_13.read()

            if pin_13_value is True:
                print("Ping received on pin 13. Launching camera app...")
                self.launch_camera()
                time.sleep(5)
            else:
                time.sleep(0.1)

    def __del__(self):
        self.camera.release()


if __name__ == "__main__":
    root = tk.Tk()
    app = CameraApp(root)
    root.mainloop()
