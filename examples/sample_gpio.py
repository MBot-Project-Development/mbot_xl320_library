from mbot_xl320_library import *
import Jetson.GPIO as GPIO

def main():

    initialize_GPIO()
    portHandler, packetHandler = initialize_handlers("/dev/ttyTHS1")

    # defines the servo's ID
    servo1_ID = 1

    open_port(portHandler)
    set_baudrate(portHandler, 1000000)

    servo1 = Servo(servo1_ID, portHandler, packetHandler)
    servo1.change_led_color(LED_GREEN)
    GPIO.output(12, GPIO.HIGH)
    servo1.enable_torque()
    close_port(portHandler)
    close_GPIO()

if __name__ == "__main__":
    main()
