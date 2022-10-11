# HiwonderServoController
LSC Series Servo Controller API for Python. At least the LX-225 is confirmed to work.

## Dependence
pyserial

## This library contains the following functions:
* Read angle function
* Set angle function
* Read voltage function

## example
```
#!/usr/bin/python3
# -*- coding: utf-8 -*-
# license removed for brevity

import HiwonderServoController as a

a.setConfig('/dev/ttyUSB0', 1)

a.moveServo(1, 500, 500)
a.moveServo(2, 500, 500)
a.moveServo(3, 200, 500)
print(a.getBatteryVoltage())
g = [1, 2, 3]
print(a.multServoPosRead(g))
```
