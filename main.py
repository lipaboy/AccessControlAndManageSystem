import sys
import os
import threading
import time

import PyQt5.QtCore
import spidev

from PyQt5.QtCore import QThread, pyqtSlot, pyqtSignal, QObject
from PyQt5.QtWidgets import QApplication
from MainWindow import MainWindow


class SPIScanner(QObject):
    readCardId = pyqtSignal(int)

    def __init__(self):
        super().__init__()

        self.i = 8
        pass

    @pyqtSlot()
    def spiCheck(self):
        if self.i < 10:
            self.i += 1
            self.readCardId.emit(self.i)
        pass


class SPIThread(QThread):
    def __init__(self):
        PyQt5.QtCore.QThread.__init__(self)

        self.spiScanner = None
        self.stopFlag = False

    def stop(self):
        self.stopFlag = True

    def take(self,
             spiObject: QObject):
        self.spiScanner = spiObject
        spiObject.moveToThread(self)

    def run(self) -> None:
        while True:
            time.sleep(5)
            self.spiScanner.spiCheck()
            if self.stopFlag:
                break
        pass


# __main__

app = QApplication(sys.argv)

if len(sys.argv) < 2:
    print('Не передан аргумент: имя файла (.db)')

dbFileName = sys.argv[1]
if not os.path.exists(dbFileName):
    print('Такого файла не существует на диске')

isFullScreen = False if len(sys.argv) < 3 else (sys.argv[2] == 'fullscreen')

thread = SPIThread()

mainWindow = MainWindow(dbFileName, True)
mainWindow.showFullScreen() if isFullScreen else mainWindow.show()

spiScanner = SPIScanner()
spiScanner.readCardId.connect(mainWindow.handleCard)
thread.take(spiScanner)
thread.start()

app.exec()
