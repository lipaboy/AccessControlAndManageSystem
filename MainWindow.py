import AccessController
import Globals
import Utils
import VirtualKeyboard

from PyQt5 import QtWidgets, QtGui
from PyQt5.QtCore import QSize, pyqtSlot
from PyQt5.QtWidgets import QMainWindow, \
    QPushButton, QVBoxLayout, QHBoxLayout, QSizePolicy
from PyQt5.QtGui import QFont


class MainWindow(QMainWindow):
    def __init__(self, dbFilePath, isFullScreen):
        super().__init__()

        # UI окна

        self.setWindowTitle("Система контроля и управления доступом")
        self.setMinimumSize(QSize(700, 400))
        self.m_isFullScreen = isFullScreen
        self.setStyleSheet("""
            color: rgb(255, 255, 255);
            background-color: %s;
            """ % (Globals.toStr(Globals.WINDOW_BACKGROUND)))
        self.setPalette(QtGui.QPalette(Globals.WINDOW_BACKGROUND))

        # Toolbar

        # self.dataEnterDialog = QtWidgets.QInputDialog()
        # tryToGetAccessAction = QtWidgets.QAction('Получить доступ', self)
        # tryToGetAccessAction.triggered.connect(self.tryToGetAccessDialog)
        #
        # self.getAccessBar = self.addToolBar('Получить доступ')
        # self.getAccessBar.addAction(tryToGetAccessAction)

        # Main layouts

        mainLayout = QVBoxLayout()
        tablesLayout = QHBoxLayout()
        mainLayout.addLayout(tablesLayout)

        workerListLayout = QVBoxLayout()
        tablesLayout.addLayout(workerListLayout, 5)
        historyAccessLayout = QVBoxLayout()
        tablesLayout.addLayout(historyAccessLayout, 4)

        # Список сотрудников

        workerListLayout.addWidget(QtWidgets.QLabel("Список сотрудников"), 0)
        self.workerListTable = QtWidgets.QTableWidget()
        self.workerListTable.setStyleSheet(
            """background-color: %s;"""
            % (Globals.toStr(Globals.TABLE_COLOR)))
        self.mode = 'Edit'
        self.savedCellText = ''
        self.currentEditItem = None
        self.workerListTable.doubleClicked.connect(self.itemStartEditing)
        self.workerListTable.cellChanged.connect(self.changeField)
        # self.workerListTable.itemEn
        # self.workerListTable.setEditTriggers(QtWidgets.QTableWidget.NoEditTriggers)
        # AllEditTriggers
        workerListLayout.addWidget(self.workerListTable, 5)

        # workerListLayout.addStretch(2)
        workerListToolsLayout = QHBoxLayout()
        workerListLayout.addLayout(workerListToolsLayout, 1)

        self.addNewWorkerButton = QPushButton("Добавить")
        self.addNewWorkerButton.clicked.connect(self.addNewRowToWorkerTable)
        self.saveNewWorkerButton = QPushButton("Сохранить")
        self.saveNewWorkerButton.setVisible(False)
        self.saveNewWorkerButton.clicked.connect(self.saveNewWorker)
        self.removeWorkerButton = QPushButton("Удалить")
        self.removeWorkerButton.clicked.connect(self.removeWorker)
        self.cancelAddingNewWorkerButton = QPushButton("Отмена")
        self.cancelAddingNewWorkerButton.setVisible(False)
        self.cancelAddingNewWorkerButton.clicked.connect(self.cancelAdding)

        workerListToolsLayout.addWidget(self.addNewWorkerButton)
        workerListToolsLayout.addWidget(self.saveNewWorkerButton)
        workerListToolsLayout.addWidget(self.cancelAddingNewWorkerButton)
        workerListToolsLayout.addWidget(self.removeWorkerButton)
        Utils.traverseAllWidgetsInLayoutRec(
            workerListToolsLayout,
            lambda but:
            but.setSizePolicy(QSizePolicy.Minimum,
                              QSizePolicy.Expanding))

        Utils.traverseAllWidgetsInLayoutRec(
            workerListToolsLayout,
            lambda but:
            but.setFont(QFont('Arial', 18)))

        # История доступа

        historyAccessLayout.addWidget(QtWidgets.QLabel("История получения доступа сотрудниками"))
        self.historyAccessTable = QtWidgets.QTableWidget()
        self.historyAccessTable.setStyleSheet(
            """background-color: %s;"""
            % (Globals.toStr(Globals.TABLE_COLOR)))
        self.historyAccessTable.setEditTriggers(QtWidgets.QTableWidget.NoEditTriggers)
        historyAccessLayout.addWidget(self.historyAccessTable)

        self.accessController = AccessController.AccessController(dbFilePath)
        self.updateWorkerList()
        self.updateHistory()

        self.keyboard = VirtualKeyboard.KeyboardWidget(self, isFullScreen)
        # self.keyboard.newTextSignal.connect(self.keyboardSlot)
        # mainLayout.addWidget(self.keyboard)

        widget = QtWidgets.QWidget()
        widget.setLayout(mainLayout)
        self.setCentralWidget(widget)

        self.crutch = False

    @pyqtSlot()
    def itemStartEditing(self):
        self.currentEditItem = self.workerListTable.currentItem()
        self.savedCellText = self.currentEditItem.text()
        self.keyboard.m_externalTextBox = self.currentEditItem
        self.keyboard.m_internalTextBox.setText(self.savedCellText)
        if self.m_isFullScreen:
            self.keyboard.showFullScreen()
        else:
            self.keyboard.show()

    @pyqtSlot()
    def itemLeaveEditing(self):
        self.currentEditItem = None

    def setMode(self,
                newMode: str):
        if newMode == 'Edit':
            self.mode = newMode
            self.workerListTable.cellChanged.connect(self.changeField)
            # self.workerListTable.doubleClicked.connect(self.itemStartEditing)
            self.addNewWorkerButton.setVisible(True)
            self.saveNewWorkerButton.setVisible(False)
            self.cancelAddingNewWorkerButton.setVisible(False)
            self.removeWorkerButton.setVisible(True)
        elif newMode == 'Add':
            self.mode = newMode
            self.workerListTable.cellChanged.disconnect()
            # self.workerListTable.doubleClicked.disconnect()
            self.addNewWorkerButton.setVisible(False)
            self.saveNewWorkerButton.setVisible(True)
            self.cancelAddingNewWorkerButton.setVisible(True)
            self.removeWorkerButton.setVisible(False)
        pass

    @pyqtSlot()
    def cancelAdding(self):
        self.workerListTable.removeRow(self.workerListTable.rowCount() - 1)
        self.setMode('Edit')
        pass

    @pyqtSlot()
    def removeWorker(self):
        row = self.workerListTable.currentItem().row()
        cardKey = int(self.workerListTable.item(row, 0).text())
        self.accessController.removeWorker(cardKey)
        self.updateWorkerList()
        pass

    @pyqtSlot()
    def changeField(self):
        item = self.workerListTable.currentItem()
        self.itemLeaveEditing()
        if item:
            newValue = item.text()
            if self.savedCellText != newValue:
                row, column = item.row(), item.column()
                cardKey = int(self.workerListTable.item(row, column - 1).text())
                if column == 1:
                    self.accessController.renameWorker(cardKey, newValue)
                self.updateWorkerList()
                self.updateHistory()

    @pyqtSlot()
    def addNewRowToWorkerTable(self):
        # self.controller.addNewWorkerCard(int(self.keyEdit.text()), self.nameEdit.text(), 1)
        self.setMode('Add')
        table = self.workerListTable
        newRow = table.rowCount()
        table.insertRow(newRow)
        for i in range(0, table.columnCount() - 1):
            table.setItem(newRow, i, QtWidgets.QTableWidgetItem(''))

    def addNewWorker(self,
                     cardId: int):
        self.setMode('Add')
        table = self.workerListTable
        newRow = table.rowCount()
        table.insertRow(newRow)
        table.setItem(newRow, 0, QtWidgets.QTableWidgetItem(str(cardId)))
        for i in range(1, table.columnCount() - 1):
            table.setItem(newRow, i, QtWidgets.QTableWidgetItem(''))
        pass

    @pyqtSlot()
    def saveNewWorker(self):
        table = self.workerListTable
        row = table.rowCount() - 1
        if not table.item(row, 2) is None:
            places = list(map(int, table.item(row, 2).text().split(",")))
        else:
            places = []
        self.accessController.addNewWorkerCard(int(table.item(row, 0).text()),
                                               table.item(row, 1).text(),
                                               places
                                               )
        self.setMode('Edit')

    def updateWorkerList(self):
        workerList = self.accessController.getWorkerList()
        table = self.workerListTable
        table.clear()
        table.setRowCount(len(workerList))
        table.setColumnCount(3)
        table.setHorizontalHeaderLabels(['Ключ', 'Имя сотрудника', 'Разрешённые места'])
        header = table.horizontalHeader()
        header.setSectionResizeMode(0, QtWidgets.QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(1, QtWidgets.QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(2, QtWidgets.QHeaderView.ResizeMode.Stretch)
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
        historyList = self.accessController.getHistory()
        table = self.historyAccessTable
        table.clear()
        table.setRowCount(len(historyList))
        table.setColumnCount(3)
        table.setHorizontalHeaderLabels(['Имя сотрудника', 'Место', 'Время'])
        header = table.horizontalHeader()
        header.setSectionResizeMode(0, QtWidgets.QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(1, QtWidgets.QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(2, QtWidgets.QHeaderView.ResizeMode.Stretch)
        row = 0
        for historyRow in historyList:
            table.setItem(row, 0, QtWidgets.QTableWidgetItem(historyRow[0]))
            table.setItem(row, 1, QtWidgets.QTableWidgetItem(str(historyRow[1])))
            table.setItem(row, 2, QtWidgets.QTableWidgetItem(str(historyRow[2])))
            row += 1

    @pyqtSlot()
    def tryToGetAccessDialog(self):
        self.runKeyboard()

        cardKey, ok1 = QtWidgets.QInputDialog \
            .getInt(self, "Доступ", "Введите ключ карты доступа")
        placeId, ok2 = QtWidgets.QInputDialog \
            .getInt(self, "Доступ", "Введите идентификатор места")

        msg = QtWidgets.QMessageBox(self)
        msg.setWindowTitle("Оповещение")
        if ok1 and ok2:
            if self.accessController.tryToGetAccess(cardKey, placeId):
                msg.setText("Успешно предоставлен доступ")
                self.updateHistory()
            else:
                msg.setText("Доступ запрещён")
            msg.exec()

    def tryToGetAccess(self,
                       cardId: int,
                       placeId: int):
        msg = QtWidgets.QMessageBox(self)
        msg.setWindowTitle("Оповещение")
        if self.accessController.tryToGetAccess(cardId, placeId):
            msg.setText("Успешно предоставлен доступ")
            self.updateHistory()
        else:
            msg.setText("Доступ запрещён")
        msg.exec()

    @pyqtSlot(int)
    def handleCard(self,
                   cardId: int):
        if self.mode == 'Edit' and not self.crutch:
            self.crutch = True
            workers = self.accessController.getWorkerList()
            isFound = False
            for w in workers:
                if w.key == cardId:
                    self.tryToGetAccess(cardId, 1)
                    isFound = True
                    break

            if not isFound:
                msg = QtWidgets.QMessageBox()
                msg.setWindowTitle("Доступ")
                msg.setText("Добавить нового сотрудника?")
                msg.setStandardButtons(msg.StandardButton.Ok | msg.StandardButton.Cancel)
                if msg.exec() == msg.StandardButton.Ok:
                    self.addNewWorker(cardId)
            self.crutch = False
        pass

    def closeEvent(self, a0: QtGui.QCloseEvent) -> None:
        pass
