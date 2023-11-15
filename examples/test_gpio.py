import Jetson.GPIO as GPIO
import time
from dynamixel_sdk import PortHandler, PacketHandler, COMM_SUCCESS  # Assuming these are from the Dynamixel SDK

# Setup GPIO and Dynamixel SDK instances
CTL_PIN = 18  # Adjust to the correct pin
GPIO.setmode(GPIO.BOARD)  # BOARD pin-numbering scheme
GPIO.setup(CTL_PIN, GPIO.OUT)  # CTL pin set as output
GPIO.output(CTL_PIN, GPIO.LOW)  # Initialize as LOW (receiving mode)

portHandler = PortHandler('/dev/ttyTHS1')  # Set the correct port name
packetHandler = PacketHandler(2.0)  # Set the protocol version

portHandler.openPort()
portHandler.setBaudRate(1000000)

def writeAndRead(servoid, address, value):
    # Toggle CTL pin for transmission
    GPIO.output(CTL_PIN, GPIO.HIGH)
    time.sleep(0.002)  # Wait for the line to settle if needed

    # Write byte to servo and read response
    dxl_comm_result, dxl_error = packetHandler.write1ByteTxRx(portHandler, servoid, address, value)
    
    # Toggle CTL pin to receive
    GPIO.output(CTL_PIN, GPIO.LOW)
    time.sleep(0.002)  # Ensure there's enough time for servo to respond before any other write
    
    if dxl_comm_result != COMM_SUCCESS:
        print("%s" % packetHandler.getTxRxResult(dxl_comm_result))
    elif dxl_error != 0:
        print("%s" % packetHandler.getRxPacketError(dxl_error))
    else:
        print("Write and read successful!")

    return dxl_comm_result, dxl_error

# Use the function to write to servo and read response
servo_id = 1  # Your servo ID
address = 25  # Example address
value = 4    # Example value to write
writeAndRead(servo_id, address, value)

# Cleanup
portHandler.closePort()
GPIO.cleanup()
