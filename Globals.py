from PyQt5 import QtGui, QtWidgets

WINDOW_BACKGROUND = QtGui.QColor(41, 47, 52)
TABLE_COLOR = QtGui.QColor(63, 69, 75)
BORDER_COLOR = QtGui.QColor(85, 170, 127)


def toStr(color: QtGui.QColor):
    return "rgb(%s, %s, %s)" % (color.red(), color.green(), color.blue())