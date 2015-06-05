'''
@author: Cortez
'''

import sys
import pygame
#from pygame.locals import *
from PyQt4 import QtCore, QtGui, uic
import serial
from serial import *
import serial.tools.list_ports
from threading import Thread
import threading

last_received = ''

class Main(QtCore.QObject):
    
    def killAll(self):
        pygame.quit()
        if self.connected==1:
            self.stop_receive.set()
            self.connected=0
            self.ser.close()  
            print "Disconnected from " + self.ser.portstr   

    def receiving(self, stop_event):
        global last_received
        buffer = ''
        print "receiving"
        while(not stop_event.is_set()):
            # last_received = ser.readline()
            buffer += self.ser.read(self.ser.inWaiting())
            if '\n' in buffer:
                last_received, buffer = buffer.split('\n')[-2:]   
                self.ui.textCOM.append(last_received)
                self.ui.textCOM.verticalScrollBar().setSliderPosition(self.ui.textCOM.verticalScrollBar().maximum()+13)
                print last_received

    
    def __init__(self):
        self.connected=0;
        QtCore.QObject.__init__(self)
        self.ui = uic.loadUi('window.ui', baseinstance=None)
        self.Elements_Init()
        print "Program initialized"
        ports = list(serial.tools.list_ports.comports())
        for p in ports:
            print p
            if "STMicroelectronics" in p[1]:
                self.ui.comboCOM.addItem(p[0]+" VCP")
            else:
                self.ui.comboCOM.addItem(p[0])
        self.ui.textCOM.append('Program initialized')
 
   
        
    def Elements_Init(self):
        self.ui.buttonConnect.clicked.connect(self.buttonConnectClicked)
        self.ui.buttonDisconnect.clicked.connect(self.buttonDisconnectClicked)
        self.ui.buttonEXIT.clicked.connect(self.buttonEXITClicked)
        

        
    def buttonConnectClicked(self):
        self.ser = serial.Serial(int(self.ui.comboCOM.currentText()[3])-1, baudrate=115200)
        print "Connected to " + self.ser.portstr 
        self.ser.write("hello")
        self.connected=1;
        self.ui.buttonConnect.setEnabled(False) 
        self.ui.buttonDisconnect.setEnabled(True)
        self.stop_receive = threading.Event()
        Thread(target=self.receiving, args=(self.stop_receive,)).start()
    
    def buttonDisconnectClicked(self):
        if self.ser.isOpen():
            self.stop_receive.set()
            self.connected=0
            self.ser.close()
            print "Disconnected from " + self.ser.portstr 
        self.ui.buttonConnect.setEnabled(True)
        self.ui.buttonDisconnect.setEnabled(False)
        
    def buttonEXITClicked(self):
        print "Button EXIT Clicked"
        myExitHandler()
        sys.exit()
        


def myExitHandler():
    window.killAll()
    return False

if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    window = Main()
    window.ui.show()
    sys.exit(app.exec_())

