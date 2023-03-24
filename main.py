import sys
import os

from MainWindow import MainWindow
from PyQt5.QtWidgets import QApplication

# __main__

app = QApplication(sys.argv)

if len(sys.argv) < 2:
    print('Не передан аргумент: имя файла (.db)')

dbFileName = sys.argv[1]
if not os.path.exists(dbFileName):
    print('Такого файла не существует на диске')

isFullScreen = False if len(sys.argv) < 3 else (sys.argv[2] == 'fullscreen')

window = MainWindow(dbFileName, True)
window.showFullScreen() if isFullScreen else window.show()

app.exec()
