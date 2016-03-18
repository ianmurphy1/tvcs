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
import struct
def init(self):
    # put your self.registerOutput here
    self.registerOutput("facePos1", Obj("x", 0, "y", 0))
    self.registerOutput("facePos2", Obj("x", 0, "y", 0))


def run (self):
    # put your init and global variables here
    to_get = ["facePos1", "facePos2"]
    s = socket.socket()
    s.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
    host = 'localhost'
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
                sending = {
                    'tag': tag,
                    'data': obj.__data__
                }
                send_string = jsonpickle.encode(sending)
                send_one_message(s, send_string)


def addToMemory(self, key, obj):
    self.output(key, obj)


def checkMemory(self, key):
    print 'getting ' + key
    return self.getInputs()[key]

def send_one_message(sock, data):
    length = len(data)
    sock.sendall(struct.pack('!I', length))
    sock.sendall(data)

def recv_one_message(sock):
    lengthbuf = recvall(sock, 4)
    length, = struct.unpack('!I', lengthbuf)
    return recvall(sock, length)

def recvall(sock, count):
    buf = b''
    while count:
        newbuf = sock.recv(count)
        if not newbuf: return None
        buf += newbuf
        count -= len(newbuf)
    return buf