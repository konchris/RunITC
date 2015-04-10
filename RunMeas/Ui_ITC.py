# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ITCUI.ui'
#
# Created: Thu Apr  9 20:02:43 2015
#      by: PyQt4 UI code generator 4.11.2
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName(_fromUtf8("MainWindow"))
        MainWindow.resize(800, 600)
        self.centralwidget = QtGui.QWidget(MainWindow)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.horizontalLayoutWidget = QtGui.QWidget(self.centralwidget)
        self.horizontalLayoutWidget.setGeometry(QtCore.QRect(9, 9, 781, 541))
        self.horizontalLayoutWidget.setObjectName(_fromUtf8("horizontalLayoutWidget"))
        self.mainLayout = QtGui.QHBoxLayout(self.horizontalLayoutWidget)
        self.mainLayout.setSizeConstraint(QtGui.QLayout.SetNoConstraint)
        self.mainLayout.setMargin(0)
        self.mainLayout.setObjectName(_fromUtf8("mainLayout"))
        self.leftButtonLayout = QtGui.QVBoxLayout()
        self.leftButtonLayout.setObjectName(_fromUtf8("leftButtonLayout"))
        self.deviceSelector = QtGui.QComboBox(self.horizontalLayoutWidget)
        self.deviceSelector.setObjectName(_fromUtf8("deviceSelector"))
        self.leftButtonLayout.addWidget(self.deviceSelector)
        self.connectDevice = QtGui.QPushButton(self.horizontalLayoutWidget)
        self.connectDevice.setObjectName(_fromUtf8("connectDevice"))
        self.leftButtonLayout.addWidget(self.connectDevice)
        self.recordData = QtGui.QPushButton(self.horizontalLayoutWidget)
        self.recordData.setObjectName(_fromUtf8("recordData"))
        self.leftButtonLayout.addWidget(self.recordData)
        spacerItem = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.leftButtonLayout.addItem(spacerItem)
        self.stopRecording = QtGui.QPushButton(self.horizontalLayoutWidget)
        self.stopRecording.setObjectName(_fromUtf8("stopRecording"))
        self.leftButtonLayout.addWidget(self.stopRecording)
        self.disconnectDevice = QtGui.QPushButton(self.horizontalLayoutWidget)
        self.disconnectDevice.setObjectName(_fromUtf8("disconnectDevice"))
        self.leftButtonLayout.addWidget(self.disconnectDevice)
        self.mainLayout.addLayout(self.leftButtonLayout)
        self.graphLayout = QtGui.QVBoxLayout()
        self.graphLayout.setObjectName(_fromUtf8("graphLayout"))
        self.mainLayout.addLayout(self.graphLayout)
        self.tableLayout = QtGui.QVBoxLayout()
        self.tableLayout.setObjectName(_fromUtf8("tableLayout"))
        self.mainLayout.addLayout(self.tableLayout)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtGui.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 21))
        self.menubar.setObjectName(_fromUtf8("menubar"))
        self.menuFile = QtGui.QMenu(self.menubar)
        self.menuFile.setObjectName(_fromUtf8("menuFile"))
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtGui.QStatusBar(MainWindow)
        self.statusbar.setObjectName(_fromUtf8("statusbar"))
        MainWindow.setStatusBar(self.statusbar)
        self.action_Quit = QtGui.QAction(MainWindow)
        self.action_Quit.setObjectName(_fromUtf8("action_Quit"))
        self.actionQuit = QtGui.QAction(MainWindow)
        self.actionQuit.setObjectName(_fromUtf8("actionQuit"))
        self.menuFile.addSeparator()
        self.menuFile.addAction(self.actionQuit)
        self.menubar.addAction(self.menuFile.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QObject.connect(self.action_Quit, QtCore.SIGNAL(_fromUtf8("triggered()")), MainWindow.close)
        QtCore.QObject.connect(self.actionQuit, QtCore.SIGNAL(_fromUtf8("triggered()")), self.action_Quit.trigger)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow", None))
        self.connectDevice.setText(_translate("MainWindow", "Connect Data", None))
        self.recordData.setText(_translate("MainWindow", "Record Data", None))
        self.stopRecording.setText(_translate("MainWindow", "Stop Recording", None))
        self.disconnectDevice.setText(_translate("MainWindow", "Disconnect Device", None))
        self.menuFile.setTitle(_translate("MainWindow", "File", None))
        self.action_Quit.setText(_translate("MainWindow", "%Quit", None))
        self.action_Quit.setShortcut(_translate("MainWindow", "Ctrl+Q", None))
        self.actionQuit.setText(_translate("MainWindow", "&Quit", None))

import resources_rc
