#!/usr/bin/env python
# encoding: utf-8

from config import config
from tornado import ioloop, gen, autoreload
from utils import RollingMean

import sensors
import clouds



def init_sensors(cloud_instances):

    @gen.coroutine
    def callback(name, value):
        for cloud  in cloud_instances:
            yield cloud.upload(name, value)

    sensors_ins = []
    sensors_name = config['sensors'].keys()
    for name in sensors_name:
        if config['sensors'][name]['enable']:
            sensors_ins.append(
                sensors.SENSORS[name](config['sensors'][name]['device'], callback))

    return sensors_ins

def init_clouds():
    cloud_ins = []
    clouds_name = config['cloud'].keys()
    for name in clouds_name:
        if config['cloud'][name]['enable']:
            cloud_ins.append(
                clouds.CLOUDS[name](config['cloud'][name]))

    return cloud_ins

@gen.coroutine
def start_detect(sensors_instances):


    print("Enter main loop")
    test_count = 0
    while 1:
        for sensor in sensors_instances:
            sensor.queue.put(test_count)
        test_count += 1

        yield gen.sleep(15)

if __name__ == '__main__':
    cloud_instances = init_clouds()
    sensors_instances = init_sensors(cloud_instances)

    for sensor in sensors_instances:
        sensor.run()

    print("starting detect")
    start_detect(sensors_instances)

    instance = ioloop.IOLoop.instance()
    autoreload.start(instance)
    instance.start()

