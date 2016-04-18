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
import jsonpickle


def init(self):
    # put your self.registerOutput here
    self.registerOutput("headPosition", Obj("x", 0, "y", 0))
    self.registerOutput("lampPosition", Obj("z", 0))

def run (self):
    # put your init and global variables here
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
  
    # main loop
    while 1:
        # put your logic here
        # you can use: output, getInputs, message
        x = ser.readline()
        if x:
            try:
                r_obj = jsonpickle.decode(x)
                addToMemory(self, r_obj['tag'], r_obj['data'])
            except:
                pass



def addToMemory(self, key, obj):
    self.output(key, obj)


def checkMemory(self, key):
    print 'getting ' + key
    return self.getInputs()[key]