#!/usr/bin/env python
# coding: utf-8

"""The ITC Module.

"""

import visa

DEVPATH = '/home/chris/Programming/github/RunITC/test/devices.yaml'


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

    def set_resource(self, resource):
        self.resource = resource(self.address,
                                 read_termination=self.read_term,
                                 write_termination=self.write_term)

    def get_tsorp(self):
        "Get the temperature at the sorption pump."
        return self.resource.query("R1")

    def get_the3(self):
        "Get the temperature at the sorption pump."
        return self.resource.query("R2")

    def get_t1k(self):
        "Get the temperature at the sorption pump."
        return self.resource.query("R3")

    def _set_heater_to_tsrop(self):
        "Set the heater to the sorption pump"
        self.resource.query("H1")
        self.heater_set = True

    def get_heater_sensor(self):
        "Get the heater sensor"
        sensor_nr = self.resource.query("X")
        if sensor_nr == 'ERROR':
            sensor_nr = self.resource.query("XH")
        return sensor_nr.split("H")[-1][0]

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
        return self.resource.query("R0")

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
        return sensor_nr.split("A")[-1][0]


def main():
    print("{}@sim".format(DEVPATH))
    rm = visa.ResourceManager("{}@sim".format(DEVPATH))
    itc01 = ITCDevice()
    for resource in rm.list_resources():
        print(resource)
        if "GPIB" in resource:
            itc01.set_resource(rm.open_resource)

    print(itc01.auto_pid_on())
    print(itc01.get_auto_heat_status())

if __name__ == "__main__":
    main()
