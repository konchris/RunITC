import unittest

from RunITC import runitc


class DeviceTestCase(unittest.TestCase):
    """Test the device class."""

    def test_device_class_is_present(self):
        """If something something."""
        self.assertEqual(True, True)

if __name__ == "__main__":
    unittest.main()
