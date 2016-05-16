#!/usr/bin/env python
# encoding: utf-8

from conf import config as conf
from serial import aio, SerialException
import struct
import json
import asyncio
import aiohttp
import requests
from time import ctime, sleep


class SerialProtocol(asyncio.Protocol):
    cloud = conf['cloud']
    def _request(self):
        req_data = (0xa5, 0x5a, 0x02, 0xc3, 0xaa)
        req_data = struct.pack("!5B", *req_data)
        self.transport.serial.write(req_data)

    @asyncio.coroutine
    def _upload_to_cloud(self, value):
        payload = [
            {
                "Name": "hcho",
                "Value": value
            }
        ]

        # lewei50 need header in lower char, but aiohttp can't
        #r = yield from aiohttp.post(
        #        self.cloud['url'],
        #        data=json.dumps(payload),
        #        headers=self.cloud['headers'])

        #resp = yield from r.json()
        #print("uploaded", str(resp))

        r = requests.post(
                self.cloud['url'],
                data=json.dumps(payload),
                headers=self.cloud['headers'])

        print("uploaded", r.text)

    def connection_made(self, transport):
        self.transport = transport
        print('port opened')
        transport.serial.rts = False
        self._request()

    def data_received(self, data):
        loop = asyncio.get_event_loop()

        resp_data = struct.unpack("!4xH4xHHx", data)
        print("AD: %s, %d mg/m3, %d ppm" % resp_data)

        asyncio.async(self._upload_to_cloud(resp_data[1]/100))

        loop.call_later(10, self._request)


    def connection_lost(self, exc):
        print('port closed')
        asyncio.get_event_loop().stop()

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    serial_conf = conf['hcho']
    coro = aio.create_serial_connection(
            loop,
            SerialProtocol,
            serial_conf['serial'],
            baudrate=serial_conf['baudrate'])

    loop.run_until_complete(coro)
    loop.run_forever()
    loop.close()


