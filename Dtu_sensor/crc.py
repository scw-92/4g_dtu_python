#!/usr/bin/python3

class Crc():
    def __init__(self):
        self.crc_result = 0xffff

    def ca_crc(self, data_array):
        self.crc_result = 0xffff
        #for index in range(len(data_array) - 2):
        for index in range(len(data_array)):
            #print("0x%x" % data_array[index])

            self.crc_result ^= data_array[index]
            crc_num = (self.crc_result & 0x0001)

            for m in range(8):
                if crc_num :
                    xor_flag = 1;
                else:
                    xor_flag = 0

                self.crc_result >>= 1;

                if (xor_flag):
                    self.crc_result ^= 0xa001

                crc_num = (self.crc_result & 0x0001)
        return [ self.crc_result & 0xff, self.crc_result >> 8 ]
