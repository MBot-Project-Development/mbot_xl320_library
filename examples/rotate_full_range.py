"""
Servo movement example in "joint" mode

This script demonstrates the use of the mbot_xl320_library to control servo motors.
The servo is set to operate in "joint" mode, where it alternates between two limit positions.

Use: sudo python3 rotate_full_range.py
"""

from mbot_xl320_library import *

# user defined value
DXL_MOVING_STATUS_THRESHOLD = 20  # Dynamixel moving status threshold


def main():
    portHandler, packetHandler = initialize_handlers("/dev/ttyTHS1")

    # defines the servo's ID
    servo1_ID = 1
    servo2_ID = 2

    open_port(portHandler)
    set_baudrate(portHandler, 1000000)

    # Initialize a Servo instance
    servo1 = Servo(servo1_ID, portHandler, packetHandler)
    servo1.change_led_color(LED_BLUE)
    servo1.disable_torque()
    servo1.set_control_mode("joint")  # torque must be off when you change mode
    servo1.enable_torque()

    # Initialize second Servo instance
    servo2 = Servo(servo2_ID, portHandler, packetHandler)
    servo2.change_led_color(LED_YELLOW)
    servo2.disable_torque()
    servo2.set_control_mode("joint")  # torque must be off when you change mode
    servo2.enable_torque()

    index = 0
    goal_positions = [
        DXL_MINIMUM_POSITION_VALUE,
        DXL_MAXIMUM_POSITION_VALUE,
    ]  # these are the actual limits of the servo

    servo1.set_joint_speed(300)  # range(0,1023)
    servo2.set_joint_speed(300)  # range(0,1023)

    while True:
        print("Press any key to continue! (or press ESC to quit!)")
        if getch() == chr(0x1B):
            break

        servo1.set_position(goal_positions[index])
        servo2.set_position(goal_positions[index])

        while True:
            servo1_current_position = servo1.get_position()
            servo2_current_position = servo2.get_position()

            if goal_positions[index] is None or servo1_current_position is None or servo2_current_position is None:
                continue
            
            print("---")
            print("[ID:%d] GoalPos:%d  PresPos:%d"  % (servo1_ID, goal_positions[index], servo1_current_position))
            print("[ID:%d] GoalPos:%d  PresPos:%d"  % (servo2_ID, goal_positions[index], servo2_current_position))

            if (not abs(goal_positions[index] - servo1_current_position)> DXL_MOVING_STATUS_THRESHOLD) \
                and (not abs(goal_positions[index] - servo2_current_position)> DXL_MOVING_STATUS_THRESHOLD):
                break

        # Change goal position
        if index == 0:
            index = 1
        else:
            index = 0

    close_port(portHandler)


if __name__ == "__main__":
    main()
