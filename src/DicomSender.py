# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'DicomSender.ui'
#
# Created by: PyQt5 UI code generator 5.6
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets
import os, time
from pydicom import read_file
from pynetdicom3 import AE, StorageSOPClassList

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.setWindowModality(QtCore.Qt.NonModal)
        Dialog.resize(210, 175)
        Dialog.setMinimumSize(QtCore.QSize(210, 175))
        Dialog.setMaximumSize(QtCore.QSize(210, 175))

        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("ayva.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        Dialog.setWindowIcon(icon)

        self.label_4 = QtWidgets.QLabel(Dialog)
        self.label_4.setGeometry(QtCore.QRect(75, 130, 101, 16))
        self.label_4.setObjectName("label_4")

        self.label_5 = QtWidgets.QLabel(Dialog)
        self.label_5.setGeometry(QtCore.QRect(85, 150, 101, 16))
        self.label_5.setObjectName("label_5")

        self.widget = QtWidgets.QWidget(Dialog)
        self.widget.setGeometry(QtCore.QRect(10, 10, 186, 109))
        self.widget.setObjectName("widget")

        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.widget)
        self.verticalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setObjectName("verticalLayout_2")

        self.label = QtWidgets.QLabel(self.widget)
        self.label.setObjectName("label")
        self.verticalLayout_2.addWidget(self.label)
        self.label_2 = QtWidgets.QLabel(self.widget)
        self.label_2.setObjectName("label_2")
        self.verticalLayout_2.addWidget(self.label_2)
        self.label_3 = QtWidgets.QLabel(self.widget)
        self.label_3.setObjectName("label_3")
        self.verticalLayout_2.addWidget(self.label_3)
        self.horizontalLayout_2.addLayout(self.verticalLayout_2)
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")

        ipRange = "(?:[0-1]?[0-9]?[0-9]|2[0-4][0-9]|25[0-5])"
        ipRegex = QtCore.QRegExp("^" + ipRange + "\\." + ipRange + "\\." + ipRange + "\\." + ipRange + "$")
        ipValidator = QtGui.QRegExpValidator(ipRegex)
        self.ip_line = QtWidgets.QLineEdit(self.widget)
        self.ip_line.setValidator(ipValidator)
        self.ip_line.setObjectName("ip_line")

        self.verticalLayout.addWidget(self.ip_line)


        portRegex = QtCore.QRegExp("\d{1,6}")
        portValidator = QtGui.QRegExpValidator(portRegex)
        self.port_line = QtWidgets.QLineEdit(self.widget)
        self.port_line.setValidator(portValidator)
        self.port_line.setObjectName("port_line")

        self.verticalLayout.addWidget(self.port_line)

        self.source_line = QtWidgets.QLineEdit(self.widget)
        self.source_line.setObjectName("source_line")

        self.verticalLayout.addWidget(self.source_line)
        self.horizontalLayout_2.addLayout(self.verticalLayout)
        self.verticalLayout_3.addLayout(self.horizontalLayout_2)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")

        self.start_button = QtWidgets.QPushButton(self.widget)
        self.start_button.setObjectName("start_button")
        self.start_button.clicked.connect(self.baslat)

        self.horizontalLayout.addWidget(self.start_button)

        self.stop_button = QtWidgets.QPushButton(self.widget)
        self.stop_button.setObjectName("stop_button")
        self.stop_button.clicked.connect(self.durdur)

        self.horizontalLayout.addWidget(self.stop_button)
        self.verticalLayout_3.addLayout(self.horizontalLayout)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "DS"))
        self.label_4.setText(_translate("Dialog", "Dicom Sender"))
        self.label_5.setText(_translate("Dialog", "Ufuk Özer"))
        self.label.setText(_translate("Dialog", "Ip:"))
        self.label_2.setText(_translate("Dialog", "Port:"))
        self.label_3.setText(_translate("Dialog", "Kaynak:"))
        self.start_button.setText(_translate("Dialog", "Başlat"))
        self.stop_button.setText(_translate("Dialog", "Durdur"))

    def baslat(self):
        self.start_button.setEnabled(False)
        self.stop_button.setEnabled(True)
        self.source_line.setEnabled(False)
        self.ip_line.setEnabled(False)
        self.port_line.setEnabled(False)
        self.esas_kaynak = self.source_line.text()
        self.ip = self.ip_line.text()
        self.port = int(self.port_line.text())
        self.durum = 0
        self.thread = Sender()
        self.thread.start(self.thread.gonderici(self.esas_kaynak, self.ip, self.port, self.durum))

    def durdur(self):
        self.stop_button.setEnabled(False)
        self.start_button.setEnabled(True)
        self.source_line.setEnabled(True)
        self.ip_line.setEnabled(True)
        self.port_line.setEnabled(True)
        self.esas_kaynak = self.source_line.text()
        self.durum = 1
        self.thread = Sender()
        self.thread.moveToThread(self.thread)
        self.thread.exec_()
        self.thread.terminated(True)

class Sender(QtCore.QThread):
    def gonderici(self, esas_kaynak, ip, port, durum):

        QtGui.QGuiApplication.processEvents()
        #QtCore.QCoreApplication.processEvents()
        kaynak = esas_kaynak.replace("\\", "/")
        if kaynak[-1] != "/":
            kaynak = kaynak + "/"
        ae = AE(scu_sop_class=StorageSOPClassList)
        while durum == 0:
            QtGui.QGuiApplication.processEvents()
            #QtCore.QCoreApplication.processEvents()
            time.sleep(3)
            if not os.listdir(kaynak):
                QtGui.QGuiApplication.processEvents()
                #QtCore.QCoreApplication.processEvents()
                print("dene")
                continue
            else:
                print("bakiyor")
                klasorler = []
                for i in os.walk(kaynak):
                    klasorler.append(i)
                if len(klasorler) == 1:
                    #tek dizin
                    dosya_sayisi = len(klasorler[0][2])-1
                    sayac=0
                    while sayac <= dosya_sayisi:
                        assoc = ae.associate(ip, port)
                        if assoc.is_established:
                            dataset = read_file(kaynak + klasorler[0][2][sayac])
                            assoc.send_c_store(dataset)
                            assoc.release()
                            os.remove(kaynak + klasorler[0][2][sayac])
                            sayac+=1
                #else:
                 #   print("çoklu dizin")

if __name__ == "__main__":
    from sys import exit, argv
    app = QtWidgets.QApplication(argv)
    Dialog = QtWidgets.QWidget()
    ui = Ui_Dialog()
    ui.setupUi(Dialog)
    Dialog.show()
    exit(app.exec_())
