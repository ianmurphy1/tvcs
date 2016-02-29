#!/usr/bin/python

import DynamicObjectV2
Obj = DynamicObjectV2.Class

import time
import random

# import from parent directory
import sys
import os.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir)))

def run (self):
  self.registerOutput("facePos", Obj("x", 0, "y", 0))
  while 1:
    self.registerOutput("facePos", Obj("x", random.randint(-90, 90), "y", random.randint(-90, 90)))
    time.sleep(5)