import sys

from PyQt5.QtGui import QPainter, QColor

from Input import read_csv_file
from Analise.ParsedData import ParsedData
from PyQt5.QtWidgets import QMainWindow, QPushButton, QApplication, QLabel, QFileDialog, QLineEdit, QRadioButton, \
    QButtonGroup

class Example(QMainWindow):

    def __init__(self):
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

        self.rad_line = QLineEdit(self)
        """
        self.x0_line = QLineEdit(self)
        self.x1_line = QLineEdit(self)
        """
        self.initUI()

    def rb_click(self, rb):
        if rb.text() == 'Speed':
            self.I = 0
            self.method_label.setText('Определение фиксаций\nпо скорости')
            self.arg_line.setText('220')
            self.arg_label.setText('Порог скорости')
        if rb.text() == 'Area':
            self.I = 1
            self.method_label.setText('Определение фиксаций\nпо области')
            self.arg_line.setText('5')
            self.arg_label.setText('Диаметр области фиксации')
        if rb.text() == 'Dist':
            self.I = 2
            self.method_label.setText('Определение фиксаций\nпо абсолютному расстоянию')
            self.arg_line.setText('5')
            self.arg_label.setText('Максимальное расстояние')
        self.method_label.adjustSize()
        self.arg_label.adjustSize()

    def initUI(self):

        self.rb_speed.move(20, 60)
        self.rb_area.move(20, 80)
        self.rb_dist.move(20, 100)

        self.method_label.move(20, 20)


        rad_label = QLabel('Диаметр центральной области', self)
        rad_label.move(200, 20)
        rad_label.adjustSize()
        self.rad_line.setText('5')
        self.rad_line.setGeometry(200, 40, 100, 20)
        self.arg_line.setGeometry(200, 80, 100, 20)
        self.arg_line.setText('220')
        self.arg_label.move(200, 60)
        self.arg_label.adjustSize()

        self.arg_0_line.setGeometry(20, 160, 30, 20)
        self.arg_0_line.setText('1')

        self.arg_1_line.setGeometry(50, 160, 30, 20)
        self.arg_1_line.setText('2.5')

        self.arg_step_line.setGeometry(80, 160, 30, 20)
        self.arg_step_line.setText('0.2')

        load_label = QLabel('Расчёт делается\nсразу по\nвыбору файла', self)
        load_label.move(380, 20)
        load_label.adjustSize()
        load_btn = QPushButton('Выбрать файлы', self)
        load_btn.setGeometry(380, 80, 100, 30)
        load_btn.clicked.connect(self.csvLoadButton)
        file_label = QLabel('Output file', self)
        file_label.move(380, 110)
        self.file_line.setText('masterfile.xlsx')
        self.file_line.setGeometry(380, 140, 100, 20)

        ppi_label = QLabel('Определение PPI', self)
        ppi_label.adjustSize()
        ppi_label.move(220, 140)
        load_btn = QPushButton('Выбрать файлы PPI', self)
        load_btn.setGeometry(220, 160, 120, 30)
        load_btn.clicked.connect(self.ppiLoadButton)

        find_btn = QPushButton('Найти', self)
        find_btn.setGeometry(120, 160, 40, 30)
        find_btn.clicked.connect(self.findSec)
        """
        self.x0_line.setText('0')
        self.x0_line.setGeometry(20, 470, 40, 20)

        self.x1_line.setText('0')
        self.x1_line.setGeometry(440, 470, 40, 20)

        btn_left = QPushButton("<", self)
        btn_left.setGeometry(80, 460, 30, 30)
        btn_left.clicked.connect(self.btn_left_click)

        btn_right = QPushButton(">", self)
        btn_right.setGeometry(390, 460, 30, 30)
        btn_right.clicked.connect(self.btn_right_click)

        draw_btn = QPushButton("Draw", self)
        draw_btn.setGeometry(200, 460, 100, 30)
        draw_btn.clicked.connect(self.draw_graf)
        """
        pupil_btn = QPushButton('Файлы pupillabs', self)
        pupil_btn.setGeometry(480, 80, 100, 30)
        pupil_btn.clicked.connect(self.pupilButton)

        pupil_c_btn = QPushButton('Корреляция pupillabs', self)
        pupil_c_btn.setGeometry(480, 40, 100, 30)
        pupil_c_btn.clicked.connect(self.pupilCoreButton)

        self.statusBar()

        self.setGeometry(300, 300, 600, 200)
        self.setWindowTitle('Metric gathering')
        self.show()

    def paintEvent(self, event):
        """
        qp = QPainter()
        qp.begin(self)
        self.draw_frame(qp)
        qp.end()
        """

    def draw_frame(self, qp):
        qp.setPen(QColor(168, 34, 3))
        qp.drawLine(10, 200, 490, 200)
        qp.drawLine(10, 450, 490, 450)

    def btn_left_click(self):
        self.x0_line.setText((float(self.x0_line.text()) - 10).__str__())
        self.x1_line.setText((float(self.x0_line.text()) - 10).__str__())

    def btn_right_click(self):
        self.x0_line.setText((float(self.x0_line.text()) + 10).__str__())
        self.x1_line.setText((float(self.x0_line.text()) + 10).__str__())

    def draw_graf(self):
        qp = QPainter()
        qp.begin(self)
        self.draw_frame(qp)

        file = QFileDialog.getOpenFileName()
        if not file.__contains__('.csv'):
            return
        section = read_csv_file(file)
        metrics = ParsedData()
        print('file chosen for drawing')
        args = [float(self.speed_line.text()), float(self.area_line.text())
            , float(self.s_dist_line.text())]
        metrics.parse(section, self.I, args[self.I])

        x0 = float(self.x0_line.text())
        x1 = float(self.x1_line.text())
        y0 = 0
        y1 = 2
        qp.setPen(QColor(0, 0, 0))
        for i in range(1, len(section.positionData)-1):
            qp.drawLine()
        qp.end()

    def ppiLoadButton(self):
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

    def pupilButton(self):
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

    def pupilCoreButton(self):
        print('pupil button click')
        csv_path, _ = QFileDialog.getOpenFileName()
        pupil_path, _ = QFileDialog.getOpenFileName()

        print('files chosen')
        if not csv_path.__contains__('.csv'):
            print('cant read file ' + csv_path)
            return
        if not pupil_path.__contains__('.csv'):
            print('cant read file ' + pupil_path)
            return
        print('reading file ' + csv_path + ' with data ' + pupil_path)
        section = read_csv_file(csv_path)
        pupil_metrics = ParsedData()
        pupil_metrics.parse_pupil(section, pupil_path)
        max_comp = 0
        max_i = 0
        p_list = []
        step = 0.1
        for i in range(0, 20):
            metrics = ParsedData()
            metrics.parse(section, 2, 0.1 + i * step, 1)
            comp = metrics.compare(pupil_metrics)
            p_list.append([comp, 0.1 + i * step])
            if max_comp < comp:
                max_comp = comp
                max_i = i
        print(p_list)
        print("Comp: " + max_comp.__str__() + " i " + (0.1 + max_i * step).__str__())


    def csvLoadButton(self):
        print('load button click')
        csv_path, _ = QFileDialog.getOpenFileNames()
        if len(csv_path) == 0:
            return
        print('files chosen')
        arg = float(self.arg_line.text())
        rad = float(self.rad_line.text()) / 2
        for file in csv_path:
            if not file.__contains__('.csv'):
                print('cant read file ' + file)
                continue
            print('reading file ' + file)
            section = read_csv_file(file)
            print('parsing file by ' + self.arg_label.text() + ' = ' + self.arg_line.text())
            metrics = ParsedData()
            metrics.parse(section, self.I, arg, rad)
            metrics.calc_metrics()
            metrics.to_xls(file.split('/')[-1], self.file_line.text())
            metrics.print_some()
    #        metrics.to_csv('../out_data1 — копия.xlsx')

    def findSec(self):
        print('find sec click')
        csv_path, _ = QFileDialog.getOpenFileNames()
        if len(csv_path) == 0:
            return
        print('files chosen')
        arg0 = float(self.arg_0_line.text())
        arg1 = float(self.arg_1_line.text())
        step = float(self.arg_step_line.text())
        rad = float(self.rad_line.text()) / 2
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
                section = read_csv_file(file)
                metrics = ParsedData()
                metrics.parse(section, self.I, arg, rad)
                metrics.calc_metrics()
                metrics.to_xls_by_row(file.split('/')[-1], self.file_line.text())
#                lines.append(metrics.get_line())
                current += 1
                print( (float(current) / float(total)).__str__() + " % of progress")
            '''
                print('calculating differences...')
                diff = [0.0] * len(lines[0])
                for i in range(1, len(lines)):
                    for j in range(0, len(lines[0])):
                        if (lines[-1][j] - lines[0][j] < 0) == (lines[0][j] - lines[i][j] < 0):
                            diff[j] += 1
                fl = False
                for j in range(0, len(lines[0])):
                    diff[j] = diff[j] * 100 / (len(lines) - 1)
                    fl = fl or diff[j] > 85
                if fl:
                    diff_list.append(arg.__str__() + ' : ' + diff.__str__())
            for line in diff_list:
                print(line)
            '''

    def buttonAClicked(self):
        self.statusBar().showMessage('A was pressed' + self.line.text())

    def buttonBClicked(self):
        self.statusBar().showMessage('B was pressed' + self.line.text())


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())
