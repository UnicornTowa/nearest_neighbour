# Основное окно
import sys

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon, QPainter, QColor
from PyQt5.QtWidgets import QApplication, QLabel, QPushButton, QMainWindow, QComboBox, \
    QTableWidget, QTableWidgetItem, QHeaderView, QTextEdit

import nna
import nna_common
import nna_viz


# Основной класс
class MainWindow(QMainWindow):
    # Конструктор класса
    def __init__(self):
        super().__init__()
        self.setWindowIcon(QIcon('nodes.png'))  # Иконка

        # Текстовые поля
        self.input_title = QLabel('Input Graph', self)
        self.input_title.setFont(nna_common.title_f)
        self.input_title.move(10, 10)
        self.input_title.setFixedWidth(300)

        self.input_title = QLabel('Parameters & Control', self)
        self.input_title.setFont(nna_common.title_f)
        self.input_title.move(10, 560)
        self.input_title.setFixedWidth(300)

        self.output_title = QLabel('Output Graph', self)
        self.output_title.setFont(nna_common.title_f)
        self.output_title.move(10, 640)
        self.output_title.setFixedWidth(300)

        self.results_title = QLabel('Edge Table', self)
        self.results_title.setFont(nna_common.title_f)
        self.results_title.move(980, 10)
        self.results_title.setFixedWidth(300)

        self.results_title = QLabel('Instructions & Results', self)
        self.results_title.setFont(nna_common.title_f)
        self.results_title.move(980, 760)
        self.results_title.setFixedWidth(300)

        # Поле выбора стартовой вершины
        self.start_v_combo = QComboBox(self)
        self.start_v_combo.move(15, 600)
        self.start_v_combo.addItem('Start vertex')
        self.start_v_combo.setFont(nna_common.f)
        self.start_v_combo.setFixedWidth(150)
        self.start_v_combo.currentTextChanged.connect(self.set_start_v)
        self.start_v = None

        # Кнопки
        self.start_button = QPushButton('Start', self)
        self.start_button.setFont(nna_common.f)
        self.start_button.move(165, 600)
        self.start_button.setFixedWidth(195)
        self.start_button.clicked.connect(self.start)

        self.reset_button = QPushButton('Reset Graph', self)
        self.reset_button.setFont(nna_common.f)
        self.reset_button.move(360, 600)
        self.reset_button.setFixedWidth(200)
        self.reset_button.clicked.connect(self.reset)

        self.complete_button = QPushButton('Complete', self)
        self.complete_button.setFont(nna_common.f)
        self.complete_button.move(560, 600)
        self.complete_button.setFixedWidth(200)
        self.complete_button.clicked.connect(self.complete_graph)

        self.opt_button = QPushButton('Optimize', self)
        self.opt_button.setFont(nna_common.f)
        self.opt_button.move(760, 600)
        self.opt_button.setFixedWidth(195)
        self.opt_button.clicked.connect(self.run_opt)


        # Установка размеров окна и заголовка
        scaler = 400
        self.setFixedSize(4*scaler, 3*scaler)
        self.setWindowTitle('Nearest Neighbour Algorithm')

        # Привязываем редактируемый входной граф
        self.g_input = nna_viz.GraphWidgetEditable(self)
        self.g_input.move(10, 50)
        self.g_input.setFixedSize(950, 500)
        self.layout().addWidget(self.g_input)

        self.g_input.installEventFilter(self)

        # Привязываем нередактируемый выходной граф
        self.g_output = nna_viz.GraphWidget(self)
        self.g_output.move(10, 680)
        self.g_output.setFixedSize(950, 500)
        self.layout().addWidget(self.g_output)
        self.path_len = 0

        # Таблица вывода
        self.table = QTableWidget(self)
        self.table_size = 0
        self.table.setColumnCount(3)
        self.table.setFixedSize(600, 700)
        self.table.move(980, 50)
        self.table.setHorizontalHeaderItem(0, QTableWidgetItem('Vertex 1'))
        self.table.setHorizontalHeaderItem(1, QTableWidgetItem('Vertex 2'))
        self.table.setHorizontalHeaderItem(2, QTableWidgetItem('Path length'))
        self.table.setColumnWidth(0, 200)
        self.table.setColumnWidth(1, 200)
        self.table.setColumnWidth(2, 200)
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Fixed)
        self.table.setRowCount(0)
        self.table.itemChanged.connect(self.table_edited)

        # Текстовое поле для вывода инструкций и результата
        self.results_field = QTextEdit(self)
        self.results_field.move(980, 800)
        self.results_field.setFixedSize(600, 380)
        self.results_field.setFont(nna_common.f)
        self.results_field.setText(nna_common.default_text)
        self.results_field.setReadOnly(True)

    # Достройка графа до полного
    def complete_graph(self):
        self.g_input.complete()

    # Демонстрация выходного графа
    def update_res(self):
        self.g_output.pos = {n: self.g_input.pos[n] for n in self.g_output.G.nodes}
        self.g_output.vertex_count = len(self.g_output.G.nodes)
        self.g_output.update_graph()
        self.results_field.setText(
            f'Solution: {nna_common.get_path(self.g_output.G, int(self.start_v))}\n'
            f'Path length: {round(self.path_len, 2)}')

    # Изменение веса ребра при редактировании таблицы
    def table_edited(self, item):
        if item is not None:
            row = item.row()
            start_v = int(self.table.item(row, 0).text())
            end_v = int(self.table.item(row, 1).text())
            # Отлов исключений
            try:
                new_weight = float(item.text())
                if new_weight <= 0:
                    raise ValueError('Вес <= 0')
            except:
                nna_common.input_error('Некорректный вес ребра')
                self.table.blockSignals(True)
                self.table.setItem(row, 2, QTableWidgetItem(str(round(self.g_input.G[start_v][end_v]['weight'], 2))))
                self.table.item(row, 2).setTextAlignment(Qt.AlignCenter)
                self.table.blockSignals(False)
                return
            self.g_input.G.edges[start_v, end_v]['weight'] = new_weight

    # Функция делает редактируемой только последний элемент ряда таблицы
    def set_table_row_edit_flags(self, row):
        self.table.item(row, 0).setFlags(self.table.item(row, 0).flags() & ~Qt.ItemIsEditable)
        self.table.item(row, 1).setFlags(self.table.item(row, 1).flags() & ~Qt.ItemIsEditable)
        self.table.item(row, 2).setFlags(self.table.item(row, 2).flags() | Qt.ItemIsEditable)

    # Установка начальной вершины
    def set_start_v(self, val):
        self.start_v = val

    # Сброс графа и результатов
    def reset(self):
        self.g_input.clear_graph()
        self.table.clearContents()
        self.table.setRowCount(0)
        self.table_size = 0
        self.start_v_combo.clear()
        self.g_output.clear_graph()
        self.results_field.setText(nna_common.default_text)
        self.start_v_combo.addItem('Select start vertex')

    # Отлов событий
    def eventFilter(self, obj, event):
        # Добавление ряда таблицы при построении нового ребра
        if obj == self.g_input and event.type() == nna_common.NewEdge.Type:
            self.table.blockSignals(True)
            self.table.insertRow(self.table_size)
            self.table.setItem(self.table_size, 0, QTableWidgetItem(str(event.start)))
            self.table.setItem(self.table_size, 1, QTableWidgetItem(str(event.end)))
            self.table.setItem(self.table_size, 2, QTableWidgetItem(str(round(event.weight, 2))))
            self.set_table_row_edit_flags(self.table_size)
            for i in range(3):
                self.table.item(self.table_size, i).setTextAlignment(Qt.AlignCenter)
            self.table_size += 1
            self.table.blockSignals(False)
            return True
        # Добавление вершины в поле выбора стартовой при ее построении
        elif obj == self.g_input and event.type() == nna_common.NewVertex.Type:
            self.start_v_combo.addItem(str(event.vertex))
            return True
        return super().eventFilter(obj, event)
    # Запуск оптимизаций
    def run_opt(self):
        # Проверка есть ли решение
        if self.path_len == 0:
            nna_common.info('Нечего оптимизировать')
        else:
            # Применяем первую оптимизацию
            improve = nna.two_opt(self.g_input.G, self.g_output.G)
            if improve:
                # Если есть улучшения - изменяем картинку
                self.path_len -= improve
                self.g_output.clear_fig()
                self.update_res()
                print('improved 2-opt')
            else:
                # Пытаемся применить вторую оптимизацию
                improve = nna.vertex_opt(self.g_input.G, self.g_output.G)
                if improve:
                    # Если есть улучшения - изменяем картинку
                    self.path_len -= improve
                    self.g_output.clear_fig()
                    self.update_res()
                    print('improved v-opt')
                else:
                    # Сообщаем пользователю если оптимизация не удалась
                    nna_common.info('Оптимизация не удалась')



    # Запуск алгоритма
    def start(self):
        # Проверка на наличие графа
        if len(self.g_input.G.nodes) == 0:
            nna_common.input_error('Граф пуст')
            return
        # Проверка на выбор стартовой вершины
        if not str(self.start_v).isnumeric():
            nna_common.input_error('Выберите начальную вершину!')
            return
        # Очистка выходного графа
        self.g_output.clear_graph()
        # Запуск и установка результатов
        start_v = int(self.start_v)
        graph, self.path_len = nna.nna(self.g_input.G, start_v)
        self.g_output.G = graph
        self.update_res()

    # Разметка окна
    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setPen(QColor(0, 0, 0))
        painter.drawRect(10, 560, 950, 110)
        painter.drawRect(10, 50, 950, 500)
        painter.drawRect(10, 680, 950, 500)
        painter.drawRect(980, 50, 600, 700)
        painter.drawRect(980, 800, 600, 380)



# Запуск приложения
if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
