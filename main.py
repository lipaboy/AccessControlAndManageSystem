import sqlite3
import sys

from PyQt5 import QtWidgets
from PyQt5.QtCore import QSize
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton


class AccessController:
    def __init__(self):
        self.connection = sqlite3.connect("AccessWorkerDB.db")
        self.checkAccessRequest = """SELECT * FROM ACCESS_PLACES 
            WHERE card_key = {} AND place_id = {}"""
        self.addNewWorkerCardRequest = """INSERT INTO WORKER_CARDS (key, worker_name) 
            VALUES('{}', '{}')"""
        self.addCardAccessRequest = """INSERT INTO ACCESS_PLACES (card_key, place_id) 
            VALUES('{}', '{}')"""

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


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("My App")
        self.setMinimumSize(QSize(300, 100))

        mainLayout = QtWidgets.QVBoxLayout()

        mainLayout.addWidget(QtWidgets.QLabel("Card Key"))
        self.keyEdit = QtWidgets.QLineEdit()
        mainLayout.addWidget(self.keyEdit)
        mainLayout.addWidget(QtWidgets.QLabel("Worker Name"))
        self.nameEdit = QtWidgets.QLineEdit()
        mainLayout.addWidget(self.nameEdit)

        formLayout = QtWidgets.QHBoxLayout()
        mainLayout.addLayout(formLayout)

        self.checkAccessButton = QPushButton("Check Access")
        self.checkAccessButton.clicked.connect(self.checkAccess)
        formLayout.addWidget(self.checkAccessButton)

        self.addNewWorkerButton = QPushButton("Add New Worker")
        self.addNewWorkerButton.clicked.connect(self.addNewWorkerCard)
        formLayout.addWidget(self.addNewWorkerButton)

        self.controller = AccessController()

        widget = QtWidgets.QWidget()
        widget.setLayout(mainLayout)
        self.setCentralWidget(widget)

    def checkAccess(self):
        # self.checkAccessButton.setText("You already clicked me.")
        # self.checkAccessButton.setEnabled(False)

        if self.controller.hasAccess(int(self.keyEdit.text()), 1) is False:
            self.setWindowTitle("No Access for you")
        else:
            self.setWindowTitle("You can pass through")

    def addNewWorkerCard(self):
        self.controller.addNewWorkerCard(int(self.keyEdit.text()), self.nameEdit.text(), 1)


app = QApplication(sys.argv)

window = MainWindow()
window.show()

app.exec()
