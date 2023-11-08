#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import time
from . import config
from dynamixel_sdk import *  # Uses Dynamixel SDK library

# Function to handle single keypress
def getch():
    if os.name == 'nt':
        import msvcrt
        return msvcrt.getch().decode()
    else:
        import tty, termios
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        try:
            tty.setraw(fd)
            ch = sys.stdin.read(1)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        return ch
        
def initialize_handlers(port_name):
    portHandler = PortHandler(port_name)
    packetHandler = PacketHandler(config.PROTOCOL_VERSION)
    return portHandler, packetHandler

def open_port(portHandler):
    if portHandler.openPort():
        print("Succeeded to open the port")
    else:
        print("Failed to open the port")
        quit()

def close_port(portHandler):
    portHandler.closePort()

def set_baudrate(portHandler, baudrate):
    if portHandler.setBaudRate(baudrate):
        print("Succeeded to change the baudrate to %d" % baudrate)
    else:
        print("Failed to change the baudrate")
        quit()