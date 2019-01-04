#!/usr/bin/python3

import socket
import sys
import threading
import time
import json

sys.path.append("../")

from Config.config import *
from Dtu_dev.dtu_dev import *

class pluse_server(threading.Thread):
    def __init__(self, name):
        threading.Thread.__init__(self)
        self.name = name
        self.location = dtu_config.config_data["network"]["location"]
        self.port = 20001
        self.max_listen = 1

        self.pluse_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.pluse_socket.bind((self.location, self.port))
        self.pluse_socket.listen(self.max_listen)
        self.pluse_chr = "www.aplexiot.com"

    def run(self):
        while True :
            self.client_socket, self.client_addr = self.pluse_socket.accept()
            dtu_dev.network_alive.clear()

            self.client_socket.setblocking(True)
            self.client_socket.settimeout(10)

            while True :

                try :
                    self.client_socket.send(self.pluse_chr.encode())
                except :
                    print("pluse send fail exit")
                    dtu_dev.network_alive.set()
                    self.client_socket.close()
                    #break

                try :
                    self.msg = self.client_socket.recv(16)
                except :
                    print("pluse timeout or diconnect")
                    dtu_dev.network_alive.set()
                    self.client_socket.close()
                    break;
                else :
                    if self.msg.decode() != self.pluse_chr:
                        print("pluse chr donot eq")
                        dtu_dev.network_alive.set()
                        self.client_socket.close()
                        break;
                    else :
                        #print(self.msg.decode())
                        pass


