from PyQt5.QtWidgets import QLayout, QWidget


def traverseAllWidgetsInLayoutRec(layout: QLayout,
                                  widgetFunc):
    for i in range(0, layout.count()):
        item = layout.itemAt(i)
        if item.layout() is not None:
            traverseAllWidgetsInLayoutRec(item.layout(), widgetFunc)
        elif item.widget() is not None:
            widgetFunc(item.widget())
    pass
