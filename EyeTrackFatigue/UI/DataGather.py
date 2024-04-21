from time import sleep
import sys
from PyQt6.QtGui import QPainter, QColor
from ..Input import read_csv_file
from ..Analise.ParsedData import ParsedData
from PyQt6.QtWidgets import QMainWindow, QPushButton, QApplication, QLabel, QFileDialog, QLineEdit, QRadioButton, \
    QButtonGroup

class Example(QMainWindow):

    def __init__(self):  # инициализация визуальных компонентов
        super().__init__()

        self.rb_speed = QRadioButton('Speed', self)
        self.rb_speed.setChecked(True)
        self.I = 0
        self.rb_area = QRadioButton('Area', self)
        self.rb_dist = QRadioButton('Dist', self)

        self.rb_group = QButtonGroup()
        self.rb_group.addButton(self.rb_speed)
        self.rb_group.addButton(self.rb_area)
        self.rb_group.addButton(self.rb_dist)
        self.rb_group.buttonClicked.connect(self.rb_click)

        self.method_label = QLabel('Определение фиксаций\nпо скорости', self)
        self.method_label.adjustSize()
        self.file_line = QLineEdit(self)
        self.arg_label = QLabel("Порог скорости", self)
        self.arg_line = QLineEdit(self)

        self.arg_0_line = QLineEdit(self)
        self.arg_1_line = QLineEdit(self)
        self.arg_step_line = QLineEdit(self)
        self.initUI()

    def rb_click(self, rb): # обработка выбора метода размеметки
        if rb.text() == 'Speed':
            self.I = 0
            self.method_label.setText('Определение фиксаций\nпо скорости')
            self.arg_line.setText('220') # установка значений аргумента по умолчанию
            self.arg_label.setText('Порог скорости')
        if rb.text() == 'Area':
            self.I = 1
            self.method_label.setText('Определение фиксаций\nпо области')
            self.arg_line.setText('5') # установка значений аргумента по умолчанию
            self.arg_label.setText('Диаметр области фиксации')
        if rb.text() == 'Dist':
            self.I = 2
            self.method_label.setText('Определение фиксаций\nпо абсолютному расстоянию')
            self.arg_line.setText('5') # установка значений аргумента по умолчанию
            self.arg_label.setText('Максимальное расстояние')
        self.method_label.adjustSize()
        self.arg_label.adjustSize()

    def initUI(self): # инициализация интерфейса с конкретными значениями
        self.rb_speed.move(20, 60)
        self.rb_area.move(20, 80)
        self.rb_dist.move(20, 100)
        self.method_label.move(20, 20)
        # устаревшая часть - UI для указания центральной области
        # rad_label = QLabel('Диаметр центральной области', self)
        # rad_label.move(200, 20)
        # rad_label.adjustSize()
        # self.rad_line.setText('5')
        # self.rad_line.setGeometry(200, 40, 100, 20)

        # ввод аргумента (для метода разметки)
        self.arg_line.setGeometry(200, 80, 100, 20)
        self.arg_line.setText('220')
        self.arg_label.move(200, 60)
        self.arg_label.adjustSize()

        # ввод аргументов с перебором (для метода разметки)
        self.arg_0_line.setGeometry(20, 160, 30, 20)
        self.arg_0_line.setText('1')
        self.arg_1_line.setGeometry(50, 160, 30, 20)
        self.arg_1_line.setText('2.5')
        self.arg_step_line.setGeometry(80, 160, 30, 20)
        self.arg_step_line.setText('0.2')
        # зона загрузки файлов, запуска рассчётов
        load_label = QLabel('Расчёт делается\nсразу по\nвыбору файла', self)
        load_label.move(380, 20)
        load_label.adjustSize()
        load_btn = QPushButton('Выбрать файлы', self)
        load_btn.setGeometry(380, 80, 100, 30)
        load_btn.clicked.connect(self.csvLoadButton)
        file_label = QLabel('Output file', self)
        file_label.move(380, 110)
        self.file_line.setText('masterfile.csv')
        self.file_line.setGeometry(380, 140, 100, 20)

        
        ppi_label = QLabel('Определение PPI', self)
        ppi_label.adjustSize()
        ppi_label.move(220, 140)
        load_btn = QPushButton('Выбрать файлы PPI', self)
        load_btn.setGeometry(220, 160, 120, 30)
        load_btn.clicked.connect(self.ppiLoadButton)

        find_btn = QPushButton('Счёт в \n интервале', self)
        find_btn.setGeometry(120, 145, 65, 40)
        find_btn.clicked.connect(self.findSec)

        pupil_btn = QPushButton('Файлы pupillabs', self)
        pupil_btn.setGeometry(480, 80, 100, 30)
        pupil_btn.clicked.connect(self.pupilButton)

        self.statusBar()
        self.setGeometry(300, 300, 600, 200)
        self.setWindowTitle('Вычисление количественных характеристик')
        self.show()

    def ppiLoadButton(self): # загрузка данных о преимпульсном ингибировании 
        print('ppi button click')
        ppi_path, _ = QFileDialog.getOpenFileNames()
        if len(ppi_path) == 0:
            return
        print('files chosen')
        for file in ppi_path:
            if not file.__contains__('.txt'):
                print('cant read file ' + file)
                continue
            print('reading file ' + file)
            lines = open(file).readlines()
            ParsedData.ppi_to_xls(file, lines, self.file_line.text())

    def pupilButton(self): # загрузка файлов, полученных от PupilLabs (сервис поставщика окулографа)
        print('pupil button click')
        csv_path, _ = QFileDialog.getOpenFileNames()
        pupil_path, _ = QFileDialog.getOpenFileNames()

        if len(csv_path) == 0:
            return
        print('files chosen')
        if len(pupil_path) != len(csv_path):
            print('number of file are not matching')
            return
        for i in range(0, len(csv_path)):
            if not csv_path[i].__contains__('.csv'):
                print('cant read file ' + csv_path[i])
                continue
            if not pupil_path[i].__contains__('.csv'):
                print('cant read file ' + pupil_path[i])
                continue
            print('reading file ' + csv_path[i] + ' with data ' + pupil_path[i])
            section = read_csv_file(csv_path[i])
            metrics = ParsedData()
            metrics.parse_pupil(section, pupil_path[i])
            metrics.calc_metrics()
            metrics.to_xls(csv_path[i].split('/')[-1], self.file_line.text())

    def csvLoadButton(self): # загрузка файлов на обработку
        print('load button click')
        csv_path, _ = QFileDialog.getOpenFileNames() # выбор файлов
        if len(csv_path) == 0:
            return
        print('files chosen')
        arg = float(self.arg_line.text())
        # rad = float(self.rad_line.text()) / 2
        for file in csv_path: # перебор выбранных файлов
            if not file.__contains__('.csv'):
                print('cant read file ' + file)
                continue
            print('reading file ' + file)
            section = read_csv_file(file) # считывание сырых данных
            print('parsing file by ' + self.arg_label.text() + ' = ' + self.arg_line.text())
            metrics = ParsedData() 
            metrics.parse(section, self.I, arg) # разметка данных выбранным методом
            metrics.calc_metrics() # рассчёт метрик
            metrics.to_csv(file.split('/')[-1], self.file_line.text()) # вывод результата

    def findSec(self): # загрузка файлов на обработку с перебором аргумекта
        print('find sec click')
        csv_path, _ = QFileDialog.getOpenFileNames() # выбор файлов
        if len(csv_path) == 0:
            return
        print('files chosen')
        arg0 = float(self.arg_0_line.text()) # выделение указанных границ и шага аргумента
        arg1 = float(self.arg_1_line.text())
        step = float(self.arg_step_line.text())
        # rad = float(self.rad_line.text()) / 2
#        diff_list = []

        total = len(csv_path) * ((arg1 - arg0)/step).__int__()
        current = 0
        for ii in range(0, ((arg1 - arg0)/step).__int__()):
            arg = arg0 + ii * step
#            lines = []
            for file in csv_path:
                if not file.__contains__('.csv'):
                    print('cant read file ' + file)
                    continue
                print('reading file ' + file)
                section = read_csv_file(file) # считывание сырых данных
                metrics = ParsedData() 
                metrics.parse(section, self.I, arg) # разметка данных выбранным методом
                metrics.calc_metrics() # рассчёт метрик
                metrics.to_csv(file.split('/')[-1], 'Summary.csv') # вывод
                current += 1
                print( (float(current) / float(total) * 100.0).__str__() + " % of progress")

# инициализация приложения через мейн процесс
if __name__ == '__main__':
    app = QApplication(sys.argv)
    sleep(1)
    ex = Example()
    sys.exit(app.exec_())
