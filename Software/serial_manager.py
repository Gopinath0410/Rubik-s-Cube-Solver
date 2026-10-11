import serial
import serial.tools.list_ports
from tkinter import messagebox


class SerialManager:

    def __init__(self):
        self.ser = None

    # -----------------------------
    # Get Available COM Ports
    # -----------------------------
    def get_ports(self):

        ports = serial.tools.list_ports.comports()

        return [port.device for port in ports]

    # -----------------------------
    # Connect
    # -----------------------------
    def connect(self, port, baudrate=115200):

        try:
            self.ser = serial.Serial(
                port,
                baudrate,
                timeout=1
            )

            print(f"Connected to {port}")

            return True

        except Exception as e:

            messagebox.showerror(
                "Serial Error",
                str(e)
            )

            return False

    # -----------------------------
    # Send Solution
    # -----------------------------
    def send_moves(self, solution):

        if self.ser is None or not self.ser.is_open:

            messagebox.showerror(
                "Serial Error",
                "ESP32 is not connected."
            )
            return

        print("Sending Solution:")
        print(solution)

        # Send the whole solution as one line
        self.ser.write((solution + "\n").encode())

    # -----------------------------
    # Disconnect
    # -----------------------------
    def disconnect(self):

        if self.ser and self.ser.is_open:

            self.ser.close()

            print("Disconnected")