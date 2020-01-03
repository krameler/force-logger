# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'conf_server_window.ui'
#
# Created by: PyQt5 UI code generator 5.10.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_conf_server_window(object):
    def setupUi(self, conf_server_window):
        conf_server_window.setObjectName("conf_server_window")
        conf_server_window.resize(800, 600)
        self.centralwidget = QtWidgets.QWidget(conf_server_window)
        self.centralwidget.setObjectName("centralwidget")
        conf_server_window.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(conf_server_window)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 22))
        self.menubar.setObjectName("menubar")
        conf_server_window.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(conf_server_window)
        self.statusbar.setObjectName("statusbar")
        conf_server_window.setStatusBar(self.statusbar)

        self.retranslateUi(conf_server_window)
        QtCore.QMetaObject.connectSlotsByName(conf_server_window)

    def retranslateUi(self, conf_server_window):
        _translate = QtCore.QCoreApplication.translate
        conf_server_window.setWindowTitle(_translate("conf_server_window", "MainWindow"))

