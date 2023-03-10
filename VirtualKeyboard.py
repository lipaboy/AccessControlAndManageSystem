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
    def do_caps(self):
        # self.timer.start()
        if self.lang == 'ru':
            self.names = self.names_caps_ru
        else:
            self.names = self.names_caps
        self.buttonAdd()
        self.cap_button.setText("Загл")
        self.cap_button.clicked.disconnect()
        self.cap_button.clicked.connect(self.do_small)

    @pyqtSlot()
    def do_small(self):
        # self.timer.stop()
        if self.lang == 'ru':
            self.names = self.names_small_ru
        else:
            self.names = self.names_small
        self.buttonAdd()
        self.cap_button.setText("Обыч")
        self.cap_button.clicked.disconnect()
        self.cap_button.clicked.connect(self.do_caps)

    def initUI(self):
        self.layout = QGridLayout()

        # p = self.palette()
        # p.setColor(self.backgroundRole(),Qt.white)
        # self.setPalette(p)
        self.setAutoFillBackground(True)
        self.text_box = QLineEdit()
        self.text_box.setFont(QFont('Arial', self.FONT_SIZE))
        # text_box.setFixedHeight(50)
        # self.text_box.setFixedWidth(300)
        self.layout.addWidget(self.text_box, 0, 0, 1, 10)

        self.names_caps = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '0', '.', '(', ')',
                           'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M',
                           'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
        self.names_caps_ru = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '0', '.', '(', ')',
                            'А', 'Б', 'В', 'Г', 'Д', 'Е', 'Ж', 'З', 'И', 'Й', 'К', 'Л', 'М',
                            'Н', 'О', 'П', 'Р', 'С', 'Т', 'У', 'Ф', 'Х', 'Ц', 'Ч', 'Ш', 'Щ',
                              ]
        self.names_small = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '0', '.', '(', ')',
                            'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm',
                            'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']
        self.names_small_ru = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '0', '.', '(', ')',
                            'а', 'б', 'в', 'г', 'д', 'е', 'ж', 'з', 'и', 'й', 'к', 'л', 'м',
                            'н', 'о', 'п', 'р', 'с', 'т', 'у', 'ф', 'х', 'ц', 'ч', 'ш', 'щ',
                            # 'ы', 'ь', 'ъ', 'э', 'ю', 'я'
                            ]
        self.names_sym = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '0', '.',
                          '~', '`', '@', '#', '$', '%', '^', '&&', '*', '(',
                          ')', '_', '-', '+', '=', '|', '[', ']', '{', '}', "'",
                          '"', '<', '>', '?', '\\', '/', '!']
        self.names = self.names_small_ru
        self.buttonAdd()

        # Cancel button
        clear_button = QPushButton('Очистить')
        # clear_button.setFixedHeight(25)
        clear_button.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)
        clear_button.setFont(QFont('Arial', self.FONT_SIZE))
        clear_button.KEY_CHAR = Qt.Key_Clear
        self.layout.addWidget(clear_button, 5, 0, 1, 2)
        # self.layout.addWidget(clear_button, 8, 2, 1, 2)
        clear_button.clicked.connect(self.signalMapper.map)
        self.signalMapper.setMapping(clear_button, clear_button.KEY_CHAR)
        # clear_button.setFixedWidth(60)

        # Space button
        space_button = QPushButton('Пробел')
        # space_button.setFixedHeight(25)
        space_button.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)
        space_button.setFont(QFont('Arial', self.FONT_SIZE))
        space_button.KEY_CHAR = Qt.Key_Space
        self.layout.addWidget(space_button, 5, 2, 1, 2)
        # self.layout.addWidget(space_button, 5, 4, 1, 3)
        space_button.clicked.connect(self.signalMapper.map)
        self.signalMapper.setMapping(space_button, space_button.KEY_CHAR)
        # space_button.setFixedWidth(85)

        # Back button
        back_button = QPushButton('Стереть')
        # back_button.setFixedHeight(25)
        back_button.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)
        back_button.setFont(QFont('Arial', self.FONT_SIZE))
        back_button.KEY_CHAR = Qt.Key_Backspace
        self.layout.addWidget(back_button, 5, 4, 1, 2)
        # self.layout.addWidget(back_button, 5, 7, 1, 2)
        back_button.clicked.connect(self.signalMapper.map)
        self.signalMapper.setMapping(back_button, back_button.KEY_CHAR)
        # back_button.setFixedWidth(60)

        # Enter button
        enter_button = QPushButton('Язык')
        # enter_button.setFixedHeight(25)
        enter_button.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)
        enter_button.setFont(QFont('Arial', self.FONT_SIZE))
        enter_button.KEY_CHAR = Qt.Key_Enter
        self.layout.addWidget(enter_button, 5, 6, 1, 2)
        # self.layout.addWidget(enter_button, 5, 9, 1, 2)
        enter_button.clicked.connect(self.signalMapper.map)
        self.signalMapper.setMapping(enter_button, enter_button.KEY_CHAR)
        # enter_button.setFixedWidth(60)

        # Done button
        done_button = QPushButton('Ввод')
        # done_button.setFixedHeight(25)
        done_button.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)
        done_button.setFont(QFont('Arial', self.FONT_SIZE))
        done_button.KEY_CHAR = Qt.Key_Home
        self.layout.addWidget(done_button, 4, 9, 1, 1)
        # self.layout.addWidget(done_button, 5, 11, 1, 2)
        done_button.clicked.connect(self.signalMapper.map)
        self.signalMapper.setMapping(done_button, done_button.KEY_CHAR)
        # done_button.setFixedWidth(60)

        # Done button
        self.cap_button = QPushButton('Загл')
        # self.cap_button.setFixedHeight(25)
        self.cap_button.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)
        self.cap_button.setFont(QFont('Arial', self.FONT_SIZE))
        self.cap_button.KEY_CHAR = Qt.Key_Up
        self.layout.addWidget(self.cap_button, 5, 8, 1, 1)
        # self.layout.addWidget(self.cap_button, 5, 13, 1, 2)
        self.cap_button.clicked.connect(self.signalMapper.map)
        self.signalMapper.setMapping(self.cap_button, self.cap_button.KEY_CHAR)
        # self.cap_button.setFixedWidth(60)
        self.cap_button.clicked.connect(self.do_caps)
        # Done button

        sym_button = QPushButton('Симв')
        self.symbolButton = sym_button
        # sym_button.setFixedHeight(25)
        # sym_button.setFixedWidth(60)
        sym_button.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)
        sym_button.setFont(QFont('Arial', self.FONT_SIZE))
        sym_button.KEY_CHAR = Qt.Key_Down
        self.layout.addWidget(sym_button, 5, 9, 1, 1)
        # self.layout.addWidget(sym_button, 5, 15, 1, 2)
        sym_button.clicked.connect(self.signalMapper.map)
        self.signalMapper.setMapping(sym_button, sym_button.KEY_CHAR)

        self.setGeometry(0, 0, 480, 300)

        self.setLayout(self.layout)

    def buttonAdd(self):
        # self.names = self.names_small
        positions = [(i + 1, j) for i in range(6) for j in range(10)]

        for position, name in zip(positions, self.names):
            if name == '':
                continue
            button = QPushButton(name)
            button.setFont(QFont('Arial', self.FONT_SIZE))
            button.KEY_CHAR = ord(name[-1])
            button.clicked.connect(self.signalMapper.map)
            button.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)
            self.signalMapper.setMapping(button, button.KEY_CHAR)
            self.layout.addWidget(button, *position)

    def buttonClicked(self, char_ord):
        txt = self.text_box.text()
        if char_ord == Qt.Key_Up:
            pass
        elif char_ord == Qt.Key_Down:
            if self.mode == 'Letters':
                self.names = self.names_sym
                self.mode = 'Symbols'
                self.symbolButton.setText('Букв')
            else:
                self.names = self.names_small
                self.mode = 'Letters'
                self.symbolButton.setText('Симв')
            self.buttonAdd()
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
