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

import sys

from PyQt4.QtCore import (SIGNAL)
from PyQt4.QtGui import (QApplication, QMainWindow, QSizePolicy, QAction,
                         QIcon)
from tzlocal import get_localzone
import matplotlib as mpl
from matplotlib.figure import Figure
from matplotlib import pyplot as plt
from matplotlib.backends.backend_qt4agg import (FigureCanvasQTAgg as
                                                FigureCanvas)
from matplotlib.backends.backend_qt4agg import (NavigationToolbar2QT as
                                                NavigationToolbar)

import seaborn as sns

from RunMeas.Ui_ITC import Ui_MainWindow as MainWindow

sns.set_context("talk", font_scale=1.25, rc={'lines.linewidth': 3})
sns.set_style('whitegrid')


class MyMainWindow(QMainWindow, MainWindow):
    """The main window of the ITC.

    """

    def __init__(self, parent=None):
        super(MyMainWindow, self).__init__(parent)

        mpl.rcParams['timezone'] = get_localzone().zone

        self.setupUi(self)

        # Matplotlib canvas
        fig, axes1 = plt.subplots()
        fig.set_dpi(120)

        fig.autofmt_xdate()

        self.canvas = FigureCanvas(fig)
        self.canvas.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        mpl_toolbar = NavigationToolbar(self.canvas, self.canvas)

        self.axes1 = axes1
        self.axes2 = axes1.twinx()
        self.axes2.grid(False)

        self.graphLayout.insertWidget(0, self.canvas)
        self.graphLayout.insertWidget(1, mpl_toolbar)

        # Adjust the offset spinbox range and significant digits
        # self.offsetSpinBox.setDecimals(10)
        # self.offsetSpinBox.setRange(-1000000,1000000)

    def createAction(self, text, slot=None, shortcut=None, icon=None,
                     tip=None, checkable=False, signal="triggered()"):
        """Do something.

        This was take from 'Rapid Gui Programming with Python and Qt' by Mark
        Summerfield. This code automates the tasks associated with creating new
        actions.

        Parameters
        ----------
        text : str
            The text of the action.
        slot : , optional
            The slot to which the action will be connected.
        shortcut: str or PyQt.QtGui.QKeySequence, optional
            The shortcut keyboard sequence for the action.
        icon : str, optional
            The base filename of image to use as the icon.
        tip : str, optional
            The string that should appear in the tool tip and status tip.
        checkable : boolean, optional
            Whether the action in the menu bar is checkable.
        signal : str, optional
            The the text of the PyQt.QtCore.SIGNAL to use for the action.

        Returns
        -------
        PyQt.QtGui.QAction


        """
        # Create the action
        action = QAction(text, self)
        # Give it its icon
        if icon is not None:
            action.setIcon(QIcon(":/{icon}.png".format(icon=icon)))
        # Give it its shortcut
        if shortcut is not None:
            action.setShortcut(shortcut)
        # Set up its help/tip text
        if tip is not None:
            action.setToolTip(tip)
            action.setStatusTip(tip)
        # Connect it to a signal
        if slot is not None:
            self.connect(action, SIGNAL(signal), slot)
        # Make it checkable
        if checkable:
            action.setCheckable(True)
        return action

    def addActions(self, target, actions):
        """Add an action to the target object.

        Parameters
        ----------
        target : PyQt.QtGui.QObject
            The object, usually a QFileMenu, to which the action should be
            added.
        actions : list
            A list of the actions to add to target.

        """
        for action in actions:
            if action is None:
                target.addSeparator()
            else:
                target.addAction(action)


def main(argv=None):
    "The main function"

    if argv is None:
        argv = sys.argv

    app = QApplication(sys.argv)
    form = MyMainWindow()
    form.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()

