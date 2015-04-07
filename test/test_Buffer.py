import unittest

import visa
import time
from queue import Queue

from RunMeas.Buffer import Buffer
from RunMeas.ITCDevice import ITCDevice, ITCMeasurementThread

DEVPATH = '/home/chris/Programming/github/RunMeas/test/devices.yaml'


class DeviceTestCase(unittest.TestCase):
    """Test the device class."""

    def setUp(self):
        self.rm = visa.ResourceManager('{}@sim'.format(DEVPATH))
        self.itc01 = ITCDevice()
        for resource_address in self.rm.list_resources():
            if 'GPIB' in resource_address:
                self.itc01.set_resource(self.rm.open_resource)

        self.itc_queue = Queue()

        self.delay = 0.1

        self.itc_thread = ITCMeasurementThread(self.itc01, self.itc_queue,
                                               delay=self.delay)
        self.buffer = Buffer({'ITC Queue': self.itc_queue})

        self.itc_thread.start()

    def test_buffer_gets_queue(self):
        """If something something."""
        for k, v in self.buffer.queues.items():
            self.assertIsInstance(v, Queue)

    def test_buffer_has_test_queue(self):
        self.assertTrue('ITC Queue' in self.buffer.queues)

    def test_buffer_start_stop_queue(self):
        self.buffer.start_collection()
        time.sleep(0.5)
        self.Buffer.stop()

    def tearDown(self):
        self.itc_thread.stop_thread()

if __name__ == "__main__":
    unittest.main()
