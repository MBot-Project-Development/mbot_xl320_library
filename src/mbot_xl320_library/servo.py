import os
import sys
import time
from . import config
from dynamixel_sdk import *  # Uses Dynamixel SDK library

class Servo:
    def __init__(self, servo_id, portHandler, packetHandler):
        self.servo_id = servo_id
        self.portHandler = portHandler
        self.packetHandler = packetHandler

    def change_led_color(self, color):
        self.packetHandler.write1ByteTxRx(self.portHandler, self.servo_id, config.ADDR_LED, color)

    def check_torque_status(self):
        torque_enable, _, _ = self.packetHandler.read1ByteTxRx(self.portHandler, self.servo_id, config.ADDR_TORQUE_ENABLE)
        if torque_enable == 1:
            print("Torque is enabled")
        else:
            print("Torque is disabled")

    def print_error_msg(self, dxl_comm_result, dxl_error):
        if dxl_comm_result != COMM_SUCCESS:
            print("%s" % self.packetHandler.getTxRxResult(dxl_comm_result))
        elif dxl_error != 0:
            print("%s" % self.packetHandler.getRxPacketError(dxl_error))

    def enable_torque(self):
        dxl_comm_result, dxl_error = self.packetHandler.write1ByteTxRx(self.portHandler, self.servo_id, config.ADDR_TORQUE_ENABLE, config.TORQUE_ENABLE)
        if config.DEBUG:
            self.print_error_msg(dxl_comm_result, dxl_error)
        self.check_torque_status()
        return dxl_comm_result, dxl_error 

    def disable_torque(self):
        dxl_comm_result, dxl_error = self.packetHandler.write1ByteTxRx(self.portHandler, self.servo_id, config.ADDR_TORQUE_ENABLE, config.TORQUE_DISABLE)
        if config.DEBUG:
            self.print_error_msg(dxl_comm_result, dxl_error)
        self.check_torque_status()
        return dxl_comm_result, dxl_error 
    
    def look_error_info(self):
        hardware_error_status, dxl_comm_result, dxl_error = self.packetHandler.read1ByteTxRx(self.portHandler, self.servo_id, config.ADDR_HARDWARE_ERROR_STATUS)
        print("Hardware Error Status: ", hardware_error_status)
        shutdown_error_info, dxl_comm_result, dxl_error = self.packetHandler.read1ByteTxRx(self.portHandler, self.servo_id, config.ADDR_SHUTDOWN)
        print("Shutdown Error Information: ", shutdown_error_info)

    def get_position(self):
        dxl_present_position, dxl_comm_result, dxl_error = self.packetHandler.read2ByteTxRx(self.portHandler, self.servo_id, config.ADDR_PRESENT_POSITION)
        if config.DEBUG:
            self.print_error_msg(dxl_comm_result, dxl_error)
        return dxl_present_position
    
    def set_position(self, goal_position):
        dxl_comm_result, dxl_error = self.packetHandler.write2ByteTxRx(self.portHandler, self.servo_id, config.ADDR_GOAL_POSITION, goal_position)
        if config.DEBUG:
            self.print_error_msg(dxl_comm_result, dxl_error)
        goal_position_set, dxl_comm_result, dxl_error = self.packetHandler.read2ByteTxRx(self.portHandler, self.servo_id, config.ADDR_GOAL_POSITION)
        print("Goal position set to: ", goal_position_set)

    def set_control_mode(self, mode):
        if mode not in ["wheel", "joint"]:
            print("The control mode has to be either 'wheel' or 'joint'")
            return

        mode_value = config.WHEEL_MODE if mode == "wheel" else config.JOINT_MODE

        dxl_comm_result, dxl_error = self.packetHandler.write1ByteTxRx(self.portHandler, self.servo_id, config.ADDR_CONTROL_MODE, mode_value)
        if config.DEBUG:
            self.print_error_msg(dxl_comm_result, dxl_error)

        curr_control_mode, dxl_comm_result, dxl_error = self.packetHandler.read1ByteTxRx(self.portHandler, self.servo_id, config.ADDR_CONTROL_MODE)
        if config.DEBUG:
            self.print_error_msg(dxl_comm_result, dxl_error)
        print("Control Mode set to (1 is wheel, 2 is joint): ", curr_control_mode)

    def set_joint_speed(self, speed):
        # set moving speed to Goal Position. range: 0~1,023
        speed = int(speed)
        if not 0 <= speed <= 1023:
            raise ValueError("Speed must be between 0 and 1023")
        dxl_comm_result, dxl_error = self.packetHandler.write2ByteTxRx(self.portHandler, self.servo_id, config.ADDR_GOAL_SPEED, speed)
        if config.DEBUG:
            self.print_error_msg(dxl_comm_result, dxl_error)
        rpm_speed = 0.111 * speed 
        if speed == 0:
            print(f"Set joint mode speed to maximum rpm")
        else:
            print(f"Set joint mode speed to: {speed}, {rpm_speed:.2f} in rpm")

    def set_wheel_ccw_speed(self, load):
        # set moving speed to Counter-Clockwise direction. range: 0~1,023
        # it is stopped by setting to 0
        load = int(load)
        if not 0 <= load <= 100:
            raise ValueError("Load must be between 0 and 100")

        speed = int(load*0.01*1023)
        dxl_comm_result, dxl_error = self.packetHandler.write2ByteTxRx(self.portHandler, self.servo_id, config.ADDR_GOAL_SPEED, speed)
        if config.DEBUG:
            self.print_error_msg(dxl_comm_result, dxl_error)
        print(f"Set wheel mode to rotate Counter-Clockwise with {load}% output")

    def set_wheel_cw_speed(self, load):
        # set moving speed to Clockwise direction. range: 1,024~2,047
        # it is stopped by setting to 1,024
        load= int(load)
        if not 0 <= load <= 100:
            raise ValueError("Load must be between 0 and 100")
            
        # When load is 0%, we want the minimum CW speed (1024).
        # When load is 100%, we want the maximum CW speed (2047).
        speed = int((load / 100.0) * 1023)
        speed += 1024
        dxl_comm_result, dxl_error = self.packetHandler.write2ByteTxRx(self.portHandler, self.servo_id, config.ADDR_GOAL_SPEED, speed)
        if config.DEBUG:
            self.print_error_msg(dxl_comm_result, dxl_error)

        print(f"Set wheel mode to rotate Clockwise direction with {load}% output")