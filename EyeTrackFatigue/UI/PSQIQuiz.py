import sys
from _csv import writer

from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QMainWindow, QPushButton, QApplication, QLabel, QLineEdit, QRadioButton, QButtonGroup


class Example(QMainWindow):

    questions = ['1.	В какое время Вы легли спать?',
                 '2.	Сколько времени (минут) Вам потребовалось, чтобы заснуть?',
                 '3.    В какое время Вы обычно просыпались\n    в течение последнего месяца?',
                 '4.	Сколько часов в среднем Вы спали за ночь?\n    (количество часов может отличаться от\n'
                 '    количества времени, проведенного в постели).',
                 '5.	Как бы Вы охарактеризовали качество\n    Вашего сна за последнюю ночь?']

    answers = ['ВРЕМЯ ОТХОДА КО СНУ ',
               'КОЛИЧЕСТВО МИНУТ ',
               'ВРЕМЯ ПОДЪЕМА',
               'КОЛИЧЕСТВО ЧАСОВ СНА ЗА НОЧЬ ',
               ['a.	Очень хорошее',
                'b.	Достаточно хорошее',
                'c.	Скорее плохое',
                'd.	Очень плохое']]

    def __init__(self):
        super().__init__()

        self.rb_a = QRadioButton('a.	Очень хорошее', self)
        self.rb_a.adjustSize()
        self.rb_a.setChecked(True)
        self.sleep_quality = 3
        self.rb_b = QRadioButton('b.	Достаточно хорошее', self)
        self.rb_b.adjustSize()
        self.rb_c = QRadioButton('c.	Скорее плохое', self)
        self.rb_c.adjustSize()
        self.rb_d = QRadioButton('d.	Очень плохое', self)
        self.rb_d.adjustSize()

        self.rb_group = QButtonGroup()
        self.rb_group.addButton(self.rb_a)
        self.rb_group.addButton(self.rb_b)
        self.rb_group.addButton(self.rb_c)
        self.rb_group.addButton(self.rb_d)
        self.rb_group.buttonClicked.connect(self.rb_click)

        self.file_lbl = QLabel('Укажите имя записи в форматe \n yy-mm-dd-activity-time', self)
        self.file_line = QLineEdit(self)

        self.time_lbl = QLabel('Укажите время записи', self)
        self.time_line = QLineEdit(self)
        self.time_line.setText('00:00')

        self.name_lbl = QLabel('Укажите имя', self)
        self.name_line = QLineEdit(self)

        self.question_lbl = QLabel('Вопрос', self)
        self.answer_lbl = QLabel('Ответ', self)
        self.answer_line = QLineEdit(self)

        self.write_btn = QPushButton('Запись в файл', self)

        self.i = 0
        self.res = []

        """
        self.x0_line = QLineEdit(self)
        self.x1_line = QLineEdit(self)
        """
        self.initUI()

    def rb_click(self, rb):
        if rb.text()[0] == 'a':
            self.sleep_quality = 3
        if rb.text()[0] == 'b':
            self.sleep_quality = 2
        if rb.text()[0] == 'c':
            self.sleep_quality = 1
        if rb.text()[0] == 'd':
            self.sleep_quality = 0

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

        self.question_lbl.setFont(QFont('Arial', 10))
        self.question_lbl.adjustSize()
        self.question_lbl.move(20, 100)

        self.answer_lbl.setFont(QFont('Arial', 10))

        self.rb_a.move(20, 145)
        self.rb_b.move(20, 165)
        self.rb_c.move(220, 145)
        self.rb_d.move(220, 165)

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
        self.setWindowTitle('PSQI')
        self.start()
        self.show()

    def adjust_text(self):
        self.question_lbl.setText(Example.questions[self.i])
        self.question_lbl.adjustSize()
        self.answer_line.setText('')
        if self.i < 4:
            self.answer_lbl.setText(Example.answers[self.i])
            self.answer_lbl.adjustSize()
            self.answer_lbl.move(20, 150)
            self.answer_line.setGeometry(40 + self.answer_lbl.width(), 150, 440 - self.answer_lbl.width(), 20)
        if self.i == 0 or self.i == 2:
            self.answer_line.setText('0:00')
        if self.i == 1 or self.i == 3:
            self.answer_line.setText('0')

        self.rb_a.setVisible(self.i >= 4)
        self.rb_b.setVisible(self.i >= 4)
        self.rb_c.setVisible(self.i >= 4)
        self.rb_d.setVisible(self.i >= 4)
        self.answer_lbl.setVisible(self.i < 4)
        self.answer_line.setVisible(self.i < 4)

    def start(self):
        self.i = 0
        self.adjust_text()
        self.res = []
        self.write_btn.setVisible(False)

    def next(self):
        if self.i > 5:
            return
        self.i += 1
        if self.i == 5:
            self.res.append(self.sleep_quality)
            self.question_lbl.setText('Finish!')
            self.write_btn.setVisible(True)
            return
        self.res.append(self.answer_line.text())
        self.adjust_text()

    def write(self):
        row = [self.file_line.text(), self.name_line.text(), self.time_line.text()]
        for r in self.res:
            row.append(r)
        with open('PSQI.csv', 'a+', newline='') as write_obj:
            csv_writer = writer(write_obj, delimiter=';')
            csv_writer.writerow(row)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())
