#!/usr/bin/python

import time

# import from parent directory
import sys
import os.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir)))

import DynamicObjectV2
Obj = DynamicObjectV2.Class

# put your imports here
import serial
import struct
import jsonpickle


def init(self):
    pass


def run(self):
    # put your init and global variables here
    to_get = ["headPosition", "lampPosition"]
    ser = serial.Serial(
               port='/dev/ttyAMA0',
               baudrate=115200,
               parity=serial.PARITY_NONE,
               stopbits=serial.STOPBITS_ONE,
               bytesize=serial.EIGHTBITS,
               timeout=1
    )
    ser.flushInput()
    ser.flushOutput()
    z = y = x = 0
    # main loop
    while 1:
        # put your logic here

        # you can use: output, getInputs, message
        for tag in to_get:
            obj = checkMemory(self, tag)
            if obj is not None:
                ser.flushOutput()
                sending = {
                    'tag': tag,
                    'data': obj.__data__
                }
                send_string = jsonpickle.encode(sending)
                ser.write(send_string + '\n')
                time.sleep(0.1)


def addToMemory(self, key, obj):
    self.output(key, obj)


def checkMemory(self, key):
    print 'getting ' + key
    return self.getInputs()[key]