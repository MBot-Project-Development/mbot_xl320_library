# this is example shows a single servo rotate in wheel mode

from mbot_xl320_library import *

# user defined value
DXL_MOVING_STATUS_THRESHOLD = 20  # Dynamixel moving status threshold


def main():
    portHandler, packetHandler = initialize_handlers("/dev/ttyACM0")
    servo1_ID = 2
    open_port(portHandler)
    set_baudrate(portHandler, 1000000)

    servo1 = Servo(servo1_ID, portHandler, packetHandler)
    servo1.change_led_color(LED_CYAN)
    servo1.disable_torque()
    servo1.set_control_mode("wheel")  # note that when you change mode, torque needs to be off

    servo1.enable_torque()
    servo1.set_wheel_cw_speed(50)  # value is in percentage

    print("Press ESC to stop the servo.")
    try:
        while True:  # Start a loop that will run until ESC is pressed
            if getch() == chr(0x1B):
                servo1.set_wheel_cw_speed(0)  # Stop the servo by setting speed to 0
                break

    except KeyboardInterrupt:
        servo1.set_wheel_cw_speed(0)

    finally:
        servo1.disable_torque()
        close_port(portHandler)


if __name__ == "__main__":
    main()
