#!/usr/bin/python3
from . import config, utils
from dynamixel_sdk import *  # Uses Dynamixel SDK library
import os

class GPIOPortHandler(PortHandler):
    def __init__(self, port_name):
        super(GPIOPortHandler, self).__init__(port_name)
        self.detect_device()
        self.setup_pins()
        self.CTL_PIN
        self.gpio_file = open(f"/sys/class/gpio/gpio{self.CTL_PIN}/value", "w")

    def readPort(self, length):   
        if (sys.version_info > (3, 0)):
            return self.ser.read(length)
        else:
            return [ord(ch) for ch in self.ser.read(length)]
        
    def writePort(self, packet):
        self.gpio_file.write("0")
        status = self.ser.write(packet)
        self.gpio_file.write("1")
        return status

    def detect_device(self):
        # Check devices then assign GPIO Numbers,
        # on Jetson, pin 7 is gpio216 and pin 11 is gpio50
        # on RPi pin 7 is gpio4, pin 11 is gpio17
        with open('/proc/device-tree/model', 'r') as file:
            data = file.read()
        if "Raspberry Pi" in data:
            print("Detected Raspberry Pi")
            self.CTL_PIN = config.RPI_CTL_PIN 
        elif "NVIDIA Jetson" in data:
            print("Detected NVIDIA Jetson")
            self.CTL_PIN = config.JETSON_CTL_PIN 
        else:
            print("ERROR: Unknown hardware!")
            exit(1)

    def setup_pins(self):
        # Expose the GPIO pins
        if not os.path.exists(f"/sys/class/gpio/gpio{self.CTL_PIN}"):
            with open("/sys/class/gpio/export", "w") as f:
                f.write(str(self.CTL_PIN))
            time.sleep(0.1)        

        # Set GPIO pins to output
        with open(f"/sys/class/gpio/gpio{self.CTL_PIN}/direction", "w") as f:
            f.write("out")
        time.sleep(0.1)

