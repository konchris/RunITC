import unittest

import time
from datetime import datetime
from queue import Queue
from threading import Thread
import numpy as np
from pandas import DataFrame

from RunMeas.Buffer import Buffer


class MockResource(object):

    def __init__(self, address):
        self.address = address


class MockDevice(object):

    def __init__(self, address):
        self.resource = None
        self.address = address

    def set_resource(self, resource):
        self.resource = resource(self.address)

    def get_values(self):
        now = datetime.now()
        return (now, ('value', 42))


class MockDeviceMeasurementThread(Thread):

    def __init__(self, device, chan_list, delay=0.1):
        super(MockDeviceMeasurementThread, self).__init__()
        self.stop = False
        self.device = device
        self.q = Queue()
        self.delay = delay
        self.chan_list = chan_list

    def run(self):
        while not self.stop:
            time.sleep(self.delay)
            meas_values = self.device.get_values()
            self.q.put(meas_values)

    def stop_thread(self):
        self.stop = True


class BufferTestCase(unittest.TestCase):
    """Test the device class."""

    def setUp(self):
        self.delay = 0.01

        self.itc01 = MockDevice('1')
        self.itc01.set_resource(MockResource)

        self.itc01_thread = MockDeviceMeasurementThread(self.itc01,
                                                        ['value'],
                                                        delay=self.delay)

        self.itc02 = MockDevice('2')
        self.itc02.set_resource(MockResource)

        self.itc02_thread = MockDeviceMeasurementThread(self.itc02,
                                                        ['value'],
                                                        delay=self.delay)

        self.buffer = Buffer([('Mock Device 01', self.itc01,
                               self.itc01_thread),
                              ('Mock Device 02', self.itc02,
                               self.itc02_thread)])

    def test_buffer_init_creates_devices_dictionary(self):
        delay = 0.01

        itc01 = MockDevice('1')
        itc01.set_resource(MockResource)

        itc01_thread = MockDeviceMeasurementThread(itc01,
                                                   ['value'],
                                                   delay=delay)

        my_buffer = Buffer([('Mock Device 01', itc01, itc01_thread)
                            ])
        self.assertIsInstance(my_buffer.devices, dict)
        self.assertIn('Mock Device 01', my_buffer.devices)

        self.assertIsInstance(my_buffer.devices['Mock Device 01'], dict)

        self.assertIn('device', my_buffer.devices['Mock Device 01'])
        self.assertIsInstance(my_buffer.devices['Mock Device 01']['device'],
                              object)

        self.assertIn('thread', my_buffer.devices['Mock Device 01'])
        self.assertIsInstance(my_buffer.devices['Mock Device 01']['thread'],
                              Thread)

    def test_buffer_init_exception_no_list(self):
        with self.assertRaises(TypeError):
            Buffer('Hello World')

    def test_buffer_init_exception_no_tuples(self):
        with self.assertRaises(TypeError):
            Buffer(['0123', '4567'])

    def test_buffer_init_creates_collection_threads(self):
        delay = 0.01

        itc01 = MockDevice('1')
        itc01.set_resource(MockResource)

        itc01_thread = MockDeviceMeasurementThread(itc01,
                                                   ['value'],
                                                   delay=delay)

        my_buffer = Buffer([('Mock Device 01', itc01, itc01_thread)
                            ])
        self.assertIsInstance(my_buffer.collection_threads, list)
        self.assertTrue(my_buffer.collection_threads)

    def test_buffer_has_mock_device(self):
        self.assertTrue('Mock Device 01' in self.buffer.devices.keys())
        self.assertTrue('Mock Device 02' in self.buffer.devices.keys())
        self.assertTrue('device' in
                        self.buffer.devices['Mock Device 01'].keys())
        self.assertTrue(self.buffer.devices['Mock Device 01']['device']
                        is not None)
        self.assertTrue('thread' in
                        self.buffer.devices['Mock Device 01'].keys())
        self.assertTrue(self.buffer.devices['Mock Device 01']['thread']
                        is not None)

    def test_buffer_start_stop_queue(self):
        self.buffer.start_collection()
        time.sleep(0.1)
        self.buffer.stop_collection()

    def test_buffer_stop_all_devices(self):
        self.itc01_thread.start()
        self.itc02_thread.start()
        self.assertTrue(self.itc01_thread.is_alive())
        self.buffer._stop_all_devices()
        for dev_name, dev_dict in self.buffer.devices.items():
            dev_dict['thread'].join()
            self.assertFalse(dev_dict['thread'].is_alive())
        self.assertFalse(self.itc01_thread.is_alive())

    def test_buffer_data_structure(self):
        self.buffer.start_collection()
        time.sleep(0.1)
        self.buffer.stop_collection()
        self.assertIsInstance(self.buffer.data, dict)
        self.assertIsInstance(self.buffer.data['Mock Device 01'], dict)
        self.assertIn('timestamp', self.buffer.data['Mock Device 01'])
        self.assertIsInstance(self.buffer.data['Mock Device 01']['timestamp'],
                              np.ndarray)
        self.assertIsInstance(self.buffer.data['Mock Device 01']
                              ['timestamp'][0],
                              np.datetime64)
        self.assertIn('value', self.buffer.data['Mock Device 01'])
        self.assertIsInstance(self.buffer.data['Mock Device 01']['value'],
                              np.ndarray)

if __name__ == "__main__":
    unittest.main()
