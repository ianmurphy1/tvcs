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
    # put your self.registerOutput here
    self.registerOutput("facePos1", Obj("x", 0, "y", 0))
    self.registerOutput("facePos2", Obj("x", 0, "y", 0))


def run(self):
    # put your init and global variables here
    to_get = ["facePos1", "facePos2"]
    ser = serial.Serial(
               port='/dev/ttyAMA0',
               baudrate = 115200,
               parity=serial.PARITY_NONE,
               stopbits=serial.STOPBITS_ONE,
               bytesize=serial.EIGHTBITS,
               timeout=1
    )
    ser.flushInput()
    ser.flushOutput()
    counter=0
    xPos = 8000
    yPos = 8000
    # main loop
    while 1:
        # put your logic here
        # you can use: output, getInputs, message 
        addToMemory(self, "facePos1", Obj("x", xPos, "y", yPos))
        addToMemory(self, "facePos2", Obj("x", xPos, "y", yPos))
        xPos += 1
        yPos += 1
        for tag in to_get:
            obj = checkMemory(self, tag)
            if obj is not None:
                sending = {
                    'tag': tag,
                    'data': obj.__data__
                }
                send_string = jsonpickle.encode(sending)
                ser.write(send_string + '\n')



def addToMemory(self, key, obj):
    self.output(key, obj)


def checkMemory(self, key):
    print 'getting ' + key
    return self.getInputs()[key]