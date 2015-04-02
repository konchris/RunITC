import unittest
import visa
import pyvisa

from RunITC.ITCDevice import ITCDevice

DEVPATH = '/home/chris/Programming/github/RunITC/test/devices.yaml'


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
        self.assertEqual(self.itc01.get_tsorp(), "R249.200")

    def test_read_t1k(self):
        "Test reading from sorption pump sensor"
        self.assertEqual(self.itc01.get_t1k(), "R7.000")

    def test_read_the3(self):
        "Test reading from sorption pump sensor"
        self.assertEqual(self.itc01.get_the3(), "R7.000")

    def test_set_heater_sensor(self):
        "Test if setting the heater sensor to the sorption pump sensor worked"
        self.itc01._set_heater_to_tsrop()
        self.assertTrue(self.itc01.heater_set)
        self.assertEqual(self.itc01.get_heater_sensor(), "1")

    def test_get_heater_sensor(self):
        "Test getting the heater sensor"
        self.assertEqual(self.itc01.get_heater_sensor(), "1")

    def test_set_tsorp_setpoint(self):
        "Set the temperature the sorption pump should go to."
        self.itc01.set_setpoint(30)
        self.assertEqual(self.itc01.get_setpoint(), "R30.000")

    def test_turn_on_auto_heat(self):
        "Turn the auto heat control on."
        self.itc01.auto_heat_on()
        self.assertTrue(self.itc01.auto_heat)
        self.assertEqual(self.itc01.get_auto_heat_status(), "1")

    def test_turn_off_auto_heat(self):
        "Turn the auto heat control off."
        self.itc01.auto_heat_off()
        self.assertFalse(self.itc01.auto_heat)
        self.assertEqual(self.itc01.get_auto_heat_status(), "0")

    def turn_on_auto_pid(self):
        self.itc01.auto_pid_on()
        self.assertTrue(self.itc01.auto_pid)
        self.assertEqual(self.itc01.get_auto_pid_status(), "1")

    def turn_off_auto_pid(self):
        self.itc01.auto_pid_off()
        self.assertFalse(self.itc01.auto_pid)
        self.assertEqual(self.itc01.get_auto_pid_status(), "0")

if __name__ == "__main__":
    unittest.main()
