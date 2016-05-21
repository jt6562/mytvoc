#!/usr/bin/env python
# encoding: utf-8


class RollingMean(list):
    def __init__(self, window_size, *args):
        super(RollingMean, self).__init__(*args)
        assert(window_size > 0)
        self._windows_size = window_size

    def append(self, new_obj):
        print self.__len__(), self._windows_size
        if self.__len__() >= self._windows_size:
            self.pop(0)
        super(RollingMean, self).append(new_obj*1.0)

    def get_mean(self):
        return sum(self) / self.__len__()


# Unit Test
if __name__ == '__main__':
    r = RollingMean(5)
    r.append(1)

    r.append(5)
    print r.get_mean()

    r.append(5)
    print r.get_mean()

    r.append(5)
    print r.get_mean()

    r.append(5)
    print r.get_mean()

    r.append(5)
    print r.get_mean()

