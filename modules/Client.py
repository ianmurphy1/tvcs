#!/usr/bin/python

import time

# import from parent directory
import sys
import os.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir)))

import DynamicObjectV2
Obj = DynamicObjectV2.Class

# put your imports here
import socket

def init(self):
    # put your self.registerOutput here
    self.registerOutput("facePos1", Obj("x", 0, "y", 0))
    self.registerOutput("facePos2", Obj("x", 0, "y", 0))


def run (self):
    # put your init and global variables here
    to_get = ["facePos1", "facePos2"]
    s = socket.socket()
    host = '192.168.0.136'
    port = 12345
    s.connect((host, port))
    xPos = 8000
    yPos = 8000
    # main loop
    while 1:
        addToMemory(self, "facePos1", Obj("x", xPos, "y", yPos))
        addToMemory(self, "facePos2", Obj("x", xPos, "y", yPos))
        time.sleep(5)
        xPos += 1
        yPos += 1
        for tag in to_get:
            obj = checkMemory(self, tag)
            if obj is not None:
                sending = {}
                sending['tag'] = tag
                sending['data'] = obj.__to_json__()
                self.message('sending {}'.format(sending))
                print 'size of sending: {}'.format(len(sending))
                self.message('sending {}'.format(sending))
                s.sendall(sending)


def addToMemory(self, key, obj):
    self.output(key, obj)


def checkMemory(self, key):
    print 'getting ' + key
    return self.getInputs()[key]
