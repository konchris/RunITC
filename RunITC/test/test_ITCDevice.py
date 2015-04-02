import unittest

from RunITC.ITCDevice import ITCDevice


class MockVisaInstrument(object):

    def __init__(self):
        self.session = 1
        self.timeout = 1000
        self.read_termination = '\r'
        self.write_termination = '\r'

    def __str__(self):
        return "<GPIBInstrument('GPIB::MOCK')>"

    def query_ascii_values(self):
        pass

    def query_binary_values(self):
        pass

    def query_values(self):
        pass

    def write_ascii_values(self):
        pass

    def write_binary_values(self):
        pass

    def write(self):
        pass

    def read_raw(self):
        pass

    def wait_for_srq(self):
        pass

    def query(self):
        pass

    def close(self):
        pass


class DeviceTestCase(unittest.TestCase):
    """Test the device class."""

    def test_device_class_is_present(self):
        """If something something."""
        self.assertEqual(True, True)

if __name__ == "__main__":
    unittest.main()
