import unittest
import visa
import pyvisa
import time
from queue import Queue
from datetime import datetime

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

    def test_device_has_gpib_resource(self):
        """Make sure the devices resource is a gpib resource."""
        self.assertIsInstance(self.itc01.resource,
                              pyvisa.resources.gpib.GPIBInstrument)

    def test_device_read_termination_character(self):
        "Make sure that the read termination character is a carriage return."
        self.assertEqual(self.itc01.resource.read_termination, '\r')

    def test_device_write_termination_character(self):
        "Make sure that the write termination character is a carriage return."
        self.assertEqual(self.itc01.resource.write_termination, '\r')

    def test_itc_identity(self):
        "Confirm the identity of the device"
        self.assertEqual(self.itc01.resource.query('V'), "ITC503")

    def test_read_tsorp(self):
        "Test reading from sorption pump sensor"
        self.assertEqual(self.itc01.get_tsorp(), 249.2)

    def test_read_t1k(self):
        "Test reading from sorption pump sensor"
        self.assertEqual(self.itc01.get_t1k(), 7.0)

    def test_read_the3(self):
        "Test reading from sorption pump sensor"
        self.assertEqual(self.itc01.get_the3(), 7.0)

    def test_set_heater_sensor(self):
        "Test if setting the heater sensor to the sorption pump sensor worked"
        self.itc01._set_heater_to_tsrop()
        self.assertTrue(self.itc01.heater_set)
        self.assertEqual(self.itc01.get_heater_sensor(), "TSorp")

    def test_set_tsorp_setpoint(self):
        "Set the temperature the sorption pump should go to."
        self.itc01.set_setpoint(30)
        self.assertEqual(self.itc01.get_setpoint(), 30.0)

    def test_turn_on_auto_heat(self):
        "Turn the auto heat control on."
        self.itc01.auto_heat_on()
        self.assertTrue(self.itc01.auto_heat)
        self.assertEqual(self.itc01.get_auto_heat_status(), "On")

    def test_turn_off_auto_heat(self):
        "Turn the auto heat control off."
        self.itc01.auto_heat_off()
        self.assertFalse(self.itc01.auto_heat)
        self.assertEqual(self.itc01.get_auto_heat_status(), "Off")

    def test_turn_auto_pid_on(self):
        "Turn on auto pid"
        self.itc01.auto_pid_on()
        self.assertEqual(self.itc01.get_auto_pid_status(), "On")

    def test_turn_auto_pid_off(self):
        "Turn of auto pid"
        self.itc01.auto_pid_off()
        self.assertEqual(self.itc01.get_auto_pid_status(), "Off")

    def test_set_heater_output(self):
        "Test setting heater output manually"
        self.itc01.set_heater_output(20)
        self.assertEqual(self.itc01.get_heater_output(), 20.0)

    def test_get_all_temperatures(self):
        "Test getting all temperatures from all three sensors"
        (datetimestamp, TSorp, THe3, T1K) = self.itc01.get_all_temperatures()
        self.assertIsInstance(datetimestamp, datetime)
        self.assertEqual(TSorp, 249.2)
        self.assertEqual(THe3, 7.000)
        self.assertEqual(T1K, 7.000)


class ThreadTestCase(unittest.TestCase):
    """Test the thread class."""

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

    def test_thread_start_stop(self):
        self.assertFalse(self.itc_thread.is_alive())
        self.itc_thread.start()
        self.assertTrue(self.itc_thread.is_alive())
        self.itc_thread.stop_thread()
        self.itc_thread.join()
        # time.sleep(0.01)
        self.assertFalse(self.itc_thread.is_alive())

    def test_number_elements_in_queue(self):
        wait = 5
        self.assertTrue(self.itc_queue.empty())
        self.itc_thread.start()
        time.sleep(wait*self.delay)
        self.itc_thread.stop_thread()
        self.itc_thread.join()
        i = 0
        while not self.itc_queue.empty():
            self.itc_queue.get()
            i += 1
        self.assertEqual(i, wait)


if __name__ == "__main__":
    unittest.main()
