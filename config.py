#!/usr/bin/env python
# encoding: utf-8

config = {
    "cloud": {
        "lewei": {
            "enable": True,
            "url" :"http://www.lewei50.com/api/V1/gateway/UpdateSensors/01",
            "headers" : {"userkey": "a34f724c03574b1d8eeca4185bb854a2"}
        }
    },
    "sensors": {
        "hcho": {
            "enable": True,
            "device": {
                "name": "hcho",
                "serial": "/dev/ttyUSB0",
                "baudrate": 9600
            }
        },
        "temperature": {
            "enable": True,
            "device": {
                "name": "temp",
            }
        }
    }
}
