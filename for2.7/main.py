#!/usr/bin/env python
# encoding: utf-8

import sys
sys.path.append("/home/ubuntu/mytvoc")

from conf import config as conf
from common import RollingMean
import serial
import struct
from time import sleep, ctime
import requests
import json


rollmean = RollingMean(6)

def init_HCHO_sensor():
    print("Opening serial %s" % conf['hcho']['serial'])
    client = serial.Serial(conf['hcho']['serial'], baudrate=conf['hcho']['baudrate'])
    return client

def request_HCHO_value(client):
    req_data = (0xa5, 0x5a, 0x02, 0xc3, 0xaa)
    req_data = struct.pack("!5B", *req_data)

    client.write(req_data)

    resp_data = client.read(15)
    resp_data = struct.unpack("!4xH4xHHx", resp_data)
    print resp_data
    return resp_data[1]/100.0

def reset_HCHO_detector(client):
    req_data = (0xa5, 0x5a, 0x02, 0x85, 0xaa)
    req_data = struct.pack("!5B", *req_data)

    client.write(req_data)

def upload_HCHO_value(value):
    payload = [
        {
            "Name": "hcho",
            "Value": value
        }
    ]
    cloud = conf['cloud']
    r = requests.post(cloud['url'], data=json.dumps(payload), headers=cloud['headers'])
    print r.text


def main():
    hcho_client = init_HCHO_sensor()
    #reset_HCHO_detector(hcho_client)

    while 1:
        try:
            print ctime()
            hcho_value = request_HCHO_value(hcho_client)
            rollmean.append(hcho_value)
            value = rollmean.get_mean()
            upload_HCHO_value(value)
            sleep(10)
        except (serial.SerialException, requests.RequestException) as e:
            print e
            sleep(10)

    hcho_client.close()


if __name__ == '__main__':
    main()

