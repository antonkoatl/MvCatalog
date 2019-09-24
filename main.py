import sys, time
from PyQt5 import QtWidgets, uic, QtGui, QtCore
from PyQt5.QtCore import QThread, QObject, pyqtSignal, pyqtSlot, QSettings
from PyQt5.QtWidgets import QTableWidgetItem
from core import *
import data.design_main

class MyWindow(QtWidgets.QMainWindow, data.design_main.Ui_MainWindow):
    sig1 = pyqtSignal(str)
    list_data = []

    def __init__(self):
        super(MyWindow, self).__init__()
        self.settings = QSettings("MyCompany", "MyApp")
        #uic.loadUi('data/main.ui', self)
        self.setupUi(self)

        if not self.settings.value("geometry") == None:
            self.restoreGeometry(self.settings.value("geometry"))
        if not self.settings.value("windowState") == None:
            self.restoreState(self.settings.value("windowState"))

        for i in range(self.tableWidget.rowCount()):
            self.tableWidget.setItem(i, 0, QTableWidgetItem(""))

        for i in range(self.tableWidget_2.rowCount()):
            self.tableWidget_2.setItem(i, 0, QTableWidgetItem(""))

        self.listWidget.itemClicked.connect(self.list_item_clicked)

        self.show()
        self.myThread = CoreThread()
        self.myThread.start()
        self.myThread.sig1.connect(self.fill_records_list)

    def closeEvent(self, event):
        self.settings.setValue("geometry", self.saveGeometry())
        self.settings.setValue("windowState", self.saveState())
        QtWidgets.QMainWindow.closeEvent(self, event)

    def fill_records_list(self, data):
        self.list_data = data
        self.listWidget.clear()
        for item in self.list_data:
            if item == None: break
            self.listWidget.addItem(item[12])

    def list_item_clicked(self, item):
        index = self.listWidget.currentRow()
        for i in range(self.tableWidget_2.rowCount()):
            self.tableWidget_2.item(i, 0).setText(str(self.list_data[index][i+2]))

        for i in range(self.tableWidget.rowCount()):
            j = i + self.tableWidget_2.rowCount()
            self.tableWidget.item(i, 0).setText(str(self.list_data[index][j+3]))


if __name__ == '__main__':
    sys._excepthook = sys.excepthook
    def exception_hook(exctype, value, traceback):
        print(exctype, value, traceback)
        sys._excepthook(exctype, value, traceback)
        sys.exit(1)
    sys.excepthook = exception_hook

    app = QtWidgets.QApplication(sys.argv)
    window = MyWindow()
    sys.exit(app.exec_())
