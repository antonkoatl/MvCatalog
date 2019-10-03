# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'listitem_search.ui'
#
# Created by: PyQt5 UI code generator 5.13.0
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(102, 34)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(Form.sizePolicy().hasHeightForWidth())
        Form.setSizePolicy(sizePolicy)
        Form.setStyleSheet("")
        self.gridLayout = QtWidgets.QGridLayout(Form)
        self.gridLayout.setContentsMargins(4, 4, 4, 4)
        self.gridLayout.setObjectName("gridLayout")
        self.label_original_name = QtWidgets.QLabel(Form)
        self.label_original_name.setStyleSheet("background-color: rgba(86, 23, 23, 50);")
        self.label_original_name.setObjectName("label_original_name")
        self.gridLayout.addWidget(self.label_original_name, 0, 1, 1, 1)
        self.label_movie_name = QtWidgets.QLabel(Form)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.label_movie_name.setFont(font)
        self.label_movie_name.setStyleSheet("background-color: rgba(86, 23, 23, 50);")
        self.label_movie_name.setObjectName("label_movie_name")
        self.gridLayout.addWidget(self.label_movie_name, 0, 0, 1, 1)
        self.label_source = QtWidgets.QLabel(Form)
        self.label_source.setStyleSheet("background-color: rgba(86, 23, 23, 20);")
        self.label_source.setObjectName("label_source")
        self.gridLayout.addWidget(self.label_source, 1, 0, 1, 1)
        self.label_year = QtWidgets.QLabel(Form)
        self.label_year.setStyleSheet("background-color: rgba(86, 23, 23, 20);")
        self.label_year.setObjectName("label_year")
        self.gridLayout.addWidget(self.label_year, 1, 1, 1, 1)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.label_original_name.setText(_translate("Form", "TextLabel"))
        self.label_movie_name.setText(_translate("Form", "TextLabel"))
        self.label_source.setText(_translate("Form", "TextLabel"))
        self.label_year.setText(_translate("Form", "TextLabel"))
