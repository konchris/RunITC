#!/usr/bin/env python
# coding: utf-8

"""The ITC Module.

This module contains the driver for controlling the Oxford ITC503 temperature
controller.
This uses PyVISA and creates a resource attribute of this class, which provides
access to the device.
Additionally included in this module is the main measurement thread which
collects the data from all three temperature sensors.

"""

import os
import visa
import time
from datetime import datetime
from threading import Thread
from queue import Queue

SENSORS = {"1": "TSorp", "2": "THe3", "3": "T1K"}


class ITCDevice(object):
    """The ITC Driver Object

    This provided high level access to much of the functionality of the ITC503
    temperature controller.
    The device is directly accessable via the resource attribute.

    Parameters
    ----------
    address : str
        The visa address of the ITC device.
        Example: "GPIB1::24::INSTR"
    read_term : str, optional
        The reading terminatin character of the device
        DEFUALT: "\r"

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
    auto_heat : bool
        Whether the auto heating option is turned on (i.e. the feedback control
        via the pre-programmed PID values already stored in the device)
    auto_pid : bool
        Whether the auto PID option is turned on. This uses pre-programmed PID
        tables stored in the device.

    Methods
    -------
    set_resource(resource=, resource_address)
    get_tsorp
    get_the3
    get_t1k
    get_heater_sensor
    set_setpoint(setpoint)
    get_setpoint
    auto_heat_on
    auto_heat_off
    get_auto_heat_status
    auto_pid_on
    auto_pid_off
    get_auto_pid_status
    set_heater_output(output)
    get_heater_output
    get_all_temperatures

    """

    def __init__(self, address, read_term="\r",
                 write_term="\r"):
        super(ITCDevice, self).__init__()
        self.resource = None
        self.address = address
        self.read_term = read_term
        self.write_term = write_term
        self.heater_set = False
        self.auto_heat = False
        self.auto_pid = False

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

    def get_tsorp(self):
        """Get the temperature at the sorption pump.

        Returns
        -------
        tuple : (str, float)
            A tuple with the name of the value ('TSorp') and the value in
            Kelvin

        """
        tsorp_str = self.resource.query("R1")
        tsorp_flt = float(tsorp_str.lstrip("R"))
        return ('TSorp', tsorp_flt)

    def get_the3(self):
        """Get the temperature at the helium-3 pot."

        Returns
        -------
        tuple : (str, float)
            A tuple with the name of the value ('THe3') and the value in
            Kelvin.

        """
        the3_str = self.resource.query("R2")
        the3_flt = float(the3_str.lstrip("R"))
        return ('THe3', the3_flt)

    def get_t1k(self):
        """Get the temperature at the 1K pot.

        Returns
        -------
        tuple : (str, float)
            A tuple with the name of the value ('T1K') and the value in Kelvin.

        """
        t1k_str = self.resource.query("R3")
        t1k_flt = float(t1k_str.lstrip("R"))
        return ('T1K', t1k_flt)

    def _set_heater_to_tsrop(self):
        """Set the heater to the sorption pump.

        This sets the sensor to be used during automatic control to the
        helium-3 sorption pump sensor.

        """
        self.resource.query("H1")
        self.heater_set = True

    def get_heater_sensor(self):
        """Get the heater sensor

        Returns
        -------
        heater_sensor : str
            The name of the temperature sensor that is being used for automatic
            control.

        """
        status_byte = self.resource.query("X")
        if status_byte == 'ERROR':
            status_byte = self.resource.query("XH")
        sensor_nr = status_byte.split("H")[-1][0]
        return SENSORS[sensor_nr]

    def set_setpoint(self, setpoint):
        """Set the set point temperature of the sorption pump.

        Parameters
        ----------
        setpoint : float
            The set point temperature in Kelvin for the automatic control

        """
        if not isinstance(setpoint, (float, int)):
            raise TypeError("The setpoint provided needs to be a float "
                            "or an int.")
        if not self.heater_set:
            self._set_heater_to_tsrop()
        self.resource.query("T{:.3f}".format(setpoint))

    def get_setpoint(self):
        """Get the setpoint of the sorption pump heater.

        Returns
        -------
        tuple : (str, float)
            A tuple with the name of the value being returned ('Setpoint') and
            the value in Kelvin

        """
        setpoint_str = self.resource.query("R0")
        setpoint_flt = float(setpoint_str.lstrip("R"))
        return ('Setpoint', setpoint_flt)

    def auto_heat_on(self):
        "Turn on the auto heat control."
        self.resource.query("A1")
        self.auto_heat = True

    def auto_heat_off(self):
        "Turn on the auto heat control."
        self.resource.query("A0")
        self.auto_heat = False

    def get_auto_heat_status(self):
        """Get the status of autoheating

        Returns
        -------
        tuple : (str, str)
            The first string is 'AutoHeat', i.e. the name of the value, and the
            second is either 'On' for automatic control on or 'Off'.

        """
        sensor_nr = self.resource.query("X")
        if sensor_nr == 'ERROR':
            sensor_nr = self.resource.query("XA")

        sensor_nr = sensor_nr.split("A")[-1][0]

        if sensor_nr == "0":
            return ('AutoHeat', "Off")
        elif sensor_nr == "1":
            return ('AutoHeat', "On")

    def auto_pid_on(self):
        "Turn on the auto pid for temperature control"
        self.resource.query("L1")
        self.auto_pid = True

    def auto_pid_off(self):
        "Turn off the auto pid for temperature control"
        self.resource.query("L0")
        self.auto_pid = False

    def get_auto_pid_status(self):
        """Get the status of the auto pid setting

        Returns
        -------
        tuple : (str, str)
            The first string is 'AutoPID', i.e. the name of the value, and the
            second is either 'On' for automatic control on or 'Off'.

        """
        status_byte = self.resource.query("X")
        if status_byte == 'ERROR':
            status_byte = self.resource.query("XL")

        sensor_nr = status_byte.split("L")[-1][0]

        if sensor_nr == "0":
            return ('AutoPID', "Off")
        elif sensor_nr == "1":
            return ('AutoPID', "On")

    def set_heater_output(self, output):
        """Set the heater output manually

        Parameters
        ----------
        output : float
            The desired output of the heater in %

        """
        if not isinstance(output, (float, int)):
            raise TypeError("The output provided needs to be a float "
                            "or an int.")
        self.resource.query("O{:.1f}".format(output))

    def get_heater_output(self):
        """Get the current heater output

        Returns
        -------
        tuple : (str, float)
            The string is 'HeaterOutput', i.e. the name of the value, and the
            value returned is a float representing the heater output in %.

        """
        heater_output_str = self.resource.query("R5")
        heater_output_flt = float(heater_output_str.lstrip("R"))
        return ('HeaterOutput', heater_output_flt)

    def get_all_temperatures(self):
        """Get all temperatures from all three sensors.

        Returns
        -------
        all_temperatures : tuple
            This tuple contains the following:
            1. Current datetime stamp
            2. Reading from the sorption pump sensor
            2. Reading from the helium-3 sensor
            4. Reading from the 1K pot sensor

        """
        now = datetime.now()
        TSorp = self.get_tsorp()
        THe3 = self.get_the3()
        T1K = self.get_t1k()
        return (now, TSorp, THe3, T1K)


class ITCMeasurementThread(Thread):
    """Thread for running continuous retrieval of data from the ITC.

    Once started, this thread will continuously and periodically ask the ITC
    for data, with a period defined by the 'delay' parameter. The thread can be
    stopped by calling its stop_thread method, which sets the stop attribute
    to true.

    Parameters
    ----------
    device : ITCDevice
        The instance of the device that shall be queried for data.
    chan_list : list
        A list of strings giving name to the channels that will be queried.
        This is necessary so that the collection buffer can setup its data
        before collection starts.
        The order does not matter.
    delay : float, optional
        The delay, in seconds, between queries to the device.
        DEFAULT: 0.2 s

    Attributes
    ----------
    stop : boolean
        The stop flag. When true the thread loop will end.
    device : ITCDevice
        The instance of the device that shall be queried for data.
    q : queue.Queue
        The communications queue into which the queried data is insered for
        other process to access.
    delay : float
        The delay, in seconds, between queries to the device.
    chan_list : list
        A list of strings giving name to the channels that will be queried.
        This is necessary so that the collection buffer can setup its data
        before collection starts.
        The order does not matter.

    Methods
    -------
    run
    stop_thread

    """

    def __init__(self, device, chan_list, delay=0.2):
        super(ITCMeasurementThread, self).__init__()
        assert type(chan_list) is list, ('The chan_list parameter needs to be '
                                         'a list of strings naming the '
                                         'from which data will be collected.')
        assert type(delay) is float, ('The delay passed to the measurement '
                                      'thread needs to be a float')
        self.stop = False
        self.device = device
        self.q = Queue()
        self.delay = delay
        self.chan_list = chan_list

    def run(self):
        """Method representing the thread's activity

        See Also
        --------
        threading.Thread

        """
        while not self.stop:
            time.sleep(self.delay)
            temps = self.device.get_all_temperatures()
            self.q.put(temps)

    def stop_thread(self):
        """Method to call to halt the thread's activity."""
        self.stop = True


def main():

    DEVPATH = os.path.join(os.getcwd(), 'test', 'devices.yaml')
    # DEVPATH = '/home/chris/Programming/github/RunMeas/test/devices.yaml'

    rm = visa.ResourceManager("{}@sim".format(DEVPATH))
    for resource_address in rm.list_resources():
        if 'GPIB' in resource_address and '24' in resource_address:
            itc01 = ITCDevice(resource_address)
            itc01.set_resource(rm.open_resource)

    itc_thread = ITCMeasurementThread(itc01,
                                      ['THe3', 'TSorp', 'T1K'],
                                      delay=0.2)
    itc_thread.start()
    time.sleep(0.5)
    itc_thread.stop_thread()
    while not itc_thread.q.empty():
        print(itc_thread.q.get())

if __name__ == "__main__":
    main()
