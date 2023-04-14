# Общие объекты и методы
from PyQt5.QtCore import QEvent
from PyQt5.QtGui import QIcon, QFont, QIntValidator
from PyQt5.QtWidgets import QMessageBox

# Событие "новое ребро"
class NewEdge(QEvent):
    Type = QEvent.Type(QEvent.registerEventType())

    def __init__(self, start, end, weight=None):
        QEvent.__init__(self, NewEdge.Type)
        self.start = start
        self.end = end
        self.weight = weight
# Событие "новая вершина"
class NewVertex(QEvent):
    Type = QEvent.Type(QEvent.registerEventType())

    def __init__(self, vertex):
        QEvent.__init__(self, NewVertex.Type)
        self.vertex = vertex

# Сообщение об ошибке
def input_error(text):
    msg = QMessageBox()
    msg.setIcon(QMessageBox.Warning)
    msg.setText('Неверно введены данные')
    msg.setInformativeText(text)
    msg.setWindowTitle('Ошибка')
    msg.setWindowIcon(QIcon('warning.png'))
    msg.exec()


# Информационное окно
def info(text):
    msg = QMessageBox()
    msg.setIcon(QMessageBox.Information)
    msg.setText('Сведения о работе программы:')
    msg.setInformativeText(text)
    msg.setWindowTitle('Сведения')
    msg.setWindowIcon(QIcon('info.png'))
    msg.exec()

# Основной шрифт, валидаторы проверяющие тип ввода
f = QFont("Times", 10)
title_f = QFont("Times", 10, QFont.Bold, QFont.StyleItalic)
only_int = QIntValidator()

# Цвета для точек на графике
colors = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd', '#8c564b', '#e377c2', '#7f7f7f', '#bcbd22', '#17becf']

# Текст с инструкциями
default_text = '1. Click on input graph field to add vertex.\n' \
               '2. Click at vertex and draw to the other to add edge.\n' \
               '3. You can change weights in table above.\n' \
               '4. When you finished construction of graph, click start to solve.\n' \
               '5. Here you will see the results.\n' \
               '6. Reset to repeat.'