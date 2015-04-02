import unittest
import visa

from RunITC.ITCDevice import ITCDevice


class DeviceTestCase(unittest.TestCase):
    """Test the device class."""

    def setUp(self):
        self.rm = visa.ResourceManager('@sim')
        itc01 = ITCDevice()
        for resource in self.rm.list_resources():
            if 'GPIB' in resource:
                itc01.resource = self.rm(resource)

    def test_device_class_is_present(self):
        """If something something."""
        self.assertEqual(True, True)

if __name__ == "__main__":
    unittest.main()
