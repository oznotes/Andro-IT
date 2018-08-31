import os
import re
import sys

from adb_android import *


def clear():
    os.system('cls')


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


class AdbDevice:

    """
    Commands
    """

    get_imei = \
        """
        content query --uri content://settings/system --where "name='bd_setting_i'
        " | sed 's/[^=0-9]*//g' | sed 's/[0-9]*=//g' 
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

    def partitions(self):
        device_partitions = shell(AdbDevice.get_partitions)
        device_partitions = str(device_partitions[1])\
            .replace("\\r", '').replace('\\n', '\n')\
            .replace('major', '\n Partition Table with Details ')\
            .replace('#blocks', '').replace('minor', '')\
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
        firmware = "[ro.build.PDA]: "

        brand = extract(prop, manufacturer, '\n').replace('[', '').replace(']', '').replace('\r', '').upper()
        model = extract(prop, model, '\n').replace('[', '').replace(']', '').replace('\r', '').upper()
        firmware = extract(prop, firmware, '\n').replace('[', '').replace(']', '').replace('\r', '').upper()
        ver = extract(prop, versi, '\n').replace('[', '').replace(']', '').replace('\r', '').upper()
        cpu = extract(prop, board, '\n').replace('[', '').replace(']', '').replace('\r', '').upper()

        return brand, model, firmware, ver, cpu


myDevice = AdbDevice()
result = getserialno()
serial = result[1].strip()
imei = myDevice.imei()

if is_hex(serial) is True:
    properties = myDevice.getprop()
    device = myDevice.device_details(properties)

    print(
            "Device   : " + device[0] + '\n' + \
            "Model    : " + device[1] + '\n' + \
            "Firmware : " + device[2] + '\n' + \
            "Android  : " + device[3] + '\n' + \
            "CPU      : " + device[4] + '\n' + \
            "IMEI     : " + imei
    )
else:
    print ("No Device Here")
