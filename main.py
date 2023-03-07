import subprocess
import sys
import AccessController
import subprocess
import os

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
        workerListLayout = QVBoxLayout()
        mainLayout.addLayout(workerListLayout, 1)
        historyAccessLayout = QVBoxLayout()
        mainLayout.addLayout(historyAccessLayout, 1)

        # Список сотрудников

        workerListLayout.addWidget(QtWidgets.QLabel("Список сотрудников"))
        self.workerListTable = QtWidgets.QTableWidget()
        self.savedCell = ''
        self.mode = 'Edit'
        self.workerListTable.doubleClicked.connect(self.saveCell)
        self.workerListTable.cellChanged.connect(self.changeField)
        # self.workerListTable.setEditTriggers(QtWidgets.QTableWidget.NoEditTriggers)
        workerListLayout.addWidget(self.workerListTable)

        workerListToolsLayout = QHBoxLayout()
        workerListLayout.addLayout(workerListToolsLayout)

        self.addNewWorkerButton = QPushButton("Добавить")
        self.addNewWorkerButton.clicked.connect(self.addNewRowToWorkerTable)
        self.saveNewWorkerButton = QPushButton("Сохранить")
        # self.removeWorkerButton = QPushButton("Сохранить")
        self.saveNewWorkerButton.setEnabled(False)
        self.saveNewWorkerButton.clicked.connect(self.saveNewWorker)
        workerListToolsLayout.addWidget(self.addNewWorkerButton)
        workerListToolsLayout.addWidget(self.saveNewWorkerButton)

        # История доступа

        historyAccessLayout.addWidget(QtWidgets.QLabel("История получения доступа сотрудниками"))
        self.historyAccessTable = QtWidgets.QTableWidget()
        self.historyAccessTable.setEditTriggers(QtWidgets.QTableWidget.NoEditTriggers)
        historyAccessLayout.addWidget(self.historyAccessTable)

        self.controller = AccessController.AccessController()
        self.updateWorkerList()
        self.updateHistory()

        widget = QtWidgets.QWidget()
        widget.setLayout(mainLayout)
        self.setCentralWidget(widget)

    def saveCell(self):
        self.savedCell = self.workerListTable.currentItem().text()

    def changeField(self):
        item = self.workerListTable.currentItem()
        if item:
            newValue = item.text()
            if self.savedCell != newValue:
                row, column = item.row(), item.column()
                cardKey = int(self.workerListTable.item(row, column - 1).text())
                if column == 1:
                    self.controller.renameWorker(cardKey, newValue)
                self.updateWorkerList()
                self.updateHistory()

    def addNewRowToWorkerTable(self):
        # self.controller.addNewWorkerCard(int(self.keyEdit.text()), self.nameEdit.text(), 1)

        self.mode = 'Add'
        self.workerListTable.cellChanged.disconnect()
        self.workerListTable.doubleClicked.disconnect()

        # Запускаем на малине стороннюю виртуальную клавиатуру
        if os.uname()[4].startswith("arm"):
            subprocess.Popen(['/usr/bin/florence'])

        table = self.workerListTable
        newRow = table.rowCount()
        table.insertRow(newRow)

        self.addNewWorkerButton.setEnabled(False)
        self.saveNewWorkerButton.setEnabled(True)

    def saveNewWorker(self):
        table = self.workerListTable
        row = table.rowCount() - 1
        places = list(map(int, table.item(row, 2).text().split(",")))
        self.controller.addNewWorkerCard(int(table.item(row, 0).text()),
                                         table.item(row, 1).text(),
                                         places
                                         )

        self.mode = 'Edit'
        self.workerListTable.cellChanged.connect(self.changeField)
        self.workerListTable.doubleClicked.connect(self.saveCell)
        self.addNewWorkerButton.setEnabled(True)
        self.saveNewWorkerButton.setEnabled(False)

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
                if i < size - 1:
                    placesStr += ","
                i += 1

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
        cardKey, ok1 = QtWidgets.QInputDialog \
            .getInt(self, "Доступ", "Введите ключ карты доступа")
        placeId, ok2 = QtWidgets.QInputDialog \
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
