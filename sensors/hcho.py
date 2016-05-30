#!/usr/bin/env python
# encoding: utf-8

import serial
import struct
from base import SensorBase
from tornado.concurrent import run_on_executor

class Sensor(SensorBase):
    def __init__(self, *args, **kwargs):
        super(Sensor, self).__init__(*args, **kwargs)

        serial_path = self.config.get('serial', "")
        baudrate = self.config.get('baudrate', 9600)
        self.name = self.config.get('name', 'hcho')
        self.device = serial.Serial(serial_path, baudrate=baudrate)

    def reset(self):
        req_data = (0xa5, 0x5a, 0x02, 0x85, 0xaa)
        req_data = struct.pack("!5B", *req_data)

        self.device.write(req_data)

    @run_on_executor
    def get_value(self):
        req_data = (0xa5, 0x5a, 0x02, 0xc3, 0xaa)
        req_data = struct.pack("!5B", *req_data)

        self.device.write(req_data)

        resp_data = client.read(15)
        resp_data = struct.unpack("!4xH4xHHx", resp_data)

        value = resp_data[1]/100.0

        return value