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
    s = socket.socket()
    host = ''
    port = 12345
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
    s.bind((host, port))
    s.listen(5)
    # main loop
    while 1:
        # put your logic here
        # you can use: output, getInputs, message
        c, addr = s.accept()
        self.message('Got connection from {}'.format(addr))
        print 'look for connection loop'

        while 1:
            print 'server while loop'
            data = recv_one_message(c)
            if not data:
                self.message('connection broke')
                break
            r_obj = jsonpickle.decode(data)
            addToMemory(self, r_obj['tag'], r_obj['data'])

        c.close()


def addToMemory(self, key, obj):
    self.output(key, obj)
    time.sleep(5)


def checkMemory(self, key):
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