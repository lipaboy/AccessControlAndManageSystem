import sys
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.Qt import Qt
from PyQt5.QtWidgets import *


class KeyboardWidget(QDialog):
    def __init__(self, parent=None):
        super(KeyboardWidget, self).__init__(parent)
        self.currentTextBox = None

        self.signalMapper = QSignalMapper(self)
        self.signalMapper.mapped[int].connect(self.buttonClicked)

        self.FONT_SIZE = 18
        self.mode = 'Letters'
        self.lang = 'ru'

        self.initUI()

    @pyqtSlot()
    def showKeyboardLayout(self,
                           widget: QWidget):
        self.currentWidget.setVisible(False)
        self.currentWidget = widget
        self.currentWidget.setVisible(True)
        self.currentWidget.setFocus()

    def initUI(self):
        self.layout = QVBoxLayout()

        # p = self.palette()
        # p.setColor(self.backgroundRole(),Qt.white)
        # self.setPalette(p)
        self.setAutoFillBackground(True)
        self.text_box = QLineEdit()
        self.text_box.setFont(QFont('Arial', self.FONT_SIZE))
        # text_box.setFixedHeight(50)
        # self.text_box.setFixedWidth(300)

        self.layout.addWidget(self.text_box)

        self.digitsBase = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '0']

        self.namesCapsEn = \
            [
                ['Q', 'W', 'E', 'R', 'T', 'Y', 'U', 'I', 'O', 'P'],
                ['A', 'S', 'D', 'F', 'G', 'H', 'J', 'K', 'L'],
                ['Z', 'X', 'C', 'V', 'B', 'N', 'M'],
            ]
        self.namesCapsEn.insert(0, self.digitsBase)

        self.namesSmallEn = \
            [
                ['q', 'w', 'e', 'r', 't', 'y', 'u', 'i', 'o', 'p'],
                ['a', 's', 'd', 'f', 'g', 'h', 'j', 'k', 'l'],
                ['z', 'x', 'c', 'v', 'b', 'n', 'm'],
            ]
        self.namesSmallEn.insert(0, self.digitsBase)

        self.namesCapsRu = \
            [
                ['Й', 'Ц', 'У', 'К', 'Е', 'Н', 'Г', 'Ш', 'Щ', 'З', 'Х', 'Ъ'],
                ['Ф', 'Ы', 'В', 'А', 'П', 'Р', 'О', 'Л', 'Д', 'Ж', 'Э'],
                ['Я', 'Ч', 'С', 'М', 'И', 'Т', 'Ь', 'Б', 'Ю'],
            ]
        self.namesCapsRu.insert(0, self.digitsBase)
        self.namesSmallRu = \
            [
                ['й', 'ц', 'у', 'к', 'е', 'н', 'г', 'ш', 'щ', 'з', 'х', 'ъ'],
                ['ф', 'ы', 'в', 'а', 'п', 'р', 'о', 'л', 'д', 'ж', 'э'],
                ['я', 'ч', 'с', 'м', 'и', 'т', 'ь', 'б', 'ю'],
            ]
        self.namesSmallRu.insert(0, self.digitsBase)
        self.names_sym = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '0', '.',
                          '~', '`', '@', '#', '$', '%', '^', '&&', '*', '(',
                          ')', '_', '-', '+', '=', '|', '[', ']', '{', '}', "'",
                          '"', '<', '>', '?', '\\', '/', '!']

        self.names = self.namesSmallRu


        self.widgetSmallRu = self.createKeyboardLayout(
            self.namesSmallRu, False,
            lambda: self.showKeyboardLayout(self.widgetCapsRu),
            lambda: self.showKeyboardLayout(self.widgetSmallEn)
        )
        self.layout.addWidget(self.widgetSmallRu)
        self.widgetCapsRu = self.createKeyboardLayout(
            self.namesCapsRu, True,
            lambda: self.showKeyboardLayout(self.widgetSmallRu),
            lambda: self.showKeyboardLayout(self.widgetCapsEn)
        )
        self.layout.addWidget(self.widgetCapsRu)
        self.widgetCapsRu.setVisible(False)
        self.widgetSmallEn = self.createKeyboardLayout(
            self.namesSmallEn, False,
            lambda: self.showKeyboardLayout(self.widgetCapsEn),
            lambda: self.showKeyboardLayout(self.widgetSmallRu)
        )
        self.layout.addWidget(self.widgetSmallEn)
        self.widgetSmallEn.setVisible(False)
        self.widgetCapsEn = self.createKeyboardLayout(
            self.namesCapsEn, True,
            lambda: self.showKeyboardLayout(self.widgetSmallEn),
            lambda: self.showKeyboardLayout(self.widgetCapsRu)
        )
        self.layout.addWidget(self.widgetCapsEn)
        self.widgetCapsEn.setVisible(False)

        self.currentWidget = self.widgetSmallRu

        # Cancel button
        clear_button = QPushButton('Очистить')
        # clear_button.setFixedHeight(25)
        clear_button.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)
        clear_button.setFont(QFont('Arial', self.FONT_SIZE))
        clear_button.KEY_CHAR = Qt.Key_Clear
        # self.layout.addWidget(clear_button, 5, 0, 1, 2)
        # self.layout.addWidget(clear_button, 8, 2, 1, 2)
        clear_button.clicked.connect(self.signalMapper.map)
        self.signalMapper.setMapping(clear_button, clear_button.KEY_CHAR)
        # clear_button.setFixedWidth(60)


        # Back button
        back_button = QPushButton('Стереть')
        # back_button.setFixedHeight(25)
        back_button.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)
        back_button.setFont(QFont('Arial', self.FONT_SIZE))
        back_button.KEY_CHAR = Qt.Key_Backspace
        # self.layout.addWidget(back_button, 5, 4, 1, 2)
        # self.layout.addWidget(back_button, 5, 7, 1, 2)
        back_button.clicked.connect(self.signalMapper.map)
        self.signalMapper.setMapping(back_button, back_button.KEY_CHAR)
        # back_button.setFixedWidth(60)


        # Done button
        done_button = QPushButton('Ввод')
        # done_button.setFixedHeight(25)
        done_button.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)
        done_button.setFont(QFont('Arial', self.FONT_SIZE))
        done_button.KEY_CHAR = Qt.Key_Home
        # self.layout.addWidget(done_button, 4, 9, 1, 1)
        # self.layout.addWidget(done_button, 5, 11, 1, 2)
        done_button.clicked.connect(self.signalMapper.map)
        self.signalMapper.setMapping(done_button, done_button.KEY_CHAR)
        # done_button.setFixedWidth(60)


        sym_button = QPushButton('Симв')
        self.symbolButton = sym_button
        # sym_button.setFixedHeight(25)
        # sym_button.setFixedWidth(60)
        sym_button.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)
        sym_button.setFont(QFont('Arial', self.FONT_SIZE))
        sym_button.KEY_CHAR = Qt.Key_Down
        # self.layout.addWidget(sym_button, 5, 9, 1, 1)
        # self.layout.addWidget(sym_button, 5, 15, 1, 2)
        sym_button.clicked.connect(self.signalMapper.map)
        self.signalMapper.setMapping(sym_button, sym_button.KEY_CHAR)

        self.setGeometry(0, 0, 480, 300)

        self.setLayout(self.layout)

    def createKeyboardLayout(self,
                             symbolNames: list,
                             isCaps: bool,
                             registerChangeFunc,
                             langChangeFunc):
        widget = QWidget()
        layout = QVBoxLayout(widget)

        # Done button
        self.changeRegisterButton = QPushButton('Обыч' if isCaps else 'Загл')
        self.changeRegisterButton.clicked.connect(registerChangeFunc)
        # self.cap_button.setFixedHeight(25)
        self.changeRegisterButton.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)
        self.changeRegisterButton.setFont(QFont('Arial', self.FONT_SIZE))
        self.changeRegisterButton.clicked.connect(self.signalMapper.map)
        # self.cap_button.setFixedWidth(60)
        # Done button

        # Enter button
        langButton = QPushButton('Язык')
        # enter_button.setFixedHeight(25)
        langButton.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)
        langButton.setFont(QFont('Arial', self.FONT_SIZE))
        langButton.clicked.connect(langChangeFunc)
        # langButton.KEY_CHAR = Qt.Key_Enter
        # langButton.clicked.connect(self.signalMapper.map)
        # self.signalMapper.setMapping(langButton, langButton.KEY_CHAR)
        # enter_button.setFixedWidth(60)

        # Space button
        spaceButton = QPushButton('Пробел')
        # space_button.setFixedHeight(25)
        spaceButton.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)
        spaceButton.setFont(QFont('Arial', self.FONT_SIZE))
        spaceButton.KEY_CHAR = Qt.Key_Space
        spaceButton.clicked.connect(self.signalMapper.map)
        self.signalMapper.setMapping(spaceButton, spaceButton.KEY_CHAR)
        # space_button.setFixedWidth(85)

        row = 0
        for namesRow in symbolNames:
            hBox = QHBoxLayout()
            layout.addLayout(hBox)
            # hBox.setContentsMargins(50, 0, 50, 0)
            # hBox.setSpacing(0)
            if row == 3:
                hBox.addWidget(self.changeRegisterButton)

            for name in namesRow:
                if name == '':
                    continue
                button = QPushButton(name)
                button.setFont(QFont('Arial', self.FONT_SIZE))
                button.KEY_CHAR = ord(name[-1])
                button.clicked.connect(self.signalMapper.map)
                button.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)
                self.signalMapper.setMapping(button, button.KEY_CHAR)

                hBox.addWidget(button)

            row += 1

        hBox = QHBoxLayout()
        hBox.addWidget(langButton, 1)
        hBox.addWidget(spaceButton, 10)
        layout.addLayout(hBox)

        return widget

    def buttonClicked(self, char_ord):
        txt = self.text_box.text()
        if char_ord == Qt.Key_Down:
            if self.mode == 'Letters':
                self.names = self.names_sym
                self.mode = 'Symbols'
                self.symbolButton.setText('Букв')
            else:
                self.names = self.names_small
                self.mode = 'Letters'
                self.symbolButton.setText('Симв')
            self.createKeyboardLayout()
        elif char_ord == Qt.Key_Backspace:
            txt = txt[:-1]
        elif char_ord == Qt.Key_Enter:
            if self.lang == 'ru':
                self.lang = 'en'
                self.do_small()
            else:
                self.lang = 'ru'
                self.do_small()
        #     txt += chr(10)
        elif char_ord == Qt.Key_Home:
            self.currentTextBox.setText(txt)
            # self.text_box.setText("")
            self.hide()
            return
        elif char_ord == Qt.Key_Clear:
            txt = ""
        elif char_ord == Qt.Key_Space:
            txt += ' '
        else:
            txt += chr(char_ord)

        self.text_box.setText(txt)
