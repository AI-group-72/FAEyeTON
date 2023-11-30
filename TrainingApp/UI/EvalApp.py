import sys
from time import sleep
from PyQt5.QtGui import QColor, QFont
import pandas as pd
import random as rnd
from Input import read_csv_file
from Analise.ParsedData import ParsedData
from PyQt5.QtWidgets import QMainWindow, QPushButton, QApplication, QLabel, QFileDialog, QLineEdit, QCheckBox, \
    QPlainTextEdit, QScrollArea, QScrollBar, QVBoxLayout


class EvalApp(QMainWindow):
    def __init__(self):
        super().__init__()

        self.data_list1 = []
        self.data_list2 = []
        self.data_list_text1 = QPlainTextEdit(self)
        self.data_list_text2 = QPlainTextEdit(self)

        self.edu_list1 = []
        self.edu_list2 = []
        self.edu_list_text1 = QPlainTextEdit(self)
        self.edu_list_text2 = QPlainTextEdit(self)

        self.eval_list = []
        self.eval_list_text = QPlainTextEdit(self)

        self.res_list1 = []
        self.res_list2 = []
        self.res_list_text1 = QPlainTextEdit(self)
        self.res_list_text2 = QPlainTextEdit(self)
        self.arg_line = QLineEdit('1.0', self)

        self.corr = 0
        self.err = 0

        self.keys = ParsedData.get_df_null_row().drop(columns=['File'])
        self.key_boxes = []
        for col in self.keys.head():
            self.keys[col] = 0
        self.ideal_min = ParsedData.get_df_null_row().drop(columns=['File'])
        self.ideal_max = ParsedData.get_df_null_row().drop(columns=['File'])
        self.f1_line = QLineEdit('0.0', self)

        self.setup_ui()

    def setup_ui(self):
        self.setGeometry(300, 300, 1010, 550)
        self.setWindowTitle('Оценка данных')

        data_files_btn = QPushButton('Загрузить данные', self)
        data_files_btn.setGeometry(10, 10, 200, 30)
        data_files_btn.clicked.connect(self.calc_data)

        data_label1 = QLabel('Бодрые', self)
        data_label1.setGeometry(10, 40, 200, 10)
        self.data_list_text1.setStyleSheet("color: blue; background-color: white;")
        self.data_list_text1.setGeometry(10, 50, 200, 50)

        data_label2 = QLabel('Усталые', self)
        data_label2.setGeometry(10, 100, 90, 10)
        self.data_list_text2.setStyleSheet("color: red; background-color: white;")
        self.data_list_text2.setGeometry(10, 110, 200, 50)

        data_save_file_btn = QPushButton('Сохранить', self)
        data_save_file_btn.setGeometry(10, 200, 100, 30)
        data_save_file_btn.clicked.connect(self.save_data)

        data_load_file_btn = QPushButton('Загрузить', self)
        data_load_file_btn.setGeometry(110, 200, 100, 30)
        data_load_file_btn.clicked.connect(self.load_data)

        edu_files_btn = QPushButton('Разбить выборку для обучения', self)
        edu_files_btn.setGeometry(280, 10, 200, 30)
        edu_files_btn.clicked.connect(self.take_sample)

        edu_label1 = QLabel('Бодрые', self)
        edu_label1.setGeometry(280, 40, 200, 10)
        self.edu_list_text1.setStyleSheet("color: blue; background-color: white;")
        self.edu_list_text1.setGeometry(280, 50, 200, 50)
        edu_label2 = QLabel('Усталые', self)
        edu_label2.setGeometry(280, 100, 90, 10)
        self.edu_list_text2.setStyleSheet("color: red; background-color: white;")
        self.edu_list_text2.setGeometry(280, 110, 200, 50)

        edu_btn = QPushButton('Обучение', self)
        edu_btn.setGeometry(280, 170, 200, 30)
        edu_btn.clicked.connect(self.do_edu)

        edu_save_file_btn = QPushButton('Сохранить', self)
        edu_save_file_btn.setGeometry(280, 200, 100, 30)
        edu_save_file_btn.clicked.connect(self.save_edu_file)

        edu_load_file_btn = QPushButton('Загрузить', self)
        edu_load_file_btn.setGeometry(380, 200, 100, 30)
        edu_load_file_btn.clicked.connect(self.load_edu_file)

        crossvalid_btn = QPushButton('Кроссвалидация', self)
        crossvalid_btn.setGeometry(280, 240, 200, 30)
        crossvalid_btn.clicked.connect(self.cross_validation)
        self.crossvalid_label = QLineEdit('none', self)
        self.crossvalid_label.setGeometry(280, 270, 200, 30)

        eval_label = QLabel('На оценку', self)
        eval_label.setGeometry(550, 40, 200, 10)
        self.eval_list_text.setGeometry(550, 50, 200, 150)

        self.arg_line.setGeometry(550, 210, 200, 30)

        scroll_box = QScrollArea(self)
        scroll_box.setGeometry(550, 250, 200, 200)
        
        self.scrollbar = QScrollBar(self)
        self.scrollbar.setGeometry(750, 250, 20, 200)
        self.scrollbar.sliderMoved.connect(self.scroll_check_box)
        
        self.create_check_box(scroll_box)        

        res_files_btn = QPushButton('Выполнить оценку', self)
        res_files_btn.setGeometry(550, 10, 200, 30)
        res_files_btn.clicked.connect(self.do_eval)        

        res_label1 = QLabel('Бодрые', self)
        res_label1.setGeometry(800, 40, 200, 10)
        self.res_list_text1.setStyleSheet("color: blue; background-color: white;")
        self.res_list_text1.setGeometry(800, 50, 200, 50)

        res_label2 = QLabel('Усталые', self)
        res_label2.setGeometry(800, 100, 90, 10)
        self.res_list_text2.setStyleSheet("color: red; background-color: white;")
        self.res_list_text2.setGeometry(800, 110, 200, 50)

        self.f1_line.setGeometry(800, 200, 200, 30)

        self.show()


    def create_check_box(self, parent):
        x = 0
        y = 0
        w = parent.width()
        h = 15
        self.scr_area = QScrollArea(parent)
        for col in ParsedData.get_df_null_row().drop(columns='File').head():
            chbx = QCheckBox(str(col), self.scr_area)
            chbx.setChecked(self.keys[col].iloc[0] == 1)
            chbx.setGeometry(x, y, w, h)
            chbx.clicked.connect(self.check_box_click)
            self.key_boxes.append(chbx)
            y += h 
        self.scr_area.resize(parent.width(), y)
        self.scrollbar.setMaximum(y - parent.height() + 10)

    def scroll_check_box(self):
        value = self.scrollbar.value()
        self.scr_area.move(0, -value)

    def check_box_click(self):
        i = 0
        for col in self.keys.head():
            self.keys[col].iloc[0] = 1 if self.key_boxes[i].isChecked() else 0
            i += 1

    def calc_df(self, files):
        arg = float(self.arg_line.text())
        data_frame = ParsedData.get_df_null_row()
        for line in files:
            section = read_csv_file(line)
            metrics = ParsedData()
            metrics.parse(section, 2, arg)
            metrics.calc_metrics()
            row = metrics.get_df_row(line.split('/')[-1])
            data_frame = pd.concat([data_frame, row], ignore_index=True)
        data_frame = data_frame.drop(index=[0])
        return data_frame

    def calc_data(self):
        print('load edu button click')
        
        self.data_list2 = ParsedData.get_df_null_row()

        csv_path, _ = QFileDialog.getOpenFileNames(caption='Загрузите Бодрых')
        self.data_list1 = self.calc_df(csv_path)
        self.data_list_text1.setPlainText('')
        for line in self.data_list1['File']:
            self.data_list_text1.setPlainText(self.data_list_text1.toPlainText() + line + '\n')

        csv_path, _ = QFileDialog.getOpenFileNames(caption='Загрузите Уставших')
        self.data_list2 = self.calc_df(csv_path)
        self.data_list_text2.setPlainText('')
        for line in self.data_list2['File']:
            self.data_list_text2.setPlainText(self.data_list_text2.toPlainText() + line + '\n')

    def save_data(self):
        self.data_list1.to_csv('Бодрые.csv', sep=';', index=False)
        self.data_list2.to_csv('Усталые.csv', sep=';', index=False)

    def load_data(self):
        self.data_list1 = pd.read_csv('Бодрые.csv', sep=';')
        self.data_list2 = pd.read_csv('Усталые.csv', sep=';')
        self.data_list_text1.setPlainText('')
        for line in self.data_list1['File']:
            self.data_list_text1.setPlainText(self.data_list_text1.toPlainText() + line + '\n')
        self.data_list_text2.setPlainText('')
        for line in self.data_list2['File']:
            self.data_list_text2.setPlainText(self.data_list_text2.toPlainText() + line + '\n')
        print(self.data_list2)


    def take_sample(self):
        print('load edu button click')
        l1 = []
        l2 = []
        self.eval_list = []
        for _, row in self.data_list1.iterrows():
            l1.append(list(row))
            self.eval_list.append(list(row))
        for _, row in self.data_list2.iterrows():
            l2.append(list(row))
            self.eval_list.append(list(row))

        self.edu_list1 = rnd.sample(l1, k=int(0.8*len(l1)))
        self.edu_list2 = rnd.sample(l2, k=int(0.8*len(l2)))
        self.edu_list_text1.setPlainText('')
        for line in self.edu_list1:
            self.edu_list_text1.setPlainText(self.edu_list_text1.toPlainText() + line[0] + '\n')
            self.eval_list.remove(line)
            
        self.edu_list_text2.setPlainText('')
        for line in self.edu_list2:
            self.edu_list_text2.setPlainText(self.edu_list_text2.toPlainText() + line[0] + '\n')
            self.eval_list.remove(line)

        #print(self.eval_list)
        self.eval_list_text.setPlainText('')
        for line in self.eval_list:
            self.eval_list_text.setPlainText(self.eval_list_text.toPlainText() + line[0] + '\n')
        
            

    def do_edu(self):
        print('edu')
        print('---------')
        mean = [0] * len(ParsedData.get_df_null_row().drop(columns=['File']).columns.values)
        for line in self.edu_list1:
            for i in range(1, len(line)):
                mean[i-1] += line[i]        
        for i in range(0, len(mean)):
            mean[i] /= len(self.edu_list1)        
        i = 0
        self.ideal_max = ParsedData.get_df_null_row().drop(columns=['File'])
        for cell in self.ideal_max:
            self.ideal_max[cell] = mean[i]
            i += 1
        
        print('---------')
        mean = [0] * len(ParsedData.get_df_null_row().drop(columns=['File']).columns.values)
        for line in self.edu_list2:
            for i in range(1, len(line)):
                mean[i-1] += line[i]
        for i in range(0, len(mean)):
            mean[i] /= len(self.edu_list2)        
        i = 0
        self.ideal_min = ParsedData.get_df_null_row().drop(columns=['File'])
        for cell in self.ideal_min:
            self.ideal_min[cell] = mean[i]
            i += 1

    def save_edu_file(self):
        self.ideal_min.to_csv('edu_min.csv', sep=';', index=False)
        self.ideal_max.to_csv('edu_max.csv', sep=';', index=False)

    def load_edu_file(self):
        self.ideal_min = pd.read_csv('edu_min.csv', sep=';')
        self.ideal_max = pd.read_csv('edu_max.csv', sep=';')

    def do_eval(self):
        print('eval')
        #self.load_edu_file()
        self.res_list1.clear()
        self.res_list2.clear()
        
        for file in self.eval_list:
            i_min = i_max = 0
            for i in range(1, len(file)):
                key = self.keys.columns.values[i-1]
                if self.keys[key].iloc[0] == 0:
                    continue
                if abs(file[i] - self.ideal_max[key].iloc[0]) < abs(file[i] - self.ideal_min[key].iloc[0]):
                    i_max += 1
                else:
                    i_min += 1
            if i_max > i_min:
                self.res_list1.append(file)
            else:
                self.res_list2.append(file)

        self.corr = 0
        self.err = 0
        for line in self.res_list1:
            if self.data_list_text1.toPlainText().__contains__(line[0]) : # gjghfdbnm
                self.corr += 1
            else:
                self.err += 1
        for line in self.res_list2:
            if self.data_list_text2.toPlainText().__contains__(line[0]): #
                self.corr += 1
            else:
                self.err += 1
        print('Corr: ' + str(self.corr) + '  Err: ' + str(self.err))
        self.f1_line.setText('Corr: ' + str(self.corr) + '  Err: ' + str(self.err))
        self.print_result()

    def cross_validation(self):
        n=150
        corr_sum = 0
        err_sum = 0
        for i in range(n):
            self.take_sample()
            self.do_edu()
            self.do_eval()
            corr_sum += self.corr
            err_sum += self.err
        corr_sum /= n
        err_sum /= n
        self.crossvalid_label.setText('Corr: ' + format(corr_sum,'.2f') + '  Err: ' + format(err_sum, '.2f'))
    


    def print_result(self):
        print('print result')
        self.res_list_text1.setPlainText('')
        for line in self.res_list1:
            self.res_list_text1.setPlainText(self.res_list_text1.toPlainText() + line[0] + '\n')
        self.res_list_text2.setPlainText('')
        for line in self.res_list2:
            self.res_list_text2.setPlainText(self.res_list_text2.toPlainText() + line[0] + '\n')


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = EvalApp()
    sys.exit(app.exec_())
