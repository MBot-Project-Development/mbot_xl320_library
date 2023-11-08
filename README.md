This is a python library for XL320 servo using DynamixelSDK.

## Install
```bash
$ ./install.sh
```

## Examples
Example `rotate_full_range.py`: 

Modify your config in the code (portname, id, baudrate) first,
```python
portHandler, packetHandler = initialize_handlers('/dev/ttyACM0')

servo1_ID = 1
servo2_ID = 2

open_port(portHandler)
set_baudrate(portHandler, 1000000)
```
then run the following:
```bash
$ cd examples/
$ sudo python3 rotate_full_range.py
```