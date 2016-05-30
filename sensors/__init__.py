#!/usr/bin/env python
# encoding: utf-8


from hcho import Sensor as hcho
from temperature import Sensor as temp


SENSORS = {
    "hcho": hcho, 
    "temperature":temp
}