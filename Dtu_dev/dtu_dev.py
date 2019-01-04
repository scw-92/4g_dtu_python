#!/usr/bin/python3

import serial
import json
import sys
import queue
import socket
import fcntl
import struct
import threading

sys.path.append("../")

from Config.config import *

def get_ip_address(ifname):
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    return socket.inet_ntoa(fcntl.ioctl(
        s.fileno(), \
        0x8915, \
        struct.pack("256s".encode(), ifname[:15].encode())  \
    )[20:24])


class dtu_device():
    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, "_inst"):
            cls._inst = super(dtu_device, cls).__new__(cls)

            try :
                cls.serial_com1 = serial.Serial(\
                        dtu_config.serial_com1_config["port"], \
                        dtu_config.serial_com1_config["baudrate"], \
                        timeout = dtu_config.serial_com1_config["timeout"])
                cls.serial_com2 = serial.Serial(\
                        dtu_config.serial_com2_config["port"], \
                        dtu_config.serial_com2_config["baudrate"], \
                        timeout = dtu_config.serial_com2_config["timeout"])
            except :
                print("open device error")

            if dtu_config.config_data["network"]["protocol"] == "tcp" :
                cls.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            elif dtu_config.config_data["network"]["protocol"] == "udp" :
                cls.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            else :
                print("protocol error")

            #cls.target = dtu_config.config_data["network"]["target"]
            cls.target = get_ip_address("eth0")
            cls.port = dtu_config.config_data["network"]["port"]
            cls.localtion = get_ip_address("eth0")
            cls.max_listen = 5

            if dtu_config.config_data["network"]["type"] == "client" :
                cls.socket.connect((cls.target, cls.port))
            elif dtu_config.config_data["network"]["type"] == "server" :
                cls.socket.bind((cls.localtion, cls.port))
                cls.socket.listen(cls.max_listen)

            cls.network_recv_queue = queue.Queue(maxsize = 2048)
            cls.network_send_queue = queue.Queue(maxsize = 2048)

            cls.network_alive = threading.Event()
            cls.network_alive.clear()

        return cls._inst

dtu_dev = dtu_device()


