import sys
from _csv import writer
import csv
import os.path
import datetime
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QMainWindow, QPushButton, QApplication, QLabel, QLineEdit, QSlider


class Example(QMainWindow):

    lines = ['уставший', 'сонный', 'вялый', 'утомленный', 'измученный', 'энергичный',  'активный',
             'бодрый', 'производительный', 'оживленный', 'вымотанный', 'изнуренный',
             'держать глаза открытыми', 'двигать телом', 'концентрироваться', 'поддерживать беседу',
             'желание закрыть глаза', 'желание лечь']

    labels = [['Совсем нет', 'Очень сильно'],
              ['Без усилий', 'Крайне трудно'],
              ['Нет', 'Крайне велико']]

    tresh1 = 12
    tresh2 = 4
    tresh3 = 2

    def __init__(self):
        super().__init__()

        self.file_lbl = QLabel('Укажите имя записи в форматe \n yy-mm-dd-activity-time', self)
        self.file_line = QLineEdit(self)
        self.file_line.setText(datetime.datetime.now().__str__().split(' ')[0][2:])

        self.time_lbl = QLabel('Укажите время записи', self)
        self.time_line = QLineEdit(self)
        self.time_line.setText(datetime.datetime.now().__str__().split(' ')[1].split('.')[0])

        self.name_lbl = QLabel('Укажите имя', self)
        self.name_line = QLineEdit(self)
        self.last_name = ''
        self.read_last_name()
        self.name_line.setText(self.last_name)

        self.i = 0
        self.j = 0

        self.slider_label = QLabel('Показатель', self)
        self.left_label = QLabel('От', self)
        self.right_label = QLabel('До', self)
        self.slider = QSlider(Qt.Orientation.Horizontal, self)
        self.slider.setRange(0, 100)
        self.slider.setPageStep(1)

        self.write_btn = QPushButton('Запись в файл', self)

        self.res = []

        """
        self.x0_line = QLineEdit(self)
        self.x1_line = QLineEdit(self)
        """
        self.initUI()

    def initUI(self):
        self.file_lbl.adjustSize()
        self.file_lbl.move(50, 20)
        self.file_line.setGeometry(50, 60, 150, 20)

        self.time_lbl.adjustSize()
        self.time_lbl.move(350, 20)
        self.time_line.setGeometry(350, 40, 100, 20)

        self.name_lbl.adjustSize()
        self.name_lbl.move(350, 60)
        self.name_line.setGeometry(350, 80, 100, 20)

        self.left_label.adjustSize()
        self.left_label.move(20, 160)
        self.right_label.adjustSize()
        self.right_label.move(400, 160)

        self.slider_label.setFont(QFont('Arial', 16))
        self.slider_label.adjustSize()
        self.slider_label.move(int(250 - self.slider_label.width()/2), 140)

        self.slider.setGeometry(20, 180, 460, 20)
        self.slider.orientation()

        start_btn = QPushButton('Сбросить', self)
        start_btn.setGeometry(20, 200, 100, 30)
        start_btn.clicked.connect(self.start)

        next_btn = QPushButton('Далее', self)
        next_btn.setGeometry(140, 200, 100, 30)
        next_btn.clicked.connect(self.next)

        self.write_btn.setVisible(False)
        self.write_btn.setGeometry(380, 200, 100, 30)
        self.write_btn.clicked.connect(self.write)
        self.write_btn.setVisible(False)

        self.statusBar()

        self.setGeometry(300, 300, 500, 250)
        self.setWindowTitle('VAS-F')
        self.start()
        self.show()

    def adjust_text(self):
        self.slider_label.setText(Example.lines[self.i])
        self.left_label.setText(Example.labels[self.j][0])
        self.right_label.setText(Example.labels[self.j][1])
        self.left_label.adjustSize()
        self.right_label.adjustSize()
        self.slider_label.adjustSize()
        self.slider_label.move(int(250 - self.slider_label.width() / 2), 140)

    def start(self):
        self.i = 0
        self.j = 0
        self.adjust_text()
        self.res = []
        self.write_btn.setVisible(False)
        self.write_btn.setEnabled(True)

# автоматическая запись, числовой ввод

    def next(self):
        if self.i >= 18:
            return
        self.res.append(self.slider.value() * 1.0)
        self.slider.setValue(0)
        self.i += 1
        if self.i == Example.tresh1:
            self.j = 1
        if self.i == Example.tresh2 + Example.tresh1:
            self.j = 2
        if self.i >= Example.tresh3 + Example.tresh2 + Example.tresh1:
            self.j = 3
            self.slider_label.setText('Finish!')
            self.write_btn.setVisible(True)
            return
        self.adjust_text()

    def write(self):
        self.write_btn.setEnabled(False)
        row = [self.file_line.text(), self.name_line.text(), self.time_line.text()]
        for r in self.res:
            row.append(r)
        with open('VAS-F.csv', 'a+', newline='') as write_obj:
            csv_writer = writer(write_obj, delimiter=';')
            csv_writer.writerow(row)

    def read_last_name(self):
        if not os.path.isfile('VAS-F.csv'):
            return
        with open('VAS-F.csv', 'r', encoding="utf-8", errors="ignore") as scraped:
            reader = csv.reader(scraped, delimiter=',')
            for row in reader:
                if row:  # avoid blank lines
                    self.last_name = row.__str__().split(';')[1]

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())
