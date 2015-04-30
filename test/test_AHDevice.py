import os
import unittest
import visa
import pyvisa
import time
from queue import Queue
from datetime import datetime

from RunMeas.AHDevice import AHDevice, AHMeasurementThread

DEVPATH = os.path.join(os.getcwd(), 'test', 'devices.yaml')
# DEVPATH = '/home/chris/Programming/github/RunMeas/test/devices.yaml'

class DeviceTestCase(unittest.TestCase):
    """Test the device class."""

    def setUp(self):
        rm = visa.ResourceManager('{}@sim'.format(DEVPATH))
        for resource_address in rm.list_resources():
            if 'GPIB' in resource_address and '28' in resource_address:
                self.ah = AHDevice(resource_address)
                self.ah.set_resource(rm.open_resource)

    def test_create_ah_device(self):
        rm = visa.ResourceManager('{}@sim'.format(DEVPATH))
        for resource_address in rm.list_resources():
            print(resource_address)
            if 'GPIB' in resource_address and '28' in resource_address:
                ah = AHDevice(resource_address)
                ah.set_resource(rm.open_resource)
        self.assertIsInstance(ah.resource,
                              pyvisa.resources.gpib.GPIBInstrument)

    def test_device_has_gpib_resource(self):
        """Make sure the devices resource is a gpib resource."""
        self.assertIsInstance(self.ah.resource,
                              pyvisa.resources.gpib.GPIBInstrument)

    def test_device_read_termination_character(self):
        "Make sure that the read termination character is a line feed."
        self.assertEqual(self.ah.resource.read_termination, '\n')

    def test_device_write_termination_character(self):
        "Make sure that the write termination character is a line feed."
        self.assertEqual(self.ah.resource.write_termination, '\n')

    def test_ah_identity(self):
        "Confirm the identity of the device"
        self.assertEqual(self.ah.resource.query('*IDN?'), "AH2550A")

    def test_read_average_exponent(self):
        "Test reading the average exponent"
        self.assertEqual(self.ah.get_average(), ('AVERAGE', 4))

    def test_set_average_exponent(self):
        "Test setting the averaging exponent"
        self.ah.set_average(5)
        # The following 'read' command is to trick the PyVISA-sim device,
        # which does not allow for write commands without a paired read
        # command.
        self.ah.resource.read()
        self.assertEqual(self.ah.get_average(), ('AVERAGE', 5))

    def test_start_continuous(self):
        "Test starting continuous measurements"
        self.ah.start_continuous()

    def test_stop_continuous(self):
        "Test starting continuous measurements"
        self.ah.stop_continuous()
        
