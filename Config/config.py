#!/usr/bin/python3

import os
import json

class configure():
    __configure_file_path = "Config/config.json"

    def __new__(cls, *args, **kwargs):

        if not hasattr(cls, "_inst"):

            cls._inst = super(configure, cls).__new__(cls);

            try :
                cls.config_file = open(cls.__configure_file_path)
            except :
                cls.__configure_file_path = "../Config/config.json"
                cls.config_file = open(cls.__configure_file_path)

            cls.config_data = json.load(cls.config_file)

            cls.config_file.close()

            cls.serial_com1_config = cls.config_data["serial"]["COM1"]
            cls.serial_com2_config = cls.config_data["serial"]["COM2"]

        return cls._inst

    def print_cfg(cls):
        print(cls.config_data)

    def set_config_file_path(cls, filepath):
        cls.__configure_file_path = filepath
        #print(cls.__configure_file_path)

    def save_config_data(cls):
        try :
            with open(cls.__configure_file_path, "w") as config_file :
                config_file.write(json.dumps(cls.config_data))
        except :
            print("write config data error")

dtu_config = configure()

if __name__ == "__main__":
    dtu_config.print_cfg()
    dtu_config.set_config_file_path("../Config/config.json")

