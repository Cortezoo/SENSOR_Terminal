'''
@author: Cortez
'''

import sys
import pygame
#from pygame.locals import *
from PyQt4 import QtCore, QtGui, uic
from pywinusb import hid
import threading
import thread
import time
from ctypes import *
import struct
from struct import *
from collections import deque
import serial
import serial.tools.list_ports

class Main(QtCore.QObject):
    
    def killAll(self):
        pygame.quit()
        if self.connected:
            self.ser.close()    
    
    def __init__(self):
        QtCore.QObject.__init__(self)
        self.ui = uic.loadUi('window.ui', baseinstance=None)
        self.Elements_Init()
        print "Program initialized"
        ports = list(serial.tools.list_ports.comports())
        for p in ports:
            print p
            self.ui.comboCOM.addItem(p[0])
        self.connected=2;
        
    def Elements_Init(self):
        self.ui.buttonConnect.clicked.connect(self.buttonConnectClicked)
        self.ui.buttonEXIT.clicked.connect(self.buttonEXITClicked)

    def buttonConnectClicked(self):
        print "Button Connect Clicked"
        
        
    def buttonEXITClicked(self):
        print "Button EXIT Clicked"
        #myExitHandler()
        sys.exit()
        


def myExitHandler():
    window.killAll()
    return False

if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    window = Main()
    window.ui.show()
    sys.exit(app.exec_())

