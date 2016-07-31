#!/usr/bin/env python
# encoding: utf-8


from concurrent.futures import ThreadPoolExecutor
from tornado.concurrent import run_on_executor
import requests
import json
from time import ctime


class Cloud(object):
    executor = ThreadPoolExecutor(2)

    def __init__(self, config):
        self.gw_url = config['url']
        self.headers = config['headers']

    @run_on_executor
    def upload(self, sensor_name, value):
        payload = [{"Name": sensor_name,
                    "Value": value}]

        try:
            r = requests.post(self.gw_url, data=json.dumps(payload), headers=self.headers)
        except Exception as e:
            print e
            return 0
            

        print ctime(), r.text
        return r.ok
