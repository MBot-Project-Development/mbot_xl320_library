from . import config
from dynamixel_sdk import *  # Uses Dynamixel SDK library

class ServoGroup:
    def __init__(self, servo1_id, servo2_id, port_name):
        self.servo1_id = servo1_id
        self.servo2_id = servo2_id
        self.port_name = port_name
        self.portHandler = PortHandler(port_name)
        self.packetHandler = PacketHandler(config.PROTOCOL_VERSION)