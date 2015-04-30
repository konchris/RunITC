#!/usr/bin/env python
# coding: utf-8

"""The Andeen Hagerling Module

This module contains the driver for controlling the Andeen Hagerling
Ultra-Precision 1kHz Capacitance Bridge.
This uses PyVISA and creates a resource attribute of this class, which provides
access to the device.
Additionally included in this module is the main measurement thread which
collects the data from the measurement input.

"""

import os
import visa
import time
from datetime import datetime
from threading import Thread
from queue import Queue


class AHDevice(object):
    """The AH Driver Object"""
    pass


class AHMeasurementThread(Thread):
    """Thread for running continuous retrieval of data from the AH."""
    pass


def main():

    DEVPATH = os.path.join(os.getcwd(), 'test', 'devices.yaml')

    rm = visa.ResourceManager("{}@sim".format(DEVPATH))
    for resource_address in rm.list_resources():
        print(resource_address)

if __name__ == "__main__":
    main()
