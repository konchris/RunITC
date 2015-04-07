#!/usr/bin/env python
# coding: utf-8

"""The Buffer Module.

"""

import time
from threading import Thread


class Buffer(object):

    def __init__(self, devices):
        self.devices = self._generate_device_dictionary(devices)

    def _generate_device_dictionary(self, devices):
        if not isinstance(devices, list):
            raise TypeError("The devices passed to the manager needs to be a "
                            "list of tuples")
        if not isinstance(devices[0], tuple):
            raise TypeError("Each unit of the devices list need to be a tuple")

        d = {}

    def start_collection(self):
        for k, v in self.queues.items():
            print('Starting queue: {}'.format(k))

        while not self.stop:
            print('Stop:', self.stop)
            for k, v in self.queues.items():
                print('Queue: {qname}, Value: {val}'.format(qname=k,
                                                            val=v.get()))

        for k, v in self.queues.items():
            print('Stopping queue: {}'.format(k))
            v.task_done()

    def stop_thread(self):
        self.stop = True


class BufferCollectionThread(Thread):
    pass


def main():

    import visa
    from threading import Thread
    from queue import Queue

    from ITCDevice import ITCDevice, ITCMeasurementThread

    DEVPATH = '/home/chris/Programming/github/RunMeas/test/devices.yaml'

    rm = visa.ResourceManager("{}@sim".format(DEVPATH))
    itc01 = ITCDevice()
    for resource in rm.list_resources():
        if "GPIB" in resource:
            itc01.set_resource(rm.open_resource)

    itc_queue = Queue()
    my_buffer = Buffer({'ITC Queue': itc_queue})

    itc_thread = ITCMeasurementThread(itc01, itc_queue, delay=0.1)
    print('starting thread')
    itc_thread.start()
    t = Thread(target=my_buffer.start_collection)
    t.start()
    print('Is t alive, start?:', t.is_alive())

    time.sleep(1)
    my_buffer.stop_thread()
    itc_thread.stop_thread()
    t.join()
    print('Is t alive after stop?', t.is_alive())
    print('Exiting')


if __name__ == "__main__":
    main()
