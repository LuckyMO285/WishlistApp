# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'design.ui'
#
# Created by: PyQt5 UI code generator 5.15.0
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1436, 886)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.horizontalLayoutWidget = QtWidgets.QWidget(self.centralwidget)
        self.horizontalLayoutWidget.setGeometry(QtCore.QRect(10, 10, 621, 521))
        self.horizontalLayoutWidget.setObjectName("horizontalLayoutWidget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.gridWidget = QtWidgets.QWidget(self.horizontalLayoutWidget)
        self.gridWidget.setObjectName("gridWidget")
        self.gridWidget.setVisible(False)
        self.gridLayout = QtWidgets.QGridLayout(self.gridWidget)
        self.gridLayout.setObjectName("gridLayout")
        self.tableWidget = QtWidgets.QTableWidget(self.gridWidget)
        self.tableWidget.setRowCount(1)
        self.tableWidget.setColumnCount(5)
        self.tableWidget.setObjectName("tableWidget")
        self.gridLayout.addWidget(self.tableWidget, 1, 2, 1, 1)
        self.wishlist_Title = QtWidgets.QLabel(self.gridWidget)
        self.wishlist_Title.setText("")
        self.wishlist_Title.setObjectName("wishlist_Title")
        self.gridLayout.addWidget(self.wishlist_Title, 0, 2, 1, 1)
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.add_pushButton = QtWidgets.QPushButton(self.gridWidget)
        self.add_pushButton.setObjectName("add_pushButton")
        self.verticalLayout.addWidget(self.add_pushButton)
        self.edit_pushButton = QtWidgets.QPushButton(self.gridWidget)
        self.edit_pushButton.setObjectName("edit_pushButton")
        self.verticalLayout.addWidget(self.edit_pushButton)
        self.delete_pushButton = QtWidgets.QPushButton(self.gridWidget)
        self.delete_pushButton.setObjectName("delete_pushButton")
        self.verticalLayout.addWidget(self.delete_pushButton)
        self.gridLayout.addLayout(self.verticalLayout, 1, 3, 1, 1)
        self.horizontalLayout.addWidget(self.gridWidget)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1436, 21))
        self.menubar.setObjectName("menubar")
        self.menuFile = QtWidgets.QMenu(self.menubar)
        self.menuFile.setObjectName("menuFile")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.action_Create = QtWidgets.QAction(MainWindow)
        self.action_Create.setObjectName("action_Create")
        self.actionCreate_new_wishlist = QtWidgets.QAction(MainWindow)
        self.actionCreate_new_wishlist.setObjectName("actionCreate_new_wishlist")
        self.action_Load = QtWidgets.QAction(MainWindow)
        self.action_Load.setObjectName("action_Load")
        self.menuFile.addAction(self.action_Create)
        self.menuFile.addAction(self.action_Load)
        self.menubar.addAction(self.menuFile.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def activateTable(self, MainWindow):
        self.gridWidget.setVisible(True)

    def setTextToWishlistTable(self, MainWindow, w_title):
        self.wishlist_Title.setText(w_title)

    def printToTable(self, MainWindow, result):
        self.tableWidget.setRowCount(0)
        for row_number, row_data in enumerate(result):
            self.tableWidget.insertRow(row_number)
            for column_number, data in enumerate(row_data):
                self.tableWidget.setItem(row_number, column_number, QtWidgets.QTableWidgetItem(str(data)))

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.add_pushButton.setText(_translate("MainWindow", "Add..."))
        self.edit_pushButton.setText(_translate("MainWindow", "Edit..."))
        self.delete_pushButton.setText(_translate("MainWindow", "Delete..."))
        self.menuFile.setTitle(_translate("MainWindow", "&File"))
        self.action_Create.setText(_translate("MainWindow", "Create new wishlist..."))
        self.actionCreate_new_wishlist.setText(_translate("MainWindow", "Create new wishlist..."))
        self.action_Load.setText(_translate("MainWindow", "Load wishlist..."))
