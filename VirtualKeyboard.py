import sys
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.Qt import Qt
from PyQt5.QtWidgets import *
from Utils import *


class KeyboardWidget(QDialog):
    def __init__(self, parent=None, isFullScreen=False):
        super(KeyboardWidget, self).__init__(parent)
        self.m_externalTextBox = None

        self.signalMapper = QSignalMapper(self)
        self.signalMapper.mapped[int].connect(self.buttonClicked)

        self.FONT_SIZE = 18 if not isFullScreen else 30
        self.m_isFullScreen = isFullScreen

        self.initUI()

    def initUI(self):
        self.layout = QVBoxLayout()

        # p = self.palette()
        # p.setColor(self.backgroundRole(),Qt.white)
        # self.setPalette(p)
        self.setAutoFillBackground(True)
        self.m_internalTextBox = QLineEdit()
        self.m_internalTextBox.setFont(QFont('Arial', self.FONT_SIZE))
        # text_box.setFixedHeight(50)
        # self.text_box.setFixedWidth(300)

        self.layout.addWidget(self.m_internalTextBox)

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


        self.widgetSmallRu = self.createKeyboardLayout(
            self.namesSmallRu, False,
            lambda: self.showKeyboardLayout(self.widgetCapsRu),
            lambda: self.showKeyboardLayout(self.widgetSmallEn)
        )
        self.layout.addWidget(self.widgetSmallRu)
        self.widgetSmallRu.setVisible(False)
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
        self.currentWidget.setVisible(True)

        # Cancel button
        clear_button = QPushButton('Очистить')
        # clear_button.setFixedHeight(25)
        clear_button.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)
        clear_button.setFont(QFont('Arial', self.FONT_SIZE))
        clear_button.KEY_CHAR = Qt.Key_Clear
        clear_button.clicked.connect(self.signalMapper.map)
        self.signalMapper.setMapping(clear_button, clear_button.KEY_CHAR)
        # clear_button.setFixedWidth(60)

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

    @pyqtSlot()
    def showKeyboardLayout(self,
                           widget: QWidget):
        self.currentWidget.setVisible(False)
        self.currentWidget = widget
        self.currentWidget.setVisible(True)
        self.currentWidget.setFocus()

    def createKeyboardLayout(self,
                             symbolNames: list,
                             isCaps: bool,
                             registerChangeFunc,
                             langChangeFunc):
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
        for namesRow in symbolNames:
            hBox = QHBoxLayout()
            layout.addLayout(hBox)
            # hBox.setContentsMargins(50, 0, 50, 0)
            # hBox.setSpacing(0)

            if row == 3:
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

        hBox = QHBoxLayout()
        hBox.addWidget(langButton, 1)
        hBox.addWidget(spaceButton, 10)
        hBox.addWidget(cancelButton, 2)
        hBox.addWidget(applyButton, 2)
        layout.addLayout(hBox)

        traverseAllWidgetsInLayoutRec(
            layout,
            lambda w: w.setStyleSheet("""
                    QPushButton 
                    {
                        color: rgb(255, 255, 255);
                        background-color: qlineargradient(
                            x1: 0, y1: 0.2, x2: 1, y2: 1,
                            stop: 0 rgba(%s, %s, %s, 255), 
                            stop: 1 rgba(%s, %s, %s, 255));
                        border-radius: 20px
                        border: 2px solid black
                    }
                    """ % (63, 69, 75, 53, 58, 60)))

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
