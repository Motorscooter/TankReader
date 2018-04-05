# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'Mainwindow.ui'
#
# Created by: PyQt5 UI code generator 5.6
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_mainwindow(object):
    def setupUi(self, mainwindow):
        mainwindow.setObjectName("mainwindow")
        mainwindow.resize(724, 489)
        self.centralwidget = QtWidgets.QWidget(mainwindow)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName("gridLayout")
        self.openFile = QtWidgets.QPushButton(self.centralwidget)
        self.openFile.setObjectName("openFile")
        self.gridLayout.addWidget(self.openFile, 0, 0, 1, 1)
        self.label_3 = QtWidgets.QLabel(self.centralwidget)
        self.label_3.setAlignment(QtCore.Qt.AlignCenter)
        self.label_3.setObjectName("label_3")
        self.gridLayout.addWidget(self.label_3, 0, 1, 1, 2)
        self.titlebox = QtWidgets.QLineEdit(self.centralwidget)
        self.titlebox.setObjectName("titlebox")
        self.gridLayout.addWidget(self.titlebox, 0, 3, 1, 3)
        self.tableWidget = QtWidgets.QTableWidget(self.centralwidget)
        self.tableWidget.setObjectName("tableWidget")
        self.tableWidget.setColumnCount(0)
        self.tableWidget.setRowCount(0)
        self.gridLayout.addWidget(self.tableWidget, 1, 0, 1, 6)
        self.average = QtWidgets.QCheckBox(self.centralwidget)
        self.average.setObjectName("average")
        self.gridLayout.addWidget(self.average, 2, 0, 1, 1)
        self.unitBox = QtWidgets.QComboBox(self.centralwidget)
        self.unitBox.setObjectName("unitBox")
        self.gridLayout.addWidget(self.unitBox, 4, 0, 1, 1)
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setAlignment(QtCore.Qt.AlignCenter)
        self.label_2.setObjectName("label_2")
        self.gridLayout.addWidget(self.label_2, 3, 0, 1, 1)
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 3, 1, 1, 2)
        self.filterBox = QtWidgets.QComboBox(self.centralwidget)
        self.filterBox.setObjectName("filterBox")
        self.gridLayout.addWidget(self.filterBox, 4, 1, 1, 2)
        self.graphbtn = QtWidgets.QPushButton(self.centralwidget)
        self.graphbtn.setObjectName("graphbtn")
        self.gridLayout.addWidget(self.graphbtn, 4, 3, 1, 3)
        mainwindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(mainwindow)
        self.statusbar.setObjectName("statusbar")
        mainwindow.setStatusBar(self.statusbar)

        self.retranslateUi(mainwindow)
        QtCore.QMetaObject.connectSlotsByName(mainwindow)

    def retranslateUi(self, mainwindow):
        _translate = QtCore.QCoreApplication.translate
        mainwindow.setWindowTitle(_translate("mainwindow", "Tank Data"))
        self.openFile.setText(_translate("mainwindow", "Add Tank Data"))
        self.label_3.setText(_translate("mainwindow", "Title"))
        self.average.setText(_translate("mainwindow", "Average Groups"))
        self.label_2.setText(_translate("mainwindow", "Units"))
        self.label.setText(_translate("mainwindow", "SAE Filter"))
        self.graphbtn.setText(_translate("mainwindow", "Graph"))

