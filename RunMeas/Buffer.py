#!/usr/bin/env python
# coding: utf-8

"""The Buffer Module.

"""

import time
from threading import Thread


class BufferCollectionThread(Thread):

    def __init__(self, name, q, delay=0.2):
        super(BufferCollectionThread, self).__init__()
        self.name = name
        self.q = q
        self.delay = delay
        self.stop = False

    def run(self):
        while not self.stop:
            vals = self.q.get()
            print(self.name, vals)

    def stop_thread(self):
        self.stop = True


class Buffer(object):

    def __init__(self, devices):
        if not isinstance(devices, list):
            raise TypeError("The devices passed to the manager needs to be a "
                            "list of tuples")
        if not isinstance(devices[0], tuple):
            raise TypeError("Each unit of the devices list need to be a tuple")

        self.devices = self._generate_device_dictionary(devices)
        self.collection_threads = self._generate_collection_threads()

    def _generate_device_dictionary(self, devices):
        d = {}

        for dev in devices:
            (dev_name, dev_obj, dev_thread) = dev
            d[dev_name] = {'device': dev_obj, 'thread': dev_thread}

        return d

    def _generate_collection_threads(self):
        col_ts = []
        for dev_name, dev_obj in self.devices.items():
            t = BufferCollectionThread(dev_name, dev_obj['thread'].q)
            col_ts.append(t)
        return col_ts

    def start_collection(self):
        # Make sure that all the device threads are started
        for k, v in self.devices.items():
            print('Starting device thread: {}'.format(k))
            if not v['thread'].is_alive():
                v['thread'].start()

        for t in self.collection_threads:
            print('Starting', t.name)
            t.start()

    def stop_collection(self):
        for t in self.collection_threads:
            print('Stopping', t.name)
            t.stop_thread()
            t.join()

        self._stop_all_devices()

    def _stop_all_devices(self):
        for k, v in self.devices.items():
            if v['thread'].is_alive():
                print('Stopping device thread: {}'.format(k))
                v['thread'].stop_thread()


def main():

    import visa
    from queue import Queue

    from ITCDevice import ITCDevice, ITCMeasurementThread

    DEVPATH = '/home/chris/Programming/github/RunMeas/test/devices.yaml'

    rm = visa.ResourceManager("{}@sim".format(DEVPATH))
    for resource in rm.list_resources():
        if "GPIB" in resource and '24' in resource:
            itc01 = ITCDevice(address=resource)
            itc01.set_resource(rm.open_resource)
        elif 'GPIB' in resource and '23' in resource:
            itc02 = ITCDevice(address=resource)
            itc02.set_resource(rm.open_resource)

    print(itc01.address)
    print(itc02.address)

    itc01_queue = Queue()
    itc02_queue = Queue()

    itc01_thread = ITCMeasurementThread(itc01, itc01_queue, delay=0.1)
    itc02_thread = ITCMeasurementThread(itc02, itc02_queue, delay=0.2)
    my_buffer = Buffer([('ITC1 Queue', itc01, itc01_thread, itc01_queue),
                        ('ITC2 Queue', itc02, itc02_thread, itc02_queue)])
    my_buffer.start_collection()
    time.sleep(1)
    my_buffer.stop_collection()
    my_buffer.stop_all_devices()

if __name__ == "__main__":
    main()
