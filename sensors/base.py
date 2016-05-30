#!/usr/bin/env python
# encoding: utf-8

from concurrent.futures import ThreadPoolExecutor
from tornado import gen, ioloop, queues

class SensorBase(object):

    def __init__(self, callback):
        self.callback = callback
        self.executor = ThreadPoolExecutor(1)
        self.queue = queues.Queue()

    @gen.coroutine
    def run(self):
        while 1:
            yield self.queue.get()
            try:
                value = yield self.get_value()
                yield self.callback(self.name, value)
            finally:
                self.queue.task_done()
                print '<<<<<done', self.name, self.queue