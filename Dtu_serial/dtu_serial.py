#!/usr/bin/python3

import serial
import threading
import time
import sys

sys.path.append("../")

from Dtu_dev.dtu_dev import *

class dtu_serial(threading.Thread) :
    def __init__(self, name, serial_com, flag):
        threading.Thread.__init__(self)
        self.name = name
        self.serial_com = serial_com
        self.flag = flag

    def msg_put_to_serial(self):
        while True :
            try :
                msg = dtu_dev.network_recv_queue.get(
                    timeout = dtu_config.config_data["network"]["timeout"])
                if(1):
                    self.serial_com.write(msg)
                    time.sleep(0.05)
                    #print(msg)

            except :
                pass
                #print("serial write fial or queue timeout")

    def msg_get_from_serial(self):
        while True :
            


            #     msg = self.serial_com.read(1)
            #     if(msg[0] == 3):
            #         msg = msg + self.serial_com.read(8)
                
            #     #print(msg)
                
            #     #print("serial read len : %d" % len(msg))
            #     if (len(msg) > 0):
            #         dtu_dev.network_send_queue.put(msg)
            #     msg = b""
            # except :
            #     pass
            try :
                data=self.serial_com.read(1)
                if data:
                    time.sleep(0.01)
                    n = self.serial_com.inWaiting()
                    if n:
                        data = data + self.serial_com.read(n)
                        dtu_dev.network_send_queue.put(data)                
                data = b""
            except :
                pass
    def run(self):
        if (self.flag) :
            self.msg_put_to_serial()
        else :
            self.msg_get_from_serial()

