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
    """The AH Driver Object

    This provides high level access to some of the functionality of the AH2550A
    capacitive bridge.
    The device is directly accessable via the resource attribute.

    Parameters
    ----------
    address : str
        The visa address of the ITC device.
        Example: "GPIB1::24::INSTR"
    read_term : str, optional
        The reading terminatin character of the device
        DEFUALT: "\n"

    Attributes
    ----------
    resource : pyvisa.resources.gpib.GPIBInstrument
        The instance of the gpib instrument giving direct access to the device.
    address : str
        The visa address of the device
        Example: "GPIB1::24::INSTR"
    read_term : str
        The reading termination character of the device
    write_term : str
        The writing termination character of the device

    Methods
    -------
    set_resource(resource=, resource_address)

    """

    def __init__(self, address, read_term="\n",
                 write_term="\n"):
        super(AHDevice, self).__init__()
        self.resource = None
        self.address = address
        self.read_term = read_term
        self.write_term = write_term

    def set_resource(self, resource):
        """Set the VISA resource for the device.

        The sets the VISA resources as the 'resource' attribute of the object.

        Parameters
        ----------
        resource : method
            This is the method from
            pyvisa.highlevel.ResourceManager.open_resource() and it will take
            the subsequent address attribute of the class as a parameter.

        """
        self.resource = resource(self.address,
                                 read_termination=self.read_term,
                                 write_termination=self.write_term)

    def get_average(self):
        """Get the approximate time used to make a measurement.

        Returns
        -------
        tuple : (str, int)
            A tupe with the name of the value ('AVERAGE') and the value.

        """
        aveg_rsp = self.resource.query("SH AV")
        aveg_exp = int(aveg_rsp.split('=')[-1])
        print(aveg_exp, type(aveg_exp))
        return('AVERAGE', aveg_exp)

    def set_average(self, aveg_exp):
        """Set the approximate time usedto make a measurement

        Parameters
        ----------
        aveg_exp : int
            The time averaging exponent

        """
        if not isinstance(aveg_exp, int):
            raise TypeError("The averaging exponent provided needs to be an "
                            "int.")
        self.resource.write("AV {:d}".format(aveg_exp))

    def start_continuous(self):
        "Initiate measurements which are taken continuously"
        self.resource.write('CO ON')

    def stop_continuous(self):
        "Stop measurements which are taken continuously"
        self.resource.write('CO OF')

    def get_values(self):
        "Hi"


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
