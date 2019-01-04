#!/usr/bin/python3

import threading
import time
import sys
import json
from websocket_server import WebsocketServer

sys.path.append("../")

from Config.config import *
from Dtu_dev.dtu_dev import *
from Dtu_sensor.crc import *




#不包含crc检验码，检验码动态生成
line_chart_cmd = {
    "air_humidity":[0x1, 0x3, 0x0, 0x0, 0x0, 0x2],
    "temperature":[0x1, 0x3, 0x0, 0x0, 0x0, 0x2],
    "soil_moisture":[0x2, 0x3, 0x0, 0x2, 0x0, 0x1],
    "light_intensity":[0x3, 0x3, 0x0, 0x2, 0x0, 0x2],
    "CO2_concentration":[0x4, 0x3, 0x0, 0x5, 0x0, 0x1],
    "pressure":[0x5, 0x3, 0x0, 0x2, 0x0, 0x2],
    "rainfall":[0x6, 0x3, 0x0, 0x2, 0x0, 0x2]
}



'''
{
        "opt_type" : "witelist",
        "type" : "firewall",
        "ip" : "",
        "ip_direction" : "input", // "output" , "all"
        "port" : 7777,
        "port_direction" : "input", // "output" , "all"
        "protocol" : "tcp", // "udp" "all"
        "protocol_direction" : "input" // "output" "all"
}
'''
def dtu_firewall(firewall_msg):
    print(firewall_msg)
    if (firewall_msg["opt_type"] == "blacklist"):
        if (len(firewall_msg["ip"] > 0)) :
            if (firewall_msg["ip_direction"] == "input"):
                cmd = "iptables" + " -A INPUT " + " -s " + firewall_msg["ip"] + " -j DROP"
            elif (firewall_msg["ip_direction"] == "output"):
                cmd = "iptables" + " -A OUTPUT " + " -s " + firewall_msg["ip"] + " -j DROP"
            elif (firewall_msg["ip_direction"] == "all"):
                cmd = "iptables" + " -A OUTPUT " + " -s " + firewall_msg["ip"] + " -j DROP"
                cmd = "iptables" + " -A INPUT " + " -s " + firewall_msg["ip"] + " -j DROP"

        if (len(firewall_msg["port"] > 0)):
            if (firewall_msg["port_direction"] == "input"):
                cmd = "iptables" + " -A INPUT -p tcp --dport " + firewall_msg["port"] + " -j ACCEPT"
            elif (firewall_msg["port_direction"] == "output"):
                cmd = "iptables" + " -A OUTPUT -p tcp --dport " + firewall_msg["port"] + " -j ACCEPT"
            elif (firewall_msg["port_direction"] == "all"):
                cmd = "iptables" + " -A OUTPUT -p tcp --dport " + firewall_msg["port"] + " -j ACCEPT"
                cmd = "iptables" + " -A INPUT -p tcp --dport " + firewall_msg["port"] + " -j ACCEPT"

        if (len(firewall_msg["protocol"]) > 0):
            if (firewall_msg["protocol_direction"] == "input"):
                cmd = "iptables" + " -A INPUT -p " + firewall_msg["protocol"]  + " -j ACCEPT"
            elif (firewall_msg["protocol_direction"] == "output"):
                cmd = "iptables" + " -A OUTPUT -p " + firewall_msg["protocol"] + " -j ACCEPT"
            elif (firewall_msg["protocol_direction"] == "all"):
                cmd = "iptables" + " -A OUTPUT -p " + firewall_msg["protocol"] + " -j ACCEPT"
                cmd = "iptables" + " -A INPUT -p " + firewall_msg["protocol"]  + " -j ACCEPT"

        print(cmd)
    elif (firewall_msg["opt_type"] == "whitelist"):
        pass
        print(cmd)

class dtu_websocket(threading.Thread):
    def __init__(self, name):
        threading.Thread.__init__(self)
        self.name = name
        self.port = 9001
        self.addr = "0.0.0.0"

    def new_client(self, client, server):
        print("new clinet %d" % client["id"])

    def client_left(self, client, server):
        print(" clinet %d lift" % client["id"])

    def client_msg_received(self, client, server, message):

        msg = json.loads(message)

        if (msg["type"] == "line_chart"):
            if(msg["line_time"] == "real_time"):
                line_crc = Crc()
                for l_name in msg["line_name"]:
                    #print(line_chart_cmd[l_name] + line_crc.ca_crc(line_chart_cmd[l_name]))
                    #dtu_dev.network_recv_queue.put(self.temp_humi_cmd)
                   
                    #print(l_name)
                    #if(msg["line_name"])
                    #self.temp_humi_cmd = [0x1, 0x3, 0x0, 0x0, 0x0, 0x2, 0xc4, 0xb]
                    dtu_dev.network_recv_queue.put(line_chart_cmd[l_name] + line_crc.ca_crc(line_chart_cmd[l_name]))
                    time.sleep(0.2)
                self.server_send(client)
        elif (msg["type"] == "firewall"):
            dtu_firewall(msg)

    def server_send(self, client):
        msg_array = []
        send_msg = {
                "type" : "line_chart",
                "data_type" : "real_time",
                "data" : {
                    # "temperature" : [[-1, "xxxx"]],
                    # "air_humidity" : [[-1, "xxxx"]],
                    # "soil_moisture" : [[-1, "xxxx"]],
                    # "light_intensity" : [[-1, "xxxx"]],
                    # "CO2_concentration" : [[-1, "xxxx"]],
                    # "pressure" : [[-1, "xxxx"]]
                },
                "uart_name" : "/dev/ttyO1",
                }
        try :
            while not(dtu_dev.network_send_queue.empty()):
                 time.sleep(0.05)
                 msg = dtu_dev.network_send_queue.get(\
                    timeout = dtu_config.config_data["network"]["timeout"])
                 msg_array.append(msg)
            #print(len(msg_array))
        except :
            msg = None


    #     "air_humidity":[0x1, 0x3, 0x0, 0x0, 0x0, 0x2],
    # "soil_moisture":[0x3, 0x3, 0x0, 0x2, 0x0, 0x2],
    # "light_intensity":[0x3, 0x3, 0x0, 0x2, 0x0, 0x2],
    # "CO2_concentration":[0x3, 0x3, 0x0, 0x2, 0x0, 0x2],
    # "pressure":[0x3, 0x3, 0x0, 0x2, 0x0, 0x2],
    # "temperature":[0x3, 0x3, 0x0, 0x2, 0x0, 0x2],
    # "rainfall":[0x3, 0x3, 0x0, 0x2, 0x0, 0x2]
        

        #print(msg_array)
        if(len(msg_array)):
            for sen_msg in msg_array:
                if(sen_msg[0] == 1):
                    #print(sen_msg)
                    send_msg["data"]["temperature"]          = [[-1, "xxxx"]]
                    send_msg["data"]["air_humidity"]         = [[-1, "xxxx"]]
                    send_msg["data"]["temperature"][0][0]    = ((sen_msg[3] << 8) + sen_msg[4]) / 10
                    send_msg["data"]["air_humidity"][0][0]   = ((sen_msg[5] << 8) + sen_msg[6]) / 10
                    send_msg["data"]["temperature"][0][1]    = time.strftime("%H:%M:%S", time.localtime())
                    send_msg["data"]["air_humidity"][0][1]   = time.strftime("%H:%M:%S", time.localtime())
                elif(sen_msg[0] == 2):
                    send_msg["data"]["soil_moisture"]          = [[-1, "xxxx"]]
                    send_msg["data"]["soil_moisture"][0][0]    = int.from_bytes(sen_msg[3:5], byteorder='big', signed=False) / 10
                    send_msg["data"]["soil_moisture"][0][1]    = time.strftime("%H:%M:%S", time.localtime())
                elif(sen_msg[0] == 3):
                    send_msg["data"]["light_intensity"]          = [[-1, "xxxx"]]
                    send_msg["data"]["light_intensity"][0][0]    = int.from_bytes(sen_msg[3:7], byteorder='big', signed=False)
                    send_msg["data"]["light_intensity"][0][1]    = time.strftime("%H:%M:%S", time.localtime())
                elif(sen_msg[0] == 4):
                    send_msg["data"]["CO2_concentration"]          = [[-1, "xxxx"]]
                    send_msg["data"]["CO2_concentration"][0][0]    = int.from_bytes(sen_msg[3:5], byteorder='big', signed=False)
                    send_msg["data"]["CO2_concentration"][0][1]    = time.strftime("%H:%M:%S", time.localtime())
                elif(sen_msg[0] == 5):
                    send_msg["data"]["pressure"]          = [[-1, "xxxx"]]
                    send_msg["data"]["pressure"][0][0]    = ((sen_msg[3] << 8) + sen_msg[4]) / 10
                    send_msg["data"]["pressure"][0][1]    = time.strftime("%H:%M:%S", time.localtime())
                elif(sen_msg[0] == 6):
                    send_msg["data"]["rainfall"]          = [[-1, "xxxx"]]
                    send_msg["data"]["rainfall"][0][0]    = ((sen_msg[3] << 8) + sen_msg[4]) / 10
                    send_msg["data"]["rainfall"][0][1]    = time.strftime("%H:%M:%S", time.localtime())

        # if (msg != None) :
        #     if (len(msg) > 8):
        #         send_msg["data"]["temperature"][0][0] = ((msg[3] << 8) + msg[4]) / 10
        #         send_msg["data"]["air_humidity"][0][0] = ((msg[5] << 8) + msg[6]) / 10
        #         #send_msg["data"]["temperature"][1] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        #         send_msg["data"]["temperature"][0][1] = time.strftime("%H:%M:%S", time.localtime())
        #         send_msg["data"]["air_humidity"][0][1] = time.strftime("%H:%M:%S", time.localtime())
        #         #send_msg["data"]["humidity"][1] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())

        #     if (send_msg["data"]["temperature"][0][0] == -1) :
        #         send_msg["data"]["temperature"][0][0] = "-"

        #     if (send_msg["data"]["air_humidity"][0][0] == -1) :
        #         send_msg["data"]["air_humidity"][0][0] = "-"
        # else :
        #     send_msg["data"]["temperature"][0][0] = "-"
        #     send_msg["data"]["air_humidity"][0][0] = "-"
        #     send_msg["data"]["temperature"][0][1] = time.strftime("%H:%M:%S", time.localtime())
        #     send_msg["data"]["air_humidity"][0][1] = time.strftime("%H:%M:%S", time.localtime())

        #print(send_msg)
        self.websocket_server.send_message(client, json.dumps(send_msg))

    def websocket_init(self):
        self.websocket_server = WebsocketServer(self.port, self.addr)
        self.websocket_server.set_fn_new_client(self.new_client)
        self.websocket_server.set_fn_client_left(self.client_left)
        self.websocket_server.set_fn_message_received(self.client_msg_received)
        self.websocket_server.run_forever()

    def run(self):
        self.websocket_init()
