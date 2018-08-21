# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'D:\learning\QT\pys\widget.ui'
#
# Created: Sun Mar 18 21:27:39 2018
#      by: pyside2-uic  running on PySide2 5.9.0a1
#
# WARNING! All changes made in this file will be lost!
"""
TODO : CPU Check at first and apply commands accordingly .
"""
from PySide2 import QtCore, QtGui, QtWidgets

from adb_android import *


def is_hex(s):
    try:
        int(s, 16)
        return True
    except ValueError:
        return False


def extract(s, first, last):
    try:
        start = s.index(first) + len(first)
        end = s.index(last, start)
        return s[start:end]
    except ValueError:
        return "nothing"


def write_to_ui(text):
    ui.mytext.insertPlainText(text)



class Ui_Widget(object):

    def setupUi(self, Widget):
        Widget.setObjectName("Widget")
        Widget.resize(420, 269)
        self.button = QtWidgets.QPushButton(Widget)
        self.button.setGeometry(QtCore.QRect(333, 220, 75, 23))
        self.button.setObjectName("button")
        self.button.clicked.connect(self.clicked)
        self.mytext = QtWidgets.QTextBrowser(Widget)
        self.mytext.setGeometry(QtCore.QRect(10, 10, 401, 192))
        self.mytext.setObjectName("mytext")
        self.retranslateUi(Widget)
        QtCore.QMetaObject.connectSlotsByName(Widget)

    def retranslateUi(self, Widget):
        Widget.setWindowTitle(QtWidgets.QApplication.translate("Widget", "ADB Console", None, -1))
        self.button.setText(QtWidgets.QApplication.translate("Widget", "Detect", None, -1))

    def clicked(self):
        click_sequence()


class AdbDevice:
    """
    Commands
    """

    get_imei = \
        """
        content query --uri content://settings/system --where "name='bd_setting_i'
        " | sed 's/[^=0-9]*//g' | sed 's/[0-9]*=//g' 
        """
    get_imei_old = \
        """
        dumpsys iphonesubinfo 1
        """
    get_model = \
        """
        getprop ro.product.model
        """
    get_factory = \
        """
        getprop ro.product.manufacturer
        """
    get_board = \
        """
        getprop ro.product.board
        """
    get_version = \
        """
        getprop ro.build.version.release
        """
    get_firmware = \
        """
        getprop ro.build.PDA

        """
    get_partitions = \
        """
        cat /proc/partitions
        """
    get_platform = \
        """
        getprop ro.board.platform
        """

    get_mtk_imei1 = \
        """
        getprop ro.ril.miui.imei0
        """

    get_mtk_imei2 = \
        """
        getprop ro.ril.miui.imei1
        """

    def __init__(self):
        self.imei()
        self.brand()
        self.model()
        self.board()
        self.version()
        self.firmware()
        self.partitions()
        self.getprop()

    def getprop(self):
        prop = shell('getprop')  # get android properties
        prop = str(prop).replace("\\r", '\r').replace('\\n', '\n')  # format
        return prop

    def imei(self):
        imei_no = shell(AdbDevice.get_imei)
        imei_no = str(imei_no[1]).replace('\n', ' ').replace('\r', '')
        return imei_no

    def imei_old(self):
        imei_no = shell(AdbDevice.get_imei_old)
        imei_no = int(filter(str.isdigit, str(imei_no)))
        # imei_no = imei_no
        return imei_no

    def mtk_imei1(self):
        imei_no = shell(AdbDevice.get_mtk_imei1)
        imei_no = int(filter(str.isdigit, str(imei_no)))
        return imei_no

    def mtk_imei2(self):
        imei_no = shell(AdbDevice.get_mtk_imei2)
        imei_no = int(filter(str.isdigit, str(imei_no)))
        return imei_no

    def brand(self):
        device_brand = shell(AdbDevice.get_factory)
        device_brand = str(device_brand[1]).replace('\n', ' ').replace('\r', '').upper()
        return device_brand

    def model(self):
        device_model = shell(AdbDevice.get_model)
        device_model = str(device_model[1]).replace('\n', ' ').replace('\r', '').upper()
        return device_model

    def board(self):
        device_board = shell(AdbDevice.get_board)
        device_board = str(device_board[1]).replace('\n', ' ').replace('\r', '').upper()
        return device_board

    def version(self):
        device_version = shell(AdbDevice.get_version)
        device_version = str(device_version[1]).replace('\n', ' ').replace('\r', '').upper()
        return device_version

    def firmware(self):
        device_firmware = shell(AdbDevice.get_firmware)
        device_firmware = str(device_firmware[1]).replace('\n', ' ').replace('\r', '').upper()
        return device_firmware

    def platform(self):
        device_platform = shell(AdbDevice.get_platform)
        device_platform = str(device_platform[1]).replace('\n', ' ').replace('\r', '').upper()
        return device_platform

    def root_check(self):
        su = \
            """
            su -c 'cat /system/build.prop'|grep "ro.product.brand="
            
            """
        read = shell(su)
        return str(read[1]).replace("\\r", '\r').replace('\\n', '\n').strip("ro.product.brand=")

    def partitions(self):
        device_partitions = shell(AdbDevice.get_partitions)
        device_partitions = str(device_partitions[1]) \
            .replace("\\r", '').replace('\\n', '\n') \
            .replace('major', '\n Partition Table with Details ') \
            .replace('#blocks', '').replace('minor', '') \
            .replace('name', '').replace('info', '')
        return device_partitions

    def device_details(self, prop):
        """
        Properties of getprop
        """
        manufacturer = "[ro.product.manufacturer]: "
        model = "[ro.product.model]: "
        versi = "[ro.build.version.release]: "
        board = "[ro.product.board]: "
        firmware = "[ro.build.description]: "

        brand = extract(prop, manufacturer, '\n').replace('[', '').replace(']', '').replace('\r', '').upper()
        model = extract(prop, model, '\n').replace('[', '').replace(']', '').replace('\r', '').upper()
        firmware = extract(prop, firmware, '\n').replace('[', '').replace(']', '').replace('\r', '').upper()
        ver = extract(prop, versi, '\n').replace('[', '').replace(']', '').replace('\r', '').upper()
        cpu = extract(prop, board, '\n').replace('[', '').replace(']', '').replace('\r', '').upper()

        return brand, model, firmware, ver, cpu

    # do MTK Stuff here 

    def device_details_mtk(self, prop):
        platform = "[ro.board.platform]:"
        cpu = extract(prop, platform, '\n').replace('[', '').replace(']', '').replace('\r', '').upper()
        return cpu


def click_sequence():
    ui.mytext.clear()
    myDevice = AdbDevice()
    mysn = getserialno()
    serial = mysn[1].strip()
    # root = myDevice.root_check()
    partition_list = myDevice.partitions()
    write_to_ui(serial+"\n")
    write_to_ui(str(partition_list))
    # write_to_ui(root)
    if str(mysn[0]).strip() != "1":  # if it is one there is no device
        properties = myDevice.getprop()  # properties inside MTK Qualcomm
        result = myDevice.device_details(properties)
        write_to_ui("Device".ljust(18) + ":" + result[0] + '\n' +
                    "Model".ljust(18)  + ":" + result[1] + '\n' +
                    "Firmware".ljust(16) + ":" + result[2] + '\n' +
                    "Android".ljust(17)  + ":" + result[3] + '\n' +
                    "CPU".ljust(18) + ":" + result[4] + '\n'
                    )
        if int(str(list(result[3])[0])) > 4:
            imei_no = myDevice.imei()
            imei_no = str(filter(str.isdigit, str(imei_no)))
            if imei_no.isdigit():
                write_to_ui("IMEI".ljust(18) + ":" + str(imei_no) + '\n')
            else:
                # MTK Checking here .
                mtk_cpu = myDevice.device_details_mtk(properties)
                if list(mtk_cpu)[1] is "M" and list(mtk_cpu)[2] is "T":  # :))
                    write_to_ui("CPU".ljust(18) + ":" + mtk_cpu + '\n')
                    imei_no1 = myDevice.mtk_imei1()
                    imei_no2 = myDevice.mtk_imei2()
                    write_to_ui("IMEI 1".ljust(18) + ":" + str(imei_no1) + '\n')
                    write_to_ui("IMEI 2".ljust(18) + ":" + str(imei_no2) + '\n')
                else:
                    pass
        else:
            imei_no = myDevice.imei_old()
            write_to_ui("IMEI     : " + str(imei_no) + '\n')
    else:
        write_to_ui('Device Not Found!')

    # DEBUG INFO
    # file = ("log.txt")
    # f = open(file,'w')
    # f.writelines(hi)


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Widget = QtWidgets.QWidget()
    ui = Ui_Widget()
    ui.setupUi(Widget)
    Widget.show()
    sys.exit(app.exec_())
