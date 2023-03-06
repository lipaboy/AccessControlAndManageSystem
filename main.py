import sys
import sqlite3
import datetime
import AccessController

from PyQt5 import QtWidgets
from PyQt5 import QtGui
from PyQt5.QtCore import QSize
from PyQt5.QtWidgets import QApplication, QMainWindow, \
    QPushButton, QVBoxLayout, QHBoxLayout



class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("My App")
        self.setMinimumSize(QSize(700, 400))

        self.dataEnterDialog = QtWidgets.QInputDialog()
        tryToGetAccessAction = QtWidgets.QAction('Получить доступ', self)
        tryToGetAccessAction.triggered.connect(self.tryToGetAccess)

        self.getAccessBar = self.addToolBar('Получить доступ')
        self.getAccessBar.addAction(tryToGetAccessAction)

        mainLayout = QHBoxLayout()

        listWorkerLayout = QVBoxLayout()
        mainLayout.addLayout(listWorkerLayout, 1)

        listWorkerLayout.addWidget(QtWidgets.QLabel("Список сотрудников"))
        self.workerListTable = QtWidgets.QTableWidget()
        listWorkerLayout.addWidget(self.workerListTable)

        historyAccessLayout = QVBoxLayout()
        mainLayout.addLayout(historyAccessLayout, 1)

        historyAccessLayout.addWidget(QtWidgets.QLabel("История получения доступа сотрудниками"))
        self.historyAccessTable = QtWidgets.QTableWidget()
        historyAccessLayout.addWidget(self.historyAccessTable)

        self.controller = AccessController.AccessController()
        self.updateWorkerList()
        self.updateHistory()

        widget = QtWidgets.QWidget()
        widget.setLayout(mainLayout)
        self.setCentralWidget(widget)

    def addNewWorkerCard(self):
        self.controller.addNewWorkerCard(int(self.keyEdit.text()), self.nameEdit.text(), 1)

    def updateWorkerList(self):
        workerList = self.controller.getWorkerList()
        table = self.workerListTable
        table.clear()
        table.setRowCount(len(workerList))
        table.setColumnCount(3)
        table.setHorizontalHeaderLabels(['Ключ', 'Имя сотрудника', 'Разрешённые места'])
        header = table.horizontalHeader()
        header.setSectionResizeMode(0, QtWidgets.QHeaderView.ResizeMode.Stretch)
        header.setSectionResizeMode(1, QtWidgets.QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(2, QtWidgets.QHeaderView.ResizeMode.ResizeToContents)
        row = 0
        for workerRow in workerList:
            table.setItem(row, 0, QtWidgets.QTableWidgetItem(str(workerRow.key)))
            table.setItem(row, 1, QtWidgets.QTableWidgetItem(workerRow.name))

            placesStr = ''
            size = len(workerRow.places)
            i = 0
            for placeId in workerRow.places:
                placesStr += str(placeId)
                i += 1
                if i < size - 1:
                    placesStr += ","

            table.setItem(row, 2, QtWidgets.QTableWidgetItem(placesStr))
            row += 1

    def updateHistory(self):
        historyList = self.controller.getHistory()
        table = self.historyAccessTable
        table.clear()
        table.setRowCount(len(historyList))
        table.setColumnCount(3)
        table.setHorizontalHeaderLabels(['Имя сотрудника', 'Место', 'Время'])
        header = table.horizontalHeader()
        header.setSectionResizeMode(0, QtWidgets.QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(1, QtWidgets.QHeaderView.ResizeMode.Stretch)
        header.setSectionResizeMode(2, QtWidgets.QHeaderView.ResizeMode.ResizeToContents)
        row = 0
        for historyRow in historyList:
            table.setItem(row, 0, QtWidgets.QTableWidgetItem(historyRow[0]))
            table.setItem(row, 1, QtWidgets.QTableWidgetItem(str(historyRow[1])))
            table.setItem(row, 2, QtWidgets.QTableWidgetItem(str(historyRow[2])))
            row += 1

    def tryToGetAccess(self):
        cardKey, ok1 = QtWidgets.QInputDialog\
            .getInt(self, "Доступ", "Введите ключ карты доступа")
        placeId, ok2 = QtWidgets.QInputDialog\
            .getInt(self, "Доступ", "Введите идентификатор места")

        msg = QtWidgets.QMessageBox(self)
        msg.setWindowTitle("Оповещение")
        if ok1 and ok2:
            if self.controller.tryToGetAccess(cardKey, placeId):
                msg.setText("Успешно предоставлен доступ")
                self.updateHistory()
            else:
                msg.setText("Доступ запрещён")
            msg.exec()



app = QApplication(sys.argv)

window = MainWindow()
window.show()

app.exec()
