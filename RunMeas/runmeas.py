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

from PyQt4.QtGui import (QApplication, QMainWindow)

from RunMeas.Ui_ITC import Ui_MainWindow as MainWindow


class MyMainWindow(QMainWindow, MainWindow):
    """The main window of the ITC.

    """

    def __init__(self, parent=None):
        super(MyMainWindow, self).__init__(parent)

        self.setupUi(self)


def main(argv=None):
    """The main function

    """

    if argv is None:
        argv = sys.argv

    app = QApplication(argv)
    form = MyMainWindow()
    form.show()

    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
