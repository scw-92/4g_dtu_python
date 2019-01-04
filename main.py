#!/usr/bin/python3

from Dtu_eth.dtu_eth import *
from Dtu_serial.dtu_serial import *
from Config.config import *
from Dtu_dev.dtu_dev import *
from Dtu_pulse.dtu_pulse_server import *
from Dtu_websocket.dtu_websocket import *


if __name__ == "__main__" :
    serial_read_pre = dtu_serial("serial_read", dtu_dev.serial_com1, 0)
    serial_write_pre = dtu_serial("serial_write", dtu_dev.serial_com1, 1)
    #network_pre = dtu_network("network_pro")
    #dtu_pluse = pluse_server("dtu_pluse")
    dtu_websocket_pre = dtu_websocket("dtu_websocket")

    serial_read_pre.start()
    serial_write_pre.start()
    #network_pre.start()
    #dtu_pluse.start()
    dtu_websocket_pre.start()

    serial_read_pre.join()
    serial_write_pre.join()
    #network_pre.join()
    #dtu_pluse.join()
    dtu_websocket_pre.join()


