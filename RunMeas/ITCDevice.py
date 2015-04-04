#!/usr/bin/env python
# coding: utf-8

"""The ITC Module.

"""

import visa
import time
from datetime import datetime
from threading import Thread
from queue import Queue

DEVPATH = '/home/chris/Programming/github/RunMeas/test/devices.yaml'

SENSORS = {"1": "TSorp", "2": "THe3", "3": "T1K"}


class ITCDevice(object):

    def __init__(self, address="GPIB1::24::INSTR", read_term="\r",
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
        self.resource = resource(self.address,
                                 read_termination=self.read_term,
                                 write_termination=self.write_term)

    def get_tsorp(self):
        "Get the temperature at the sorption pump."
        tsorp_str = self.resource.query("R1")
        tsorp_flt = float(tsorp_str.lstrip("R"))
        return tsorp_flt

    def get_the3(self):
        "Get the temperature at the sorption pump."
        the3_str = self.resource.query("R2")
        the3_flt = float(the3_str.lstrip("R"))
        return the3_flt

    def get_t1k(self):
        "Get the temperature at the sorption pump."
        t1k_str = self.resource.query("R3")
        t1k_flt = float(t1k_str.lstrip("R"))
        return t1k_flt

    def _set_heater_to_tsrop(self):
        "Set the heater to the sorption pump"
        self.resource.query("H1")
        self.heater_set = True

    def get_heater_sensor(self):
        "Get the heater sensor"
        status_byte = self.resource.query("X")
        if status_byte == 'ERROR':
            status_byte = self.resource.query("XH")
        sensor_nr = status_byte.split("H")[-1][0]
        return SENSORS[sensor_nr]

    def set_setpoint(self, setpoint):
        "Set the set point temperature of the sorption pump"
        if not isinstance(setpoint, (float, int)):
            raise TypeError("The setpoint provided needs to be a float "
                            "or an int.")
        if not self.heater_set:
            self._set_heater_to_tsrop()
        self.resource.query("T{:.3f}".format(setpoint))

    def get_setpoint(self):
        "Get the setpoint of the sorption pump heater."
        setpoint_str = self.resource.query("R0")
        setpoint_flt = float(setpoint_str.lstrip("R"))
        return setpoint_flt

    def auto_heat_on(self):
        "Turn on the auto heat control."
        self.resource.query("A1")
        self.auto_heat = True

    def auto_heat_off(self):
        "Turn on the auto heat control."
        self.resource.query("A0")
        self.auto_heat = False

    def get_auto_heat_status(self):
        sensor_nr = self.resource.query("X")
        if sensor_nr == 'ERROR':
            sensor_nr = self.resource.query("XA")

        sensor_nr = sensor_nr.split("A")[-1][0]

        if sensor_nr == "0":
            return "Off"
        elif sensor_nr == "1":
            return "On"

    def auto_pid_on(self):
        "Turn on the auto pid for temperature control"
        self.resource.query("L1")
        self.auto_pid = True

    def auto_pid_off(self):
        "Turn off the auto pid for temperature control"
        self.resource.query("L0")
        self.auto_pid = False

    def get_auto_pid_status(self):
        "Get the status of the auto pid setting"
        status_byte = self.resource.query("X")
        if status_byte == 'ERROR':
            status_byte = self.resource.query("XL")

        sensor_nr = status_byte.split("L")[-1][0]

        if sensor_nr == "0":
            return "Off"
        elif sensor_nr == "1":
            return "On"

    def set_heater_output(self, output):
        "Set the heater output manually"
        if not isinstance(output, (float, int)):
            raise TypeError("The output provided needs to be a float "
                            "or an int.")
        self.resource.query("O{:.1f}".format(output))

    def get_heater_output(self):
        "Get the current heater output"
        heater_output_str = self.resource.query("R5")
        heater_output_flt = float(heater_output_str.lstrip("R"))
        return heater_output_flt

    def get_all_temperatures(self):
        "Get all temperatures from all three sensors."
        now = datetime.now()
        TSorp = self.get_tsorp()
        THe3 = self.get_the3()
        T1K = self.get_t1k()
        return (now, TSorp, THe3, T1K)


class ITCMeasurementThread(Thread):

    def __init__(self, device, q):
        super(ITCMeasurementThread, self).__init__()
        self.stop = False
        self.device = device
        self.q = q

    def run(self):
        while not self.stop:
            time.sleep(0.1)
            temps = self.device.get_all_temperatures()
            self.q.put(temps)

    def stop_thread(self):
        self.stop = True


def main():

    rm = visa.ResourceManager("{}@sim".format(DEVPATH))
    itc01 = ITCDevice()
    for resource in rm.list_resources():
        if "GPIB" in resource:
            itc01.set_resource(rm.open_resource)

    itc_queue = Queue()

    itc_thread = ITCMeasurementThread(itc01, itc_queue)
    itc_thread.start()
    time.sleep(0.5)
    itc_thread.stop_thread()
    while not itc_queue.empty():
        print(itc_queue.get())

if __name__ == "__main__":
    main()
