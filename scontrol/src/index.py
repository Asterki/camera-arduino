import pyfirmata
import subprocess
import time
import platform

# Define the port to which the Arduino is connected
# This will vary based on your operating system
# On Windows it could be something like 'COM3', on Linux/Mac it could be '/dev/ttyUSB0'
board = pyfirmata.Arduino('/dev/ttyUSB0')

# Start an iterator thread to prevent overflow in the serial buffer
it = pyfirmata.util.Iterator(board)
it.start()

# Setup pin 13 as an input
pin_13 = board.get_pin('d:13:i')

def launch_camera():
    os_name = platform.system()
    
    if os_name == 'Windows':
        # Launch default camera app for Windows
        subprocess.run('start microsoft.windows.camera:', shell=True)
        
    elif os_name == 'Linux':
        # Launch default camera app for Linux (cheese is used as an example)
        subprocess.run(['cheese'])
        
    elif os_name == 'Darwin':  # Darwin refers to macOS
        # Launch Photo Booth on macOS
        subprocess.run(['open', '-a', 'Photo Booth'])
        
    else:
        print(f"Unsupported OS: {os_name}")

print("Waiting for a ping on pin 13...")

while True:
    # Read the input from pin 13
    pin_13_value = pin_13.read()
    
    if pin_13_value is True:
        print("Ping received on pin 13. Launching camera app...")
        launch_camera()
        time.sleep(5)  # Delay to prevent multiple triggers in quick succession
    else:
        # No ping detected
        time.sleep(0.1)  # Sleep to avoid busy-waiting
