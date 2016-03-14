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
import cPickle as pickle
import json
import jsonpickle

def init(self):
    # put your self.registerOutput here
    self.registerOutput("facePos", Obj("x", 0, "y", 0))


def run (self):
    # put your init and global variables here
    to_get = ["facePos"]

    s = socket.socket()
    host = '192.168.0.136'
    port = 12345
    s.connect((host, port))
    xPos = 1
    yPos = 1
    # main loop
    while 1:
        addToMemory(self, "facePos", Obj("x", xPos, "y", yPos))
        xPos += 1
        yPos += 1

        for tag in to_get:
            obj = checkMemory(self, tag)
            print 'obj'
            print str(obj)
            if obj is not None:
                print obj.__data__
                owner = obj.__data__['owner']
                del obj.__data__['owner']
                sending = jsonpickle.encode(obj.__data__)
                obj.__data__['owner'] = owner
                print 'sending: ' + sending
                s.sendall(sending)


def addToMemory(self, key, obj):
    self.output(key, obj)
    time.sleep(5)


def checkMemory(self, key):
    print 'getting ' + key
    return self.getInputs()[key]
