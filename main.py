import sys
import sqlite3
import datetime

from PyQt5 import QtWidgets
from PyQt5 import QtGui
from PyQt5.QtCore import QSize
from PyQt5.QtWidgets import QApplication, QMainWindow, \
    QPushButton, QVBoxLayout, QHBoxLayout


class AccessController:
    def __init__(self):
        self.connection = sqlite3.connect("AccessWorkerDB.db")
        self.checkAccessRequest = """
            SELECT * 
            FROM ACCESS_PLACES 
            WHERE card_key = {} AND place_id = {}"""
        self.addNewWorkerCardRequest = """
            INSERT INTO WORKER_CARDS 
            (key, worker_name) 
            VALUES('{}', '{}')"""
        self.addCardAccessRequest = """
            INSERT INTO ACCESS_PLACES 
            (card_key, place_id) 
            VALUES('{}', '{}')"""
        self.getWorkerListRequest = """
            SELECT * 
            FROM WORKER_CARDS"""
        self.addNewAccessToPlace = """
            INSERT INTO HISTORY 
            (card_key, place_id, time) 
            VALUES(?, ?, ?)"""

    def hasAccess(self,
                  cardKey: int,
                  placeId: int) -> bool:
        result = self.connection.cursor().execute(
            self.checkAccessRequest.format(cardKey, placeId)
        ).fetchone()
        if result is None:
            return False
        return True

    def addNewWorkerCard(self,
                         cardKey: int,
                         workerName: str,
                         placeId: int):
        cursor = self.connection.cursor()
        cursor.execute(
            self.addNewWorkerCardRequest.format(cardKey, workerName)
        )
        cursor.execute(
            self.addCardAccessRequest.format(cardKey, placeId)
        )
        self.connection.commit()

    def tryToGetAccess(self,
                       cardKey: int,
                       placeId: int) -> bool:
        cursor = self.connection.cursor()
        if self.hasAccess(cardKey, placeId):
            cursor.execute(self.addNewAccessToPlace, (cardKey, placeId, datetime.datetime.now()))
            return True
        return False

    def getWorkerList(self) -> list:
        cursor = self.connection.cursor()
        cursor.execute(self.getWorkerListRequest)
        return cursor.fetchall()


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("My App")
        self.setMinimumSize(QSize(600, 400))

        self.dataEnterDialog = QtWidgets.QInputDialog()
        tryToGetAccessAction = QtWidgets.QAction('Получить доступ', self)
        tryToGetAccessAction.triggered.connect(self.tryToGetAccess)

        self.getAccessBar = self.addToolBar('Получить доступ')
        self.getAccessBar.addAction(tryToGetAccessAction)

        mainLayout = QHBoxLayout()

        listWorkerLayout = QVBoxLayout()
        mainLayout.addLayout(listWorkerLayout)

        listWorkerLayout.addWidget(QtWidgets.QLabel("Список сотрудников"))
        self.workerListTable = QtWidgets.QTableWidget(0, 2)
        listWorkerLayout.addWidget(self.workerListTable)

        historyAccessLayout = QVBoxLayout()
        mainLayout.addLayout(historyAccessLayout)

        historyAccessLayout.addWidget(QtWidgets.QLabel("История получения доступа сотрудниками"))
        self.historyAccessTable = QtWidgets.QTableWidget(0, 3)
        historyAccessLayout.addWidget(self.historyAccessTable)

        self.controller = AccessController()
        self.updateWorkerList()

        widget = QtWidgets.QWidget()
        widget.setLayout(mainLayout)
        self.setCentralWidget(widget)


    def checkAccess(self):
        if self.controller.hasAccess(int(self.keyEdit.text()), 1) is False:
            self.setWindowTitle("No Access for you")
        else:
            self.setWindowTitle("You can pass through")

    def addNewWorkerCard(self):
        self.controller.addNewWorkerCard(int(self.keyEdit.text()), self.nameEdit.text(), 1)

    def updateWorkerList(self):
        workerList = self.controller.getWorkerList()
        table = self.workerListTable
        table.clear()
        table.setRowCount(len(workerList))
        table.setColumnCount(2)
        table.setHorizontalHeaderLabels(['Ключ', 'Имя сотрудника'])
        header = table.horizontalHeader()
        header.setSectionResizeMode(0, QtWidgets.QHeaderView.ResizeMode.Stretch)
        header.setSectionResizeMode(1, QtWidgets.QHeaderView.ResizeMode.Stretch)
        row = 0
        for workerRow in workerList:
            self.workerListTable.setItem(row, 0, QtWidgets.QTableWidgetItem(str(workerRow[0])))
            self.workerListTable.setItem(row, 1, QtWidgets.QTableWidgetItem(str(workerRow[1])))
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
            else:
                msg.setText("Доступ запрещён")
            msg.exec()



app = QApplication(sys.argv)

window = MainWindow()
window.show()

app.exec()
