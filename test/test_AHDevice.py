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
