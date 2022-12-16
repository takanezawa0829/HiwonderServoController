#!/usr/bin/python3
# -*- coding: utf-8 -*-
# license removed for brevity

#  * Copyright (c) 2022 TakumuTakanezawa
#  *
#  * Released under the GNU GENERAL PUBLIC LICENSE v3.
#  *
#  * The inherits function is:
#  * https://github.com/takanezawa0829/HiwonderServoController/blob/main/LICENSE

import serial

CMD_SERVO_MOVE = 0x03
CMD_GET_BATTERY_VOLTAGE = 0x0f
CMD_MULT_SERVO_POS_READ = 0x15

# set config
def setConfig(set_port = '/dev/ttyUSB0', timeout = 5):
    global _serial
    _serial = serial.Serial(set_port)
    _serial.baudrate = 9600
    _serial.parity = serial.PARITY_NONE
    _serial.bytesize = serial.EIGHTBITS
    _serial.stopbits = serial.STOPBITS_ONE
    _serial.timeout = timeout

# move any servo. (id: int[], position: int[], time: int)
def moveServoArray(id=None,position=None,time=None):
    buf = bytearray(b'\x55\x55')
    buf.append(5 + (len(id) * 3))
    buf.append(CMD_SERVO_MOVE)
    # # parameters
    buf.append(len(id))
    buf.extend([(0xff & time), (0xff & (time >> 8))])
    for i in range(len(id)):
        buf.append(id[i])
        buf.extend([(0xff & position[i]), (0xff & (position[i] >> 8))])
    _serial.write(buf)

# move the servo. (id: int, position: int, time: int)
def moveServo(id=None,position=None,time=None):
    buf = bytearray(b'\x55\x55')
    buf.append(8)
    buf.append(CMD_SERVO_MOVE)
    # parameters
    buf.append(1)
    buf.extend([(0xff & time), (0xff & (time >> 8))])
    buf.append(id)
    buf.extend([(0xff & position), (0xff & (position >> 8))])
    _serial.write(buf)

# get current voltage.
def getBatteryVoltage():
    buf = bytearray(b'\x55\x55')
    buf.append(2)
    buf.append(CMD_GET_BATTERY_VOLTAGE)
    _serial.write(buf)
    _serial.flush()
    result = _serial.readline()
    a = result[4] | result[5] << 8
    return a

# get current servo angle. (ids: array[id_1, id_2, ... , id_n])
def multServoPosRead(ids):
    buf = bytearray(b'\x55\x55')
    servo_num = len(ids)
    buf.append(servo_num + 3)
    buf.append(CMD_MULT_SERVO_POS_READ)
    buf.append(servo_num)
    for id in ids:
        buf.append(id)
    _serial.write(buf)
    _serial.flush()
    result = _serial.readline()

    data = {}
    for num in range(servo_num):
        i = 3 * num
        data[result[5 + i]] = result[5 + i + 1] | result[5 + i + 2] << 8

    return data
