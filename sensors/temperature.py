#!/usr/bin/env python
# encoding: utf-8

from base import SensorBase
from tornado.concurrent import run_on_executor
from w1thermsensor import W1ThermSensor


class Sensor(SensorBase):
    def __init__(self, *args, **kwargs):
        super(Sensor, self).__init__(*args, **kwargs)

        self.name = self.config.get('name', 'temp')
        self.device = W1ThermSensor()

    @run_on_executor
    def get_value(self):
        value = self.device.get_temperature()

        return value

