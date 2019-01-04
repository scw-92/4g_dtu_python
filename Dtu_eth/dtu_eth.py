#!/usr/bin/python3

import socket
import sys
import threading
import time

sys.path.append("../")

from Config.config import *
from Dtu_dev.dtu_dev import *

class dtu_server(threading.Thread):
    def __init__(self, name):
        threading.Thread.__init__(self)
        self.name = name

    def run(self):
        while True :
            dtu_dev.network_alive.clear()
            self.client_socket, self.addr = dtu_dev.socket.accept()

            self.client_socket.setblocking(True)
            self.client_socket.settimeout(dtu_config.config_data["network"]["timeout"])

            self.dtu_server_recv = dtu_server_run("server_recv", \
                    self.client_socket, 1)
            self.dtu_server_send = dtu_server_run("server_send", \
                    self.client_socket, 0)

            self.dtu_server_recv.start()
            self.dtu_server_send.start()

            self.dtu_server_recv.join()
            self.dtu_server_send.join()

            self.client_socket.close()
            time.sleep(2)


class dtu_server_run(threading.Thread):
    def __init__(self, name, client_socket, flag):
        threading.Thread.__init__(self)
        self.name = name
        self.client_socket = client_socket
        self.flag = flag

    def socket_recv(self):
        while True :
            if dtu_dev.network_alive.is_set() :
                break

            try :
                msg = self.client_socket.recv(256)
            except socket.gaierror:
                print("clinet recv gaierror")
            except socket.timeout:
                msg = None
                continue
            except OSError :
                print("client recv OSError and exit")
            else :
                if (not dtu_dev.network_recv_queue.full()) :
                    dtu_dev.network_recv_queue.put(msg)

    def socket_send(self):
        while True :
            if dtu_dev.network_alive.is_set() :
                break

            try :
                msg = dtu_dev.network_send_queue.get(\
                        timeout = dtu_config.config_data["network"]["timeout"])
            except :
                continue

            try :
                self.client_socket.send(msg)
            except :
                print("socket send timeout")
                break

    def run(self):
        if (self.flag == 1) :
            self.socket_recv()
        elif (self.flag == 0):
            self.socket_send()

class dtu_client(threading.Thread):
    def __init__(self, name, flag):
        threading.Thread.__init__(self)
        self.name = name
        self.flag = flag
        self.socket = dtu_dev.socket

        dtu_dev.socket.setblocking(True)
        dtu_dev.socket.settimeout(dtu_config.config_data["network"]["timeout"])

    def socket_recv(self):
        while True :
            try :
                msg = self.socket.recv(256)
            except :
                pass
            else :
                if (not dtu_dev.network_recv_queue.full()) :
                    dtu_dev.network_recv_queue.put(msg)

    def socket_send(self):
        while True :
            try :
                msg = dtu_dev.network_send_queue.get(\
                        timeout = dtu_config.config_data["network"]["timeout"])
                self.socket.send(msg)
            except :
                pass

    def run(self):
        if (self.flag == 1):
            self.socket_recv()
        elif (self.flag == 0):
            self.socket_send()


class dtu_network(threading.Thread):
    def __init__(self, name):
        threading.Thread.__init__(self)
        self.name = name

    def run(self):
        if dtu_config.config_data["network"]["type"] == "server" :
            dtu_network_server_send_msg = dtu_server("dtu_network_send")

            dtu_network_server_send_msg.start()

            dtu_network_server_send_msg.join()

        elif dtu_config.config_data["network"]["type"] == "client" :
            dtu_network_client_send_msg = dtu_client("dtu_network_send", 0)
            dtu_network_client_recv_msg = dtu_client("dtu_network_recv", 1)

            dtu_network_client_send_msg.start()
            dtu_network_client_recv_msg.start()

            dtu_network_client_send_msg.join()
            dtu_network_client_recv_msg.join()

