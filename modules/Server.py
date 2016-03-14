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
import jsonpickle

def init(self):
    # put your self.registerOutput here
    self.registerOutput("facePos", Obj("x", 0, "y", 0))


def run (self):
    # put your init and global variables here
    s = socket.socket()
    host = ''
    port = 12345
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind((host, port))

    s.listen(5)
    # main loop
    while 1:
        # put your logic here
        # you can use: output, getInputs, message
        c, addr = s.accept()
        print 'Got connection from', addr

        while 1:
            data, _ = c.recvfrom(4096)
            r_obj = jsonpickle.decode(data)
            print 'received from client'
            print r_obj
            addToMemory(self, "facePos", r_obj)

        c.close()


def addToMemory(self, key, obj):
    self.output(key, obj)
    time.sleep(5)


def checkMemory(self, key):
    return self.getInputs()[key]
