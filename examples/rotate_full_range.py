# this is example shows a single servo rotate between
# 2 limits end, in joint mode.

from mbot_xl320_library import *

# user defined value
DXL_MOVING_STATUS_THRESHOLD = 20        # Dynamixel moving status threshold

def main():
    portHandler, packetHandler = initialize_handlers('/dev/ttyACM0')
    servo1_ID = 1
    open_port(portHandler)
    set_baudrate(portHandler, 1000000)

    servo1 = Servo(servo1_ID, portHandler, packetHandler)
    servo1.change_led_color(LED_RED)    
    servo1.disable_torque()
    servo1.set_control_mode("joint")  # note that when you change mode, torque needs to be off
    servo1.enable_torque()

    index = 0
    goal_positions = [DXL_MINIMUM_POSITION_VALUE, DXL_MAXIMUM_POSITION_VALUE] # this is the actual limits of the servo
    servo1.set_joint_speed(300) # range(0,1023)
    while True:
        print("Press any key to continue! (or press ESC to quit!)")
        if getch() == chr(0x1b):
            break

        servo1.set_position(goal_positions[index])

        while True:
            servo1_current_position = servo1.get_position()
            if goal_positions[index] is None or servo1_current_position is None:
                continue
            
            print("[ID:%d] GoalPos:%d  PresPos:%d" % (servo1_ID, goal_positions[index], servo1_current_position))
            if not abs(goal_positions[index] - servo1_current_position) > DXL_MOVING_STATUS_THRESHOLD:
                break
        
        # Change goal position
        if index == 0:
            index = 1
        else:
            index = 0

    close_port(portHandler)

if __name__ == '__main__':
    main()