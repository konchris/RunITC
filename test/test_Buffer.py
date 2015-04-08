import unittest

import time
from datetime import datetime
from queue import Queue
from threading import Thread

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
        return (now, 42)


class MockDeviceMeasurementThread(Thread):

    def __init__(self, device, q, delay=0.1):
        super(MockDeviceMeasurementThread, self).__init__()
        self.stop = False
        self.device = device
        self.q = q
        self.delay = delay

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

        self.itc01_queue = Queue()

        self.itc01_thread = MockDeviceMeasurementThread(self.itc01,
                                                        self.itc01_queue,
                                                        delay=self.delay)

        self.itc02 = MockDevice('2')
        self.itc02.set_resource(MockResource)

        self.itc02_queue = Queue()

        self.itc02_thread = MockDeviceMeasurementThread(self.itc02,
                                                        self.itc02_queue,
                                                        delay=self.delay)

        self.buffer = Buffer([('Mock Device 01', self.itc01, self.itc01_thread,
                               self.itc01_queue),
                              ('Mock Device 02', self.itc02, self.itc02_thread,
                               self.itc02_queue)])

        self.itc01_thread.start()
        self.itc02_thread.start()

    def test_buffer_init_creates_devices_dictionary(self):
        delay = 0.01

        itc01 = MockDevice('1')
        itc01.set_resource(MockResource)

        itc01_queue = Queue()

        itc01_thread = MockDeviceMeasurementThread(itc01,
                                                   itc01_queue,
                                                   delay=delay)

        my_buffer = Buffer([('Mock Device 01', itc01, itc01_thread,
                             itc01_queue)
                            ])
        self.assertIsInstance(my_buffer.devices, dict)
        self.assertIn('Mock Device 01', my_buffer.devices)

        self.assertIsInstance(my_buffer.devices['Mock Device 01'], dict)

        self.assertIn('queue', my_buffer.devices['Mock Device 01'])
        self.assertIsInstance(my_buffer.devices['Mock Device 01']['queue'],
                              Queue)

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

        itc01_queue = Queue()

        itc01_thread = MockDeviceMeasurementThread(itc01,
                                                   itc01_queue,
                                                   delay=delay)

        my_buffer = Buffer([('Mock Device 01', itc01, itc01_thread,
                             itc01_queue)
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
        self.assertTrue('queue' in
                        self.buffer.devices['Mock Device 01'].keys())
        self.assertTrue(self.buffer.devices['Mock Device 01']['queue']
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
        self.assertTrue(self.itc01_thread.is_alive())
        self.buffer.stop_all_devices()
        for dev_name, dev_dict in self.buffer.devices.items():
            dev_dict['thread'].join()
            self.assertFalse(dev_dict['thread'].is_alive())

    def tearDown(self):
        if self.itc01_thread.is_alive():
            self.itc01_thread.stop_thread()
        if self.itc02_thread.is_alive():
            self.itc02_thread.stop_thread()

if __name__ == "__main__":
    unittest.main()
