#!/usr/bin/env python
# -*- coding: utf-8 -*-
""" The main script.

"""

__author__ = "Christopher Espy"
__copyright__ = "Copyright (C) 2015, Christopher Espy"
__credits__ = ["Christopher Espy"]
__license__ = "GPLv2"
__version__ = "0.0.1"
__maintainer__ = "Christopher Espy"
__email__ = "christopher.espy@uni-konstanz.de"
__status__ = "Development"

import os
import sys

import visa
from PyQt4.QtGui import (QApplication)

from RunMeas.ITC_view import MyMainWindow


RESOURCES = {'GPIB1::24':
             {'ITC503': ['timestamp',
                         'TSorp',
                         'THe3',
                         'T1K']},
             # 'GPIB1::28':
             # {'AH': []},
             # 'GPIB1::9':
             # {'I_Lockin': []},
             # 'GPIB1::17':
             # {'Lakeshore': ['TSample_LS']},
             # 'GPIB1::8':
             # {'V_Lockin': []},
             # 'GPIB1::3':
             # {'Yokogawa': []},
             # 'GPIB::25':
             # {'IPS': ['Magnetfield']}
             }


class Main(MyMainWindow):
    """The main window of the ITC.

    """

    def __init__(self, parent=None):
        super(Main, self).__init__(parent)


class Presenter(object):
    """Hi

    """

    def __init__(self):
        super(Presenter, self).__init__()

        self.view = None
        self.channelsList = None
        self.deviceList = None
        self.buffer = None

        self.fileMenu = None
        self.fileMenuActions = None

    def setDeviceList(self, devices):
        """Set the list of available devices.

        Parameters
        ----------
        devices : list
            The list of visa addresses where the devices can be found.

        """
        assert type(devices) is list, "The address list is not a string!"
        self.deviceList = devices

    def setView(self, view):
        """Set the view to which the information is pushed.

        Parameters
        ----------
        view : PyQt.QtGui
            The main window, dialog, etc through with the information is
            displayed.

        """

        self.view = view
        self._setUpView()

    def _setUpView(self):
        """Once the view and underlying model have added, setup the view.

        """

        # Actions
        fileQuitAction = self.view.createAction("&Quit", self.view.close,
                                                "Ctrl+Q", "exit",
                                                "Close the application")

        # Add the 'File' menu to the menu bar
        self.fileMenu = self.view.menuBar().addMenu("&File")
        self.fileMenuActions = (fileQuitAction,)
        self.view.addActions(self.fileMenu, self.fileMenuActions)

        # Connections

        # Set the devices
        self.view.deviceSelector.addItems(self.deviceList)

    def setBuffer(self, buffer):
        self.buffer = buffer

        self.view.connectDevice.clicked.connect(self.buffer.start_collection)
        self.view.disconnectDevice.clicked.connect(self.buffer.stop_collection)
        self.view.recordData.clicked.connect(self.buffer.start_recording)
        self.view.stopRecording.clicked.connect(self.buffer.stop_recording)


def main(argv=None):
    """The main function

    """

    from RunMeas.Buffer import Buffer
    from RunMeas.ITCDevice import ITCDevice, ITCMeasurementThread

    meas_thread_register = []
    device_register = []

    DEVPATH = os.path.join(os.getcwd(), 'test', 'devices.yaml')

    if argv is None:
        argv = sys.argv

    if sys.platform == 'win32':
        rm = visa.ResourceManager()
    elif sys.platform == 'linux':
        rm = visa.ResourceManager("{}@sim".format(DEVPATH))

    devices = []
    device_register = []
    for resource in rm.list_resources():
        addy_prefix = '::'.join(resource.split('::')[:2])
        try:
            resource_name = list(RESOURCES[addy_prefix].keys())[0]
            devices.append(resource_name)
            if 'ITC' in resource_name:
                if sys.platform == 'win32':
                    resource_addy = addy_prefix + '::INSTR'
                    itc_device = ITCDevice(address=resource_addy)
                    itc_device.set_resource(rm.open_resource)
                elif sys.platform == 'linux':
                    resource_addy = resource
                    itc_device = ITCDevice(address=resource)
                    itc_device.set_resource(rm.open_resource)
                print(resource_addy)
                device_register.append((resource_name, itc_device))

                itc_measurement_thread = ITCMeasurementThread(itc_device,
                                                              ['TSorp', 'THe3',
                                                               'T1K'],
                                                              delay=0.1)

                meas_thread_register.append((resource_name, itc_device,
                                             itc_measurement_thread))

        except KeyError:
            pass

    my_buffer = Buffer(meas_thread_register)
    my_buffer.set_data_folder(os.path.join(os.getcwd(), 'temp_data'))

    app = QApplication(argv)
    app.setOrganizationName("RunMeasGmbH")
    app.setApplicationName("RunMeas")

    presenter = Presenter()

    presenter.setDeviceList(devices)

    presenter.setView(Main())
    presenter.setBuffer(my_buffer)
    presenter.view.show()

    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
