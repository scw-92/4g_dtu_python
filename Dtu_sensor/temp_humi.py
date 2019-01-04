#!/usr/bin/python3

import time
import sys
import serial
import json

class temp_humi_dev():
    def __init__(self, com):
        self.cmd = {0x1, 0x3, 0x0, 0x2,0x0, 0x2, 0x65, 0xCB}
        self.com = com
        self.readlen = 9

    def read_all_data(self):
        self.com.write(self.cmd)
        time.sleep(0.1)
        self.recvmsg = self.com.read(self.readlen)
        print(self.recvmsg)


