#!/usr/bin/env python
# coding: utf-8

"""The Buffer Module.

"""

import time
from datetime import datetime
from threading import Thread
import numpy as np
import pandas as pd


class BufferCollectionThread(Thread):

    def __init__(self, name, q, dev_data, delay=0.2):
        super(BufferCollectionThread, self).__init__()
        self.name = name
        self.q = q
        self.delay = delay
        self.stop = False
        self.dev_data = dev_data

    def run(self):
        while not self.stop:
            vals = self.q.get()
            if type(vals[0]) is datetime:
                self.dev_data['timestamp'] = np.append(
                    self.dev_data['timestamp'], np.datetime64(vals[0]))
                for val in vals[1:]:
                    self.dev_data[val[0]] = np.append(
                        self.dev_data[val[0]], val[1])
            else:
                for val in vals:
                    print(val)
                # print(self.name, vals)

    def stop_thread(self):
        self.stop = True


class BufferReordThread(Thread):

    def __init__(self, name, q, dev_data, delay=0.2):
        super(BufferCollectionThread, self).__init__()
        self.name = name
        self.q = q
        self.delay = delay
        self.stop = False
        self.dev_data = dev_data

    def run(self):
        while not self.stop:
            vals = self.q.get()
            if type(vals[0]) is datetime:
                self.dev_data['timestamp'] = np.append(
                    self.dev_data['timestamp'], np.datetime64(vals[0]))
                for val in vals[1:]:
                    self.dev_data[val[0]] = np.append(
                        self.dev_data[val[0]], val[1])
            else:
                for val in vals:
                    print(val)
                # print(self.name, vals)

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
        self.data = self._generate_data_dictionary()
        self.collection_threads = self._generate_collection_threads()
        self.measurement_name = None

    def _generate_device_dictionary(self, devices):
        d = {}

        for dev in devices:
            (dev_name, dev_obj, dev_thread) = dev
            d[dev_name] = {'device': dev_obj, 'thread': dev_thread}

        return d

    def _generate_collection_threads(self):
        col_ts = []
        for dev_name, dev_obj in self.devices.items():
            t = BufferCollectionThread(dev_name, dev_obj['thread'].q,
                                       self.data[dev_name], delay=0.01)
            col_ts.append(t)
        return col_ts

    def _generate_data_dictionary(self):
        d = {}

        for dev_name in self.devices.keys():
            d[dev_name] = {}
            d[dev_name]['timestamp'] = np.array([], dtype='datetime64[us]')
            for chan_name in self.devices[dev_name]['thread'].chan_list:
                d[dev_name][chan_name] = np.array([])

        return d

    def start_collection(self):
        # Make sure that all the device threads are started
        for k, v in self.devices.items():
            print('Starting device thread: {}'.format(k))
            if not v['thread'].is_alive():
                v['thread'].start()

        # Start the collection threads
        for t in self.collection_threads:
            print('Starting collection thread for', t.name)
            t.start()

    def stop_collection(self):
        for t in self.collection_threads:
            print('Stopping collection thread for', t.name)
            t.stop_thread()
            t.join()

        self._stop_all_devices()

    def _stop_all_devices(self):
        for k, v in self.devices.items():
            if v['thread'].is_alive():
                print('Stopping device thread: {}'.format(k))
                v['thread'].stop_thread()

    def start_recording(self):
        pass

    def stop_recording(self):
        pass


def main():

    import os
    import visa

    from ITCDevice import ITCDevice, ITCMeasurementThread

    DEVPATH = os.path.join(os.getcwd(), 'test', 'devices.yaml')
    # DEVPATH = '/home/chris/Programming/github/RunMeas/test/devices.yaml'

    rm = visa.ResourceManager("{}@sim".format(DEVPATH))
    # rm = visa.ResourceManager()
    for resource in rm.list_resources():
        if "GPIB" in resource and '24' in resource:
            itc01 = ITCDevice(address=resource)
            itc01.set_resource(rm.open_resource)
        # elif 'GPIB' in resource and '23' in resource:
        #     itc02 = ITCDevice(address=resource)
        #     itc02.set_resource(rm.open_resource)

    print(itc01.address)
    # print(itc02.address)

    itc01_thread = ITCMeasurementThread(itc01, ['TSorp', 'THe3', 'T1K'],
                                        delay=0.1)
    # itc02_thread = ITCMeasurementThread(itc02, ['TSorp', 'THe3', 'T1K'],
    #                                     delay=0.2)
    my_buffer = Buffer([('ITC1', itc01, itc01_thread)])  # ,
    #                   ('ITC2', itc02, itc02_thread)])
    my_buffer.start_collection()
    time.sleep(2)
    my_buffer.stop_collection()

    df = {}
    for k, v in my_buffer.data.items():
        df[k] = pd.DataFrame(data=v)
        # times = df[k]['timestamp']
        # diff = [times[i+1] - times[i] for i in np.arange(times.count()-1)]
        # print(diff, diff[0])
        df[k] = df[k].set_index('timestamp')
        print(df[k])
        # print(df[k].index)

if __name__ == "__main__":
    main()
