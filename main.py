#!/usr/bin/env python
# encoding: utf-8

from conf import config as conf
import serial
import struct
from time import sleep
import requests
import json

headers = {"userkey": "a34f724c03574b1d8eeca4185bb854a2"}
url = "http://www.lewei50.com/api/V1/gateway/UpdateSensors/01"

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
    return resp_data[1]/100.0


def upload_HCHO_value(value):
    payload = [
        {
            "Name": "hcho",
            "Value": value
        }
    ]
    r = requests.post(url, data=json.dumps(payload), headers=headers)
    print r.text


def main():
    hcho_client = init_HCHO_sensor()
    request_HCHO_value(hcho_client)
    while 1:
        hcho_value = request_HCHO_value(hcho_client)
        print hcho_value
        upload_HCHO_value(hcho_value)
        sleep(10)
    hcho_client.close()


if __name__ == '__main__':
    main()
    