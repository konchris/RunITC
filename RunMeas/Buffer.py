#!/usr/bin/env python
# coding: utf-8

"""The Buffer Module.

"""

import os
import sys
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


class BufferRecordThread(Thread):

    def __init__(self, dev_data, measurement_name, data_folder, delay=0.1):
        super(BufferRecordThread, self).__init__()
        self.delay = delay
        self.stop = False
        self.dev_data = dev_data
        self.meas_name = measurement_name
        self.data_folder = data_folder
        self.start_time = datetime.now().strftime("%Y-%m-%dT%H-%M-%S")
        # print(self.data_folder, self.start_time, self.meas_name)
        self.file_name = self._generate_file_name()

    def _generate_file_name(self):
        basename = '_'.join((self.start_time, self.meas_name))
        fullname = basename + '.h5'
        assert type(self.data_folder) is str, 'Data folder not string!?'
        assert type(fullname) is str, 'Full name not string!?'
        fullpath = os.path.join(self.data_folder, fullname)
        return fullpath

    def run(self):

        while not self.stop:
            # Sometime the recording thread pulls the data before it has
            # all been added to the data dictionary. This raises a
            # ValueError which is caught here.
            try:
                df = {}
                for k, v in self.dev_data.items():
                    key = 'raw/'+k
                    df[k] = pd.DataFrame(data=v)
                    df[k] = df[k].set_index('timestamp')
                    df[k].to_hdf(self.file_name, key, format='table')
            except ValueError:
                pass
            time.sleep(self.delay)

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
        self.record_thread = None
        self.data_folder = os.path.join(os.getcwd(), 'temp_data')

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
            d[dev_name]['timestamp'] = np.array([], dtype='datetime64[ns]')
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
        assert type(self.data_folder) is not None
        self.record_thread = BufferRecordThread(self.data, 'Test_Measurement',
                                                self.data_folder)
        self.record_thread.start()

    def stop_recording(self):
        self.record_thread.stop_thread()
        self.record_thread.join()

    def set_measurement_name(self, measurement_name):
        assert type(measurement_name) is str, ("The measurement name given is "
                                               "not a string")

        self.measurement_name = measurement_name

    def set_data_folder(self, data_folder):
        assert type(data_folder) is str, ("The data folder given is "
                                          "not a string")

        self.data_folder = data_folder


def main():

    import os
    import visa

    from ITCDevice import ITCDevice, ITCMeasurementThread

    DEVPATH = os.path.join(os.getcwd(), 'test', 'devices.yaml')
    # DEVPATH = '/home/chris/Programming/github/RunMeas/test/devices.yaml'

    if sys.platform == 'win32':
        rm = visa.ResourceManager()
    elif sys.platform == 'linux':
        rm = visa.ResourceManager("{}@sim".format(DEVPATH))
    for resource in rm.list_resources():
        if "GPIB" in resource and '24' in resource:
            itc01 = ITCDevice(address=resource)
            itc01.set_resource(rm.open_resource)

    print(itc01.address)

    itc01_thread = ITCMeasurementThread(itc01, ['TSorp', 'THe3', 'T1K'],
                                        delay=0.1)
    my_buffer = Buffer([('ITC1', itc01, itc01_thread)])

    my_buffer.set_data_folder(os.path.join(os.getcwd(), 'temp_data'))
    # print(my_buffer.data_folder)
    my_buffer.start_collection()
    my_buffer.start_recording()
    time.sleep(0.5*60*60)
    my_buffer.stop_recording()
    my_buffer.stop_collection()

    df = {}
    for k, v in my_buffer.data.items():
        # print('raw/'+k)
        df[k] = pd.DataFrame(data=v)
        # times = df[k]['timestamp']
        # diff = [times[i+1] - times[i] for i in np.arange(times.count()-1)]
        # print(diff, diff[0])
        # df[k] = df[k].set_index('timestamp')
        # print(df[k].index)
        print(df[k]['timestamp'].count)

if __name__ == "__main__":
    main()
