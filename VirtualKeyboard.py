import sys
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.Qt import Qt
from PyQt5.QtWidgets import *

import Globals
from Utils import *


class KeyboardWidget(QDialog):
    def __init__(self, parent=None, isFullScreen=False):
        super(KeyboardWidget, self).__init__(parent)

        self.enCapsKeys = None
        self.enSmallKeys = None
        self.ruCapsKeys = None
        self.ruSmallKeys = None
        self.mainLayout = None
        self.m_internalTextBox = None
        self.symKeys = None
        self.m_externalTextBox = None

        self.signalMapper = QSignalMapper(self)
        self.signalMapper.mapped[int].connect(self.buttonClicked)

        self.FONT_SIZE = 18 if not isFullScreen else 30
        self.m_isFullScreen = isFullScreen

        self.m_currentKeyLayout = None
        self.m_previousKeyLayout = None

        palette = QPalette(Globals.WINDOW_BACKGROUND)
        self.setPalette(palette)
        self.initUI()

    def initUI(self):
        self.mainLayout = QVBoxLayout()

        # p = self.palette()
        # p.setColor(self.backgroundRole(),Qt.white)
        # self.setPalette(p)
        self.setAutoFillBackground(True)
        self.m_internalTextBox = QLineEdit()
        self.m_internalTextBox.setFont(QFont('Arial', self.FONT_SIZE))
        self.m_internalTextBox.setStyleSheet("""
            border: 2px solid %s;""" % (Globals.toStr(Globals.BORDER_COLOR)))
        # text_box.setFixedHeight(50)
        # self.text_box.setFixedWidth(300)

        self.mainLayout.addWidget(self.m_internalTextBox)

        digitsBase = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '0']

        # Нельзя переместить раскладки клавиш из полей класса в локальные переменные

        namesSmallRu = \
            [
                ['й', 'ц', 'у', 'к', 'е', 'н', 'г', 'ш', 'щ', 'з', 'х', 'ъ'],
                ['ф', 'ы', 'в', 'а', 'п', 'р', 'о', 'л', 'д', 'ж', 'э'],
                ['я', 'ч', 'с', 'м', 'и', 'т', 'ь', 'б', 'ю'],
            ]
        namesSmallRu.insert(0, digitsBase)
        self.ruSmallKeys = self.createKeyboardLayout(
            namesSmallRu, False,
            lambda: self.showKeyLayout(self.ruCapsKeys),
            lambda: self.showKeyLayout(self.enSmallKeys)
        )
        self.mainLayout.addWidget(self.ruSmallKeys)
        self.ruSmallKeys.setVisible(False)

        namesCapsRu = \
            [
                ['Й', 'Ц', 'У', 'К', 'Е', 'Н', 'Г', 'Ш', 'Щ', 'З', 'Х', 'Ъ'],
                ['Ф', 'Ы', 'В', 'А', 'П', 'Р', 'О', 'Л', 'Д', 'Ж', 'Э'],
                ['Я', 'Ч', 'С', 'М', 'И', 'Т', 'Ь', 'Б', 'Ю'],
            ]
        namesCapsRu.insert(0, digitsBase)
        self.ruCapsKeys = self.createKeyboardLayout(
            namesCapsRu, True,
            lambda: self.showKeyLayout(self.ruSmallKeys),
            lambda: self.showKeyLayout(self.enCapsKeys)
        )
        self.mainLayout.addWidget(self.ruCapsKeys)
        self.ruCapsKeys.setVisible(False)

        namesSmallEn = \
            [
                ['q', 'w', 'e', 'r', 't', 'y', 'u', 'i', 'o', 'p'],
                ['a', 's', 'd', 'f', 'g', 'h', 'j', 'k', 'l'],
                ['z', 'x', 'c', 'v', 'b', 'n', 'm'],
            ]
        namesSmallEn.insert(0, digitsBase)
        self.enSmallKeys = self.createKeyboardLayout(
            namesSmallEn, False,
            lambda: self.showKeyLayout(self.enCapsKeys),
            lambda: self.showKeyLayout(self.ruSmallKeys)
        )
        self.mainLayout.addWidget(self.enSmallKeys)
        self.enSmallKeys.setVisible(False)

        namesCapsEn = \
            [
                ['Q', 'W', 'E', 'R', 'T', 'Y', 'U', 'I', 'O', 'P'],
                ['A', 'S', 'D', 'F', 'G', 'H', 'J', 'K', 'L'],
                ['Z', 'X', 'C', 'V', 'B', 'N', 'M'],
            ]
        namesCapsEn.insert(0, digitsBase)
        self.enCapsKeys = self.createKeyboardLayout(
            namesCapsEn, True,
            lambda: self.showKeyLayout(self.enSmallKeys),
            lambda: self.showKeyLayout(self.ruCapsKeys)
        )
        self.mainLayout.addWidget(self.enCapsKeys)
        self.enCapsKeys.setVisible(False)

        namesSym = \
            [
                ['~', '`', '@', '#', '$', '%', '^', '&&', '*', '('],
                [')', '_', '-', '+', '=', '|', '[', ']', '{', '}', "'"],
                ['"', '<', '>', '?', '\\', '/', '!'],
            ]
        namesSym.insert(0, digitsBase)
        self.symKeys = self.createKeyboardLayout(
            namesSym, True,
            lambda: None,
            lambda: None,
            True,
            lambda selfRef: selfRef.showKeyLayout(selfRef.m_previousKeyLayout)
        )
        self.mainLayout.addWidget(self.symKeys)
        self.symKeys.setVisible(False)

        self.showKeyLayout(self.ruSmallKeys)

        # Cancel button
        clear_button = QPushButton('Очистить')
        # clear_button.setFixedHeight(25)
        clear_button.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)
        clear_button.setFont(QFont('Arial', self.FONT_SIZE))
        clear_button.KEY_CHAR = Qt.Key_Clear
        clear_button.clicked.connect(self.signalMapper.map)
        self.signalMapper.setMapping(clear_button, clear_button.KEY_CHAR)
        # clear_button.setFixedWidth(60)

        self.setGeometry(0, 0, 480, 300)

        self.setLayout(self.mainLayout)

    @pyqtSlot()
    def showKeyLayout(self,
                      widget: QWidget):
        self.m_previousKeyLayout = self.m_currentKeyLayout
        if self.m_currentKeyLayout is not None:
            self.m_currentKeyLayout.setVisible(False)
        self.m_currentKeyLayout = widget
        self.m_currentKeyLayout.setVisible(True)
        self.m_currentKeyLayout.setFocus()

    def createKeyboardLayout(self,
                             keyNames: list,
                             isCaps: bool,
                             registerChangeFunc,
                             langChangeFunc,
                             isSymb: bool = False,
                             symbolChangeLayoutFunc=
                             lambda selfRef:
                             selfRef.showKeyLayout(selfRef.symKeys)):
        widget = QWidget()
        layout = QVBoxLayout(widget)

        # Register button
        changeRegisterButton = QPushButton('Обыч' if isCaps else 'Загл')
        changeRegisterButton.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)
        changeRegisterButton.setFont(QFont('Arial', self.FONT_SIZE))
        changeRegisterButton.clicked.connect(registerChangeFunc)

        # Language button
        langButton = QPushButton('Язык')
        langButton.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)
        langButton.setFont(QFont('Arial', self.FONT_SIZE))
        langButton.clicked.connect(langChangeFunc)

        # Space button
        spaceButton = QPushButton('Пробел')
        spaceButton.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)
        spaceButton.setFont(QFont('Arial', self.FONT_SIZE))
        spaceButton.KEY_CHAR = Qt.Key_Space
        spaceButton.clicked.connect(self.signalMapper.map)
        self.signalMapper.setMapping(spaceButton, spaceButton.KEY_CHAR)

        # Back button
        eraseButton = QPushButton('Стереть')
        eraseButton.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)
        eraseButton.setFont(QFont('Arial', self.FONT_SIZE))
        eraseButton.KEY_CHAR = Qt.Key_Backspace
        eraseButton.clicked.connect(self.signalMapper.map)
        self.signalMapper.setMapping(eraseButton, eraseButton.KEY_CHAR)

        row = 0
        maxLetters = 0
        buttonList = []
        for namesRow in keyNames:
            hBox = QHBoxLayout()
            layout.addLayout(hBox)
            # hBox.setContentsMargins(50, 0, 50, 0)
            # hBox.setSpacing(0)

            if row == 3 and not isSymb:
                hBox.addWidget(changeRegisterButton, 2)
            else:
                hBox.addStretch(1)
            # hBox.insertSpacing(0, 20)

            countLettersInRow = 0
            for name in namesRow:
                if name == '':
                    continue
                button = QPushButton(name)
                button.setFont(QFont('Arial', self.FONT_SIZE))
                button.KEY_CHAR = ord(name[-1])
                button.clicked.connect(self.signalMapper.map)
                if self.m_isFullScreen:
                    button.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Fixed)
                else:
                    button.setSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Minimum)
                # button.setFixedWidth(100)
                self.signalMapper.setMapping(button, button.KEY_CHAR)

                hBox.addWidget(button)
                countLettersInRow += 1
                buttonList.append(button)

            if maxLetters < countLettersInRow:
                maxLetters = countLettersInRow

            if row == 3:
                hBox.addWidget(eraseButton, 2)
            else:
                hBox.addStretch(1)

            row += 1

        if self.m_isFullScreen:
            screenSize = QApplication.primaryScreen().size()
            buttonSize = QSize(
                int(screenSize.width() / (maxLetters if maxLetters > 0 else 15)) - 10,
                int((screenSize.height()) / 6))
            # 170)
            font = QFont('Arial')
            font.setPixelSize(min(buttonSize.width() - 20, buttonSize.height() - 20))
            for but in buttonList:
                but.setFixedSize(buttonSize)
                but.setFont(font)

        # Done button
        applyButton = QPushButton('ОК')
        applyButton.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)
        applyButton.setFont(QFont('Arial', self.FONT_SIZE))
        applyButton.KEY_CHAR = Qt.Key_Home
        applyButton.clicked.connect(self.signalMapper.map)
        self.signalMapper.setMapping(applyButton, applyButton.KEY_CHAR)

        # Done button
        cancelButton = QPushButton('Отмена')
        cancelButton.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)
        cancelButton.setFont(QFont('Arial', self.FONT_SIZE))
        cancelButton.clicked.connect(lambda: self.hide())

        symbolButton = QPushButton('Симв' if isSymb else 'Букв')
        symbolButton.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)
        symbolButton.setFont(QFont('Arial', self.FONT_SIZE))
        symbolButton.clicked.connect(lambda: symbolChangeLayoutFunc(self))

        hBox = QHBoxLayout()
        hBox.addWidget(symbolButton, 1)
        if not isSymb:
            hBox.addWidget(langButton, 1)
        hBox.addWidget(spaceButton, 10)
        hBox.addWidget(cancelButton, 2)
        hBox.addWidget(applyButton, 2)
        layout.addLayout(hBox)

        traverseAllWidgetsInLayoutRec(
            layout,
            lambda w: w.setStyleSheet("""
                        color: rgb(255, 255, 255);
                        background-color: qlineargradient(
                            x1: 0, y1: 0.2, x2: 1, y2: 1,
                            stop: 0 rgba(%s, %s, %s, 255), 
                            stop: 1 rgba(%s, %s, %s, 255));
                            border: 2px solid black
                    """ % (105, 109, 120, 63, 69, 75)))

        return widget

    def buttonClicked(self, char_ord):
        txt = self.m_internalTextBox.text()

        if char_ord == Qt.Key_Backspace:
            txt = txt[:-1]
        elif char_ord == Qt.Key_Home:
            self.m_externalTextBox.setText(txt)
            self.hide()
            return
        elif char_ord == Qt.Key_Clear:
            txt = ""
        elif char_ord == Qt.Key_Space:
            txt += ' '
        else:
            txt += chr(char_ord)

        self.m_internalTextBox.setText(txt)
