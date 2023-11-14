import os
import sys
import time
from . import config
from . import gpio_port_handler
from dynamixel_sdk import *  # Uses Dynamixel SDK library


class Servo:
    """@brief Class to control a Dynamixel Servo."""

    def __init__(self, servo_id, portHandler, packetHandler):
        self.servo_id = servo_id
        self.portHandler = portHandler
        self.packetHandler = packetHandler

    def change_led_color(self, color):
        """
        @brief Changes the LED color of the servo.

        @param color The color is defined in config.py

        For example: servo.change_led_color(LED_RED)
        """
        self.packetHandler.write1ByteTxRx(self.portHandler, self.servo_id, config.ADDR_LED, color)

    def check_torque_status(self):
        """
        @brief Checks the torque status by reading from torque address
        """
        torque_enable, _, _ = self.packetHandler.read1ByteTxRx(
            self.portHandler, self.servo_id, config.ADDR_TORQUE_ENABLE
        )
        if torque_enable == 1:
            print("[ID:%d] Torque is enabled!" % self.servo_id)
        else:
            print("[ID:%d] Torque is disabled!" % self.servo_id)

    def print_error_msg(self, dxl_comm_result, dxl_error):
        if dxl_comm_result != COMM_SUCCESS:
            print("%s" % self.packetHandler.getTxRxResult(dxl_comm_result))
        elif dxl_error != 0:
            print("%s" % self.packetHandler.getRxPacketError(dxl_error))

    def enable_torque(self):
        """
        @brief Enable torque for the servo.

        Note: Torque must be enabled before moving the servo.
        """
        dxl_comm_result, dxl_error = self.packetHandler.write1ByteTxRx(
            self.portHandler, self.servo_id, config.ADDR_TORQUE_ENABLE, config.TORQUE_ENABLE
        )
        if config.DEBUG:
            self.print_error_msg(dxl_comm_result, dxl_error)
        self.check_torque_status()

    def disable_torque(self):
        """
        @brief Disable torque for the servo.

        Note: Torque must be disabled before changing control mode
        """
        dxl_comm_result, dxl_error = self.packetHandler.write1ByteTxRx(
            self.portHandler, self.servo_id, config.ADDR_TORQUE_ENABLE, config.TORQUE_DISABLE
        )
        if config.DEBUG:
            self.print_error_msg(dxl_comm_result, dxl_error)
        self.check_torque_status()

    def look_error_info(self):
        hardware_error_status, dxl_comm_result, dxl_error = self.packetHandler.read1ByteTxRx(
            self.portHandler, self.servo_id, config.ADDR_HARDWARE_ERROR_STATUS
        )
        print("Hardware Error Status: ", hardware_error_status)
        shutdown_error_info, dxl_comm_result, dxl_error = self.packetHandler.read1ByteTxRx(
            self.portHandler, self.servo_id, config.ADDR_SHUTDOWN
        )
        print("Shutdown Error Information: ", shutdown_error_info)

    def get_position(self):
        """
        @brief Get servo's current position by reading from address

        @return servo's current position in range [0, 1023]
        """
        dxl_present_position, dxl_comm_result, dxl_error = self.packetHandler.read2ByteTxRx(
            self.portHandler, self.servo_id, config.ADDR_PRESENT_POSITION
        )
        if config.DEBUG:
            self.print_error_msg(dxl_comm_result, dxl_error)
        return dxl_present_position

    def set_position(self, goal_position):
        """
        @brief Sets the goal position for servo in joint mode

        @param goal_position in range [0, 1023] defined in config.py
                             as [DXL_MINIMUM_POSITION_VALUE, DXL_MAXIMUM_POSITION_VALUE]

        @return None.
        """
        dxl_comm_result, dxl_error = self.packetHandler.write2ByteTxRx(
            self.portHandler, self.servo_id, config.ADDR_GOAL_POSITION, goal_position
        )
        if config.DEBUG:
            self.print_error_msg(dxl_comm_result, dxl_error)

        goal_position_set, dxl_comm_result, dxl_error = self.packetHandler.read2ByteTxRx(
            self.portHandler, self.servo_id, config.ADDR_GOAL_POSITION
        )
        print(f"[ID:{self.servo_id}] Goal position set to: {goal_position_set}")

    def set_control_mode(self, mode):
        """
        @brief Sets the control mode of the servo to either wheel or joint.

        This method configures the servo's operating mode to either 'wheel' for continuous rotation or 'joint' for standard angular movement.
        After setting the mode, it reads back the mode to verify the change.

        @param mode A string that must be either "wheel" or "joint" to set the corresponding mode.
        @throw ValueError if the provided mode string is not "wheel" or "joint".

        @return None. However, it prints the current control mode after setting it.
        """
        if mode not in ["wheel", "joint"]:
            print("The control mode has to be either 'wheel' or 'joint'")
            return

        mode_value = config.WHEEL_MODE if mode == "wheel" else config.JOINT_MODE

        dxl_comm_result, dxl_error = self.packetHandler.write1ByteTxRx(
            self.portHandler, self.servo_id, config.ADDR_CONTROL_MODE, mode_value)

        if config.DEBUG:
            self.print_error_msg(dxl_comm_result, dxl_error)

        curr_control_mode, dxl_comm_result, dxl_error = self.packetHandler.read1ByteTxRx(
            self.portHandler, self.servo_id, config.ADDR_CONTROL_MODE)
            
        if config.DEBUG:
            self.print_error_msg(dxl_comm_result, dxl_error)

        control_mode_name = "wheel" if curr_control_mode == 1 else "joint"
        print(f"[ID:{self.servo_id}] control mode set to {control_mode_name}")

    def set_joint_speed(self, speed):
        """
        @brief Sets the joint speed of the servo.

        The range [0, 1023] maps to the speeds from minimum to maximum.
        Note that 0 represents the maximumun speed not stop.
        The servo in joint mode will only stop when reach goal postion.

        @param speed An integer value in range [0, 1023]
        @throw ValueError if the speed is not within the valid range.

        @return None.
        """
        speed = int(speed)
        if not 0 <= speed <= 1023:
            raise ValueError("Speed must be between 0 and 1023")
        dxl_comm_result, dxl_error = self.packetHandler.write2ByteTxRx(
            self.portHandler, self.servo_id, config.ADDR_GOAL_SPEED, speed
        )
        if config.DEBUG:
            self.print_error_msg(dxl_comm_result, dxl_error)
        rpm_speed = 0.111 * speed
        if speed == 0:
            print(f"[ID:{self.servo_id}] Set speed to maximum rpm")
        else:
            print(f"[ID:{self.servo_id}] Set speed to: {speed}, {rpm_speed:.2f} in rpm")

    def set_wheel_ccw_speed(self, load):
        """
        @brief Sets the moving speed of the servo in the counter-clockwise direction.

        @param load The desired speed as a percentage (0-100).
        @throw ValueError If the load parameter is outside the range of 0 to 100.

        @return None

        This function will convert the percentage to the corresponding speed value that the servo understands.
        The actual value range is range: 0~1023 and it is stopped by setting to 0.
        """
        load = int(load)
        if not 0 <= load <= 100:
            raise ValueError("Load must be between 0 and 100")

        speed = int(load * 0.01 * 1023)
        dxl_comm_result, dxl_error = self.packetHandler.write2ByteTxRx(
            self.portHandler, self.servo_id, config.ADDR_GOAL_SPEED, speed
        )
        if config.DEBUG:
            self.print_error_msg(dxl_comm_result, dxl_error)
        print(f"[ID:{self.servo_id}] Set wheel mode to rotate Counter-Clockwise with {load}% output")

    def set_wheel_cw_speed(self, load):
        """
        @brief Sets the moving speed of the servo in the clockwise direction.

        @param load The desired speed as a percentage (0-100).
        @throw ValueError If the load parameter is outside the range of 0 to 100.

        @return None

        This function will convert the percentage to the corresponding speed value that the servo understands.
        The actual value range is range: 1024~2047 and it is stopped by setting to 1024.
        """
        load = int(load)
        if not 0 <= load <= 100:
            raise ValueError("Load must be between 0 and 100")
        speed = int((load / 100.0) * 1023)
        speed += 1024
        dxl_comm_result, dxl_error = self.packetHandler.write2ByteTxRx(
            self.portHandler, self.servo_id, config.ADDR_GOAL_SPEED, speed
        )
        if config.DEBUG:
            self.print_error_msg(dxl_comm_result, dxl_error)

        print(f"[ID:{self.servo_id}] Set wheel mode to rotate Clockwise with {load}% output")
