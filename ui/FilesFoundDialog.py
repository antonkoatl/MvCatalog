from PyQt5.QtCore import Qt, pyqtSlot
from PyQt5.QtWidgets import QDialog, QListWidgetItem

import data.design_dialog_found_files

class FilesFoundDialog(QDialog, data.design_dialog_found_files.Ui_Dialog):

    def __init__(self, parent=None):
        super(FilesFoundDialog, self).__init__(parent)
        self.setupUi(self)

    def prepare(self):
        self.progressBar.setValue(0)
        self.listWidget.clear()

        '''
        for f in files:
            myQListWidgetItem = QListWidgetItem(f[0])
            #myQListWidgetItem.setSizeHint(cwidget.sizeHint())
            myQListWidgetItem.setData(Qt.UserRole, f[1])
            myQListWidgetItem.setFlags(myQListWidgetItem.flags() | Qt.ItemIsUserCheckable)
            myQListWidgetItem.setCheckState(Qt.Checked)
            self.listWidget.addItem(myQListWidgetItem)
        '''

    @pyqtSlot(str)
    def add_file_to_list(self, data):
        print(data)
        myQListWidgetItem = QListWidgetItem(data.split('/')[-1])
        # myQListWidgetItem.setSizeHint(cwidget.sizeHint())
        myQListWidgetItem.setData(Qt.UserRole, data)
        myQListWidgetItem.setFlags(myQListWidgetItem.flags() | Qt.ItemIsUserCheckable)
        myQListWidgetItem.setCheckState(Qt.Checked)
        self.listWidget.addItem(myQListWidgetItem)
