import sys
from time import sleep
import pandas as pd
import pickle
from Analise.Names import eng_to_rus
from Evaluate import *
from Input import read_csv_file
from Analise.ParsedData import ParsedData
from Evaluate.RandomForestEval import RandomForestEval
from Evaluate.DecisionTreeEval import DecisionTreeEval
from Evaluate.MLPEval import MLPEval
from PyQt6.QtGui import QPixmap
from PyQt6.QtWidgets import *
from sklearn.metrics import (
    confusion_matrix,
    accuracy_score,
    precision_score,
    recall_score,
    f1_score
)

class EvalApp(QMainWindow):
    def __init__(self):
        super().__init__()

        self.rb_base = QRadioButton('Базовый', self)
        self.rb_rfc = QRadioButton('Random Forest', self)
        self.rb_dtc = QRadioButton('Decision Tree', self)
        self.rb_mlp = QRadioButton('MLP', self)

        self.rb_group = QButtonGroup()
        self.rb_group.addButton(self.rb_base)
        self.rb_group.addButton(self.rb_rfc)
        self.rb_group.addButton(self.rb_dtc)
        self.rb_group.addButton(self.rb_mlp)
        self.rb_mlp.setChecked(True)
        self.model_name = 'MLP'
        self.rb_group.buttonClicked.connect(self.rb_click)

        self.data_list1 = []
        self.data_list2 = []
        self.data_list_text1 = QPlainTextEdit(self)
        self.data_list_text2 = QPlainTextEdit(self)
        self.model = None
        self.edu_list1 = None
        self.edu_list2 = None
        self.edu_list_text1 = QPlainTextEdit(self)
        self.edu_list_text2 = QPlainTextEdit(self)

        self.eval_list = None
        self.eval_list_text = QPlainTextEdit(self)

        self.res_list1 = ParsedData.get_df_null_row()
        self.res_list2 = ParsedData.get_df_null_row()
        self.res_list_text1 = QPlainTextEdit(self)
        self.res_list_text2 = QPlainTextEdit(self)
        self.arg_line = QLineEdit('1.0', self)
        self.file_size_line = QLineEdit('нет', self)

        self.corr = 0
        self.err = 0

        self.keys = ParsedData.get_df_null_row().drop(columns=['File'])
        self.keys.loc[0] = [0] * len(self.keys.columns)
        self.key_boxes = []
        
        self.ideal_min = ParsedData.get_df_null_row().drop(columns=['File'])
        self.ideal_max = ParsedData.get_df_null_row().drop(columns=['File'])
        self.f1_line = QLineEdit('0.0', self)

        self.data_group = []
        self.edu_group = []
        self.eval_group = []
        self.res_group = []
        self.status_ = 0
        self.status_img = QLabel(self)
        self.status_text = QLabel(self)
        self.reset_status_btn = QPushButton('Сбросить', self)
        self.reset_status_btn.clicked.connect(lambda : self.set_status(0))

        self.setup_ui()

    def setup_ui(self):
        self.setGeometry(300, 300, 1010, 650)
        self.setWindowTitle('Оценка данных')

        data_label1 = QLabel('Бодрые', self)
        data_label1.setGeometry(80, 10, 200, 15)
        self.data_group.append(data_label1)

        data_files_btn = QPushButton('Загрузить данные бодрых', self)
        data_files_btn.setGeometry(10, 25, 200, 30)
        data_files_btn.clicked.connect(self.calc_data1)
        self.data_group.append(data_files_btn)

        self.data_list_text1.setStyleSheet("color: blue; background-color: white;")
        self.data_list_text1.setGeometry(10, 60, 200, 150)
        self.data_group.append(self.data_list_text1)

        data_label2 = QLabel('Усталые', self)
        data_label2.setGeometry(80, 210, 90, 15)
        self.data_group.append(data_label2)

        data_files_btn = QPushButton('Загрузить данные усталых', self)
        data_files_btn.setGeometry(10, 225, 200, 30)
        data_files_btn.clicked.connect(self.calc_data2)
        self.data_group.append(data_files_btn)

        self.data_list_text2.setStyleSheet("color: red; background-color: white;")
        self.data_list_text2.setGeometry(10, 260, 200, 150)
        self.data_group.append(self.data_list_text2)

        data_save_file_btn = QPushButton('Сохранить\nпосчитанные\nданные', self)
        data_save_file_btn.setGeometry(10, 420, 100, 60)
        data_save_file_btn.clicked.connect(self.save_data)
        self.data_group.append(data_save_file_btn)

        data_load_file_btn = QPushButton('Загрузить\nпосчитанные\nданные', self)
        data_load_file_btn.setGeometry(110, 420, 100, 60)
        data_load_file_btn.clicked.connect(self.load_data)
        self.data_group.append(data_load_file_btn)

        arg_label = QLabel('Размер области фиксации:', self)
        arg_label.setGeometry(10, 480, 150, 30)
        self.data_group.append(arg_label)
        self.arg_line.setGeometry(160, 480, 50, 30)
        self.data_group.append(self.arg_line)

        file_size_label = QLabel('Максимальный размер файла:', self)
        file_size_label.setGeometry(10, 520, 150, 30)
        self.data_group.append(file_size_label)
        self.file_size_line.setGeometry(160, 520, 50, 30)
        self.data_group.append(self.file_size_line)

    ##################################################################################################################

        edu_files_btn = QPushButton('Разбить выборку для обучения', self)
        edu_files_btn.setGeometry(280, 10, 200, 30)
        edu_files_btn.clicked.connect(self.take_sample)
        self.edu_group.append(edu_files_btn)

        edu_label1 = QLabel('Бодрые', self)
        edu_label1.setGeometry(360, 40, 200, 15)
        self.edu_group.append(edu_label1)
        self.edu_list_text1.setStyleSheet("color: blue; background-color: white;")
        self.edu_list_text1.setGeometry(280, 60, 200, 150)
        self.edu_group.append(self.edu_list_text1)
        edu_label2 = QLabel('Усталые', self)
        edu_label2.setGeometry(360, 200, 90, 50)
        self.edu_group.append(edu_label2)
        self.edu_list_text2.setStyleSheet("color: red; background-color: white;")
        self.edu_list_text2.setGeometry(280, 240, 200, 150)
        self.edu_group.append(self.edu_list_text2)
        
        edu_btn = QPushButton('Обучение', self)
        edu_btn.setGeometry(280, 400, 200, 30)
        edu_btn.clicked.connect(self.do_edu)
        self.edu_group.append(edu_btn)

        edu_save_file_btn = QPushButton('Сохранить\n модель', self)
        edu_save_file_btn.setGeometry(280, 430, 100, 60)
        edu_save_file_btn.clicked.connect(self.save_edu_file)
        self.edu_group.append(edu_save_file_btn)
        edu_load_file_btn = QPushButton('Загрузить\n модель', self)
        edu_load_file_btn.setGeometry(380, 430, 100, 60)
        edu_load_file_btn.clicked.connect(self.load_edu_file)
        self.edu_group.append(edu_load_file_btn)

        self.crossvalid_box = QCheckBox('Кроссвалидация', self)
        self.crossvalid_box.setGeometry(280, 500, 200, 30)
        self.edu_group.append(self.crossvalid_box)
        self.normalize_box = QCheckBox('Нормализация', self)
        self.normalize_box.setGeometry(280, 540, 200, 30)
        self.edu_group.append(self.normalize_box)
        #crossvalid_box.clicked.connect(self.model_cross_validation)
        

    ##################################################################################################################

        eval_label = QLabel('На оценку', self)
        eval_label.setGeometry(550, 40, 200, 10)
        self.eval_list_text.setGeometry(550, 50, 200, 150)
        self.eval_group.append(eval_label)

        self.rb_base.move(550, 210)
        self.rb_rfc.move(550, 240)
        self.rb_dtc.move(550, 270)
        self.rb_mlp.move(550, 300)

        choose_all_btn = QPushButton('Всё', self)
        choose_all_btn.setGeometry(550, 370, 50, 30)
        choose_all_btn.clicked.connect(self.check_box_all)
        self.eval_group.append(choose_all_btn)

        choose_std_btn = QPushButton('Стандартный набор', self)
        choose_std_btn.setGeometry(610, 370, 200, 30)
        choose_std_btn.clicked.connect(self.check_box_std)
        self.eval_group.append(choose_std_btn)

        # Заглушка
        choose_find = QLineEdit('..', self)
        choose_find.setGeometry(820, 370, 180, 30)
        self.eval_group.append(choose_find)

        scroll_box = QScrollArea(self)
        scroll_box.setGeometry(550, 410, 430, 190)
        self.eval_group.append(scroll_box)

        self.scrollbar = QScrollBar(self)
        self.scrollbar.setGeometry(980, 410, 20, 190)
        self.scrollbar.sliderMoved.connect(self.scroll_check_box)
        self.eval_group.append(self.scrollbar)

        self.create_check_box(scroll_box)        

        res_files_btn = QPushButton('Выполнить оценку', self)
        res_files_btn.setGeometry(550, 10, 200, 30)
        res_files_btn.clicked.connect(self.do_eval)        
        self.eval_group.append(res_files_btn)

        res_label = QLabel('Результаты оценки', self)
        res_label.setGeometry(840, 10, 200, 15)
        self.eval_group.append(res_label)
        res_label1 = QLabel('Бодрые', self)
        res_label1.setGeometry(880, 30, 200, 10)
        self.eval_group.append(res_label1)
        self.res_list_text1.setStyleSheet("color: blue; background-color: white;")
        self.res_list_text1.setGeometry(800, 50, 200, 60)
        self.eval_group.append(self.res_list_text1)

        res_label2 = QLabel('Усталые', self)
        res_label2.setGeometry(880, 115, 90, 15)
        self.eval_group.append(res_label2)
        self.res_list_text2.setStyleSheet("color: red; background-color: white;")
        self.res_list_text2.setGeometry(800, 130, 200, 60)
        self.eval_group.append(self.res_list_text2)

        f1_label = QLabel('Точность оценки:',self)
        f1_label.setGeometry(800, 200, 100, 30)
        self.eval_group.append(f1_label)
        self.f1_line.setGeometry(900, 200, 100, 30)
        self.eval_group.append(self.f1_line)
        f1_label = QLabel('Кроссвалидация:',self)
        f1_label.setGeometry(800, 240, 100, 30)
        self.crossvalid_label = QLineEdit('', self)
        self.crossvalid_label.setGeometry(900, 240, 100, 30)
        self.eval_group.append(self.crossvalid_label)

        self.set_status(0)
        self.check_box_std()
        self.show()

    def rb_click(self, rb):
        if rb.text() == 'Базовый':
            self.model_name = 'Base'
        elif rb.text() == 'Random Forest':
            self.model_name = 'RFC'
        elif rb.text() == 'Decision Tree':
            self.model_name = 'DTC'
        elif rb.text() == 'MLP':
            self.model_name = 'MLP'

    def create_check_box(self, parent):
        x = 0
        y = 0
        w = parent.width()
        h = 15
        self.scr_area = QScrollArea(parent)
        for col in ParsedData.get_df_null_row().drop(columns='File').head():
            chbx = QCheckBox(eng_to_rus(str(col)), self.scr_area)
            chbx.setChecked(self.keys[col].iloc(0) == 1)
            chbx.setGeometry(x, y, w, h)
            chbx.clicked.connect(self.check_box_click)
            self.key_boxes.append(chbx)
            y += h 
        self.scr_area.resize(parent.width(), y)
        self.scrollbar.setMaximum(y - parent.height() + 15)
        self.scrollbar.setMinimum(-8)
    
    def scroll_check_box(self):
        value = self.scrollbar.value()
        self.scr_area.move(0, -value)

    def check_box_click(self):
        i = 0
        for col in self.keys.head():
            self.keys[col][0] = 1 if self.key_boxes[i].isChecked() else 0
            i += 1
    
    def check_box_all(self):
        i = 0
        fl = not self.key_boxes[i].isChecked()
        for col in self.keys.head():
            self.keys[col][0] = 1 if fl else 0
            self.key_boxes[i].setChecked(fl)
            i += 1
    
    def check_box_std(self):
        std = {'x_mean', 'x_std', 'x_min', 'x_max', 'x_25', 'x_50', 'x_75', 'y_mean', 'y_std', 'y_min', 'y_max', 'y_25', 'y_50', 'y_75', 'Saccades with amplitude < 6 degrees, per minute', 'Max Curve', 'Fixation time > 150 ms', 'Fixation time > 180 ms', '% of Fixations < 150 ms', '% of Fixations > 150 ms', '% of Fixations > 900 ms', '% of Fixations < 180 ms', '% of Fixations > 180 ms', 'Fixation time < 150 ms, per time', 'Fixation time > 150 ms, per time', '% of Fixations > 150 ms, per minute', '% of Fixations < 180 ms, per minute', 'Min Speed', 'Max Speed', 'Average Speed in interval (1s)', 'Max Speed in interval (1s)', 'Average Fixation Speed', 'Max Fixation Speed', 'Average Saccade Length', 'Min Saccade Length', 'Max Saccade Length'}
        #std = {'x_mean', 'x_std', 'x_min', 'x_max', 'x_25', 'x_50', 'x_75', 'y_mean', 'y_std', 'y_min', 'y_max', 'y_25', 'y_50', 'y_75'}
        #std = {'x_mean', 'y_mean', 'Average Curve', 'Min Curve', 'Min Saccade Time', 'Average Fixation Speed', "% of Fixations < 150 ms, per minute", 'Average Fixation Speed, < 150ms'}
        i = 0
        for col in self.keys.head():
            self.keys[col][0] = 1 if col in std else 0
            self.key_boxes[i].setChecked(col in std)
            i += 1

    def calc_df(self, files):
        arg = float(self.arg_line.text())
        data_frame = ParsedData.get_df_null_row()
        file_size = -1  if self.file_size_line.text() == 'нет' else float(self.file_size_line.text())
        for line in files:
            p = 1
            print(file_size)
            for section in read_csv_file(line).split(file_size):
                # print(section.time_frame())
                # print(section)
                metrics = ParsedData()
                metrics.parse(section, 2, arg)
                metrics.calc_metrics()
                row = metrics.get_df_row(line.split('/')[-1] + ('' if file_size == -1 else 'part '+str(p)))
                p += 1
                data_frame = pd.concat([data_frame, row], ignore_index=True)
        return data_frame

    def calc_data1(self):
        csv_path, _ = QFileDialog.getOpenFileNames(caption='Загрузите Бодрых')
        self.data_list1 = self.calc_df(csv_path)
        self.data_list_text1.setPlainText('')
        for line in self.data_list1['File']:
            self.data_list_text1.setPlainText(self.data_list_text1.toPlainText() + line + '\n')
    
    def calc_data2(self):
        csv_path, _ = QFileDialog.getOpenFileNames(caption='Загрузите Уставших')
        self.data_list2 = self.calc_df(csv_path)
        self.data_list_text2.setPlainText('')
        for line in self.data_list2['File']:
            self.data_list_text2.setPlainText(self.data_list_text2.toPlainText() + line + '\n')
        self.set_status(1)

    def save_data(self):
        file_name = QFileDialog.getSaveFileName(directory='_Data')
        print(file_name)
        # self.data_list1.to_csv(file_name[0] + '.csv', sep=';', index=False)
        d1 = self.data_list1.drop(columns=['File'])
        d2 = self.data_list2.drop(columns=['File'])
        gen = pd.concat([d1, d2],axis=0)
        d1 = (d1-gen.mean())/gen.std() 
        d2 = (d2-gen.mean())/gen.std() 
        d1 = pd.concat([self.data_list1['File'], d1], axis=1)
        d2 = pd.concat([self.data_list2['File'], d2], axis=1)
        self.data_list1.to_csv(file_name[0] + ' Бодрые.csv', sep=';', index=False)
        self.data_list2.to_csv(file_name[0] + ' Усталые.csv', sep=';', index=False)
        d1.to_csv(file_name[0] + ' Бодрые Норм.csv', sep=';', index=False)
        d2.to_csv(file_name[0] + ' Усталые Норм.csv', sep=';', index=False)

    def load_data(self):
        file_name = QFileDialog.getOpenFileName(directory='_Data', caption='Бодрые')
        self.data_list1 = pd.read_csv(file_name[0], sep=';')
        file_name = QFileDialog.getOpenFileName(directory='_Data', caption='Уставшие')
        self.data_list2 = pd.read_csv(file_name[0], sep=';')
        self.data_list_text1.setPlainText('')
        for line in self.data_list1['File']:
            self.data_list_text1.setPlainText(self.data_list_text1.toPlainText() + str(line) + '\n')
        self.data_list_text2.setPlainText('')
        for line in self.data_list2['File']:
            self.data_list_text2.setPlainText(self.data_list_text2.toPlainText() + str(line) + '\n')
        self.set_status(1)

    def take_sample(self):
        print('load edu button click')
        #self.eval_list = ParsedData.get_df_null_row() # pd.concat([self.data_list1, self.data_list2])
        self.edu_list1 = self.data_list1.sample(n=int(0.8*len(self.data_list1)))
        self.edu_list2 = self.data_list2.sample(n=int(0.8*len(self.data_list2)))
        ev1 = pd.concat([self.data_list1, self.edu_list1]).drop_duplicates(keep=False)
        ev2 = pd.concat([self.data_list2, self.edu_list2]).drop_duplicates(keep=False)
        self.eval_list = pd.concat([ev1, ev2], ignore_index=True)
        print(len(self.data_list1))
        print(len(self.data_list2))
        print(len(self.edu_list1))
        print(len(self.edu_list2))
        print(len(self.eval_list))
        self.edu_list_text1.setPlainText('')
        for _, row in self.edu_list1.iterrows():
            self.edu_list_text1.setPlainText(self.edu_list_text1.toPlainText() + str(row['File']) + '\n')            
        self.edu_list_text2.setPlainText('')
        for _, row in self.edu_list2.iterrows():
            self.edu_list_text2.setPlainText(self.edu_list_text2.toPlainText() + str(row['File']) + '\n')

        #print(self.eval_list)
        self.eval_list_text.setPlainText('')
        for _, row in self.eval_list.iterrows():
            self.eval_list_text.setPlainText(self.eval_list_text.toPlainText() + str(row['File']) + '\n')        
            
    def do_edu(self):
        if self.model_name == 'Basic':
            self.do_basic_edu()
        else:
            self.do_model_edu()

    def do_basic_edu(self):
        print('edu')
        print('---------')
        mean = [0] * len(ParsedData.get_df_null_row().drop(columns=['File']).columns.values)
        for _, row in self.edu_list1.iterrows():
            for i in range(1, len(row)):
                mean[i-1] += row[self.edu_list1.columns[i]]
        for i in range(0, len(mean)):
            mean[i] /= len(self.edu_list1)        
        self.ideal_max = ParsedData.get_df_null_row().drop(columns=['File'])
        self.ideal_max.loc[0] = mean
        
        print('---------')
        mean = [0] * len(ParsedData.get_df_null_row().drop(columns=['File']).columns.values)
        for _, row in self.edu_list2.iterrows():
            for i in range(1, len(row)):
                mean[i-1] += row[self.edu_list1.columns[i]]
        for i in range(0, len(mean)):
            mean[i] /= len(self.edu_list2)        
        
        self.ideal_min = ParsedData.get_df_null_row().drop(columns=['File'])
        self.ideal_min.loc[0] = mean
        self.set_status(2)
            

    def save_edu_file(self):
        pkl_filename = QFileDialog.getSaveFileName(directory='_Models')[0]
        if self.model_name == 'Base':
            with open(pkl_filename, 'wb') as file: 
                pickle.dump((self.ideal_min, self.ideal_max), file)
                print('Save')
                print(self.ideal_min)
        else:
            with open(pkl_filename, 'wb') as file: 
                pickle.dump(self.model, file) 


    def load_edu_file(self, pkl_filename ='model.pkl'):
        pkl_filename = QFileDialog.getOpenFileName(directory='_Models', caption='Загрузите модель')[0]
        if pkl_filename == '':
            return
        if self.model_name == 'Base':
            with open(pkl_filename, 'rb') as file: 
                base_model = pickle.load(file) 
                self.ideal_min = base_model[0]
                self.ideal_max = base_model[1]
                print('Load')
                print(self.ideal_min)
        else:
            #pkl_filename = "rfc_1_acc_1.00.pkl"
            with open(pkl_filename, 'rb') as file: 
                self.model = pickle.load(file)
                if self.model.get_name == 'MLP':
                    self.rb_mlp.setChecked(True)
                elif self.model.get_name == 'DTC':
                    self.rb_dtc.setChecked(True)
                elif self.model.get_name == 'RFC':
                    self.rb_rfc.setChecked(True)

        self.set_status(2)


    def do_model_eval(self):
        print('model eval')
        test_X = self.eval_list.drop(columns = ['File'])
        test_Y = pd.DataFrame({
            'fatique' : [1] * (len(self.data_list1) - len(self.edu_list1)) + [0] * (len(self.data_list2) - len(self.edu_list2))
        })
        y_pred = self.model.predict(test_X)
        m = accuracy_score(test_Y, y_pred)
        self.corr = m
        self.f1_line.setText(format(m,'.2f'))


    def do_eval(self):
        print('eval')
        #self.load_edu_file()
        self.res_list1 = ParsedData.get_df_null_row()
        self.res_list2 = ParsedData.get_df_null_row()
        #&#&#&@#@&#@#@#@#@#@#@#____________________---------------------     
        file_data = self.eval_list.drop(columns='File')
        #, self.data_list2.drop(columns='File'), ignore_index=True)
        #file_data = self.data_list2.drop(columns='File')
        
        if self.model_name == 'Basic':
            tired = BasicEval.evaluate(self.keys, self.ideal_max, self.ideal_min, row)
        else:
            for col in self.keys.head():
                if self.keys[col][0] == 0:
                    file_data = file_data.drop(columns=[col])
            tired = self.model.evaluate(file_data)
        for i in range(len(tired)):
            if not tired[i]:
                self.res_list1.loc[len(self.res_list1)] = self.eval_list['File'][i]
            else:
                self.res_list2.loc[len(self.res_list2)] = self.eval_list['File'][i]
        
        self.corr = 0
        self.err = 0
        print(self.res_list1)
        for _, row in self.res_list1.iterrows():
            if self.data_list_text1.toPlainText().__contains__(row['File']) : # gjghfdbnm
                self.corr += 1
            else:
                self.err += 1
        for _, row in self.res_list2.iterrows():
            if self.data_list_text2.toPlainText().__contains__(row['File']): #
                self.corr += 1
            else:
                self.err += 1
        #print('Corr: ' + str(self.corr) + '  Err: ' + str(self.err))
        corr_sum = self.corr / (self.corr + self.err)
        self.f1_line.setText(format(corr_sum, '.2f'))
        self.print_result()

   
    def print_result(self):
        print('print result')
        self.res_list_text1.setPlainText('')
        for _, row in self.res_list1.iterrows():
            self.res_list_text1.setPlainText(self.res_list_text1.toPlainText() + str(row['File']) + '\n')
        self.res_list_text2.setPlainText('')
        for _, row in self.res_list2.iterrows():
            self.res_list_text2.setPlainText(self.res_list_text2.toPlainText() + str(row['File']) + '\n')
        self.set_status(3)

    def do_model_edu(self, redu=False):
        #self.edu_list1 = 
        train_X = pd.concat([self.edu_list1.drop(columns = ['File']), self.edu_list2.drop(columns = ['File'])])
        test_X = self.eval_list.drop(columns = ['File'])
        for col in self.keys.columns:
            if self.keys[col][0] == 0 and col in train_X.columns:
                train_X = train_X.drop(columns=[col])
                test_X = test_X.drop(columns=[col])
        
        if self.normalize_box.isChecked():
            gen = pd.concat([train_X, test_X], ignore_index=True)
            train_X = (train_X - gen.mean())/gen.std()
            test_X = (test_X - gen.mean())/gen.std()

        train_Y = pd.DataFrame({
            'fatique' : [1] * len(self.edu_list1) + [0] * len(self.edu_list2)
        })
        test_Y = pd.DataFrame({
            'fatique' : [1] * (len(self.data_list1) - len(self.edu_list1)) + [0] * (len(self.data_list2) - len(self.edu_list2))
        })

        if redu:
            self.model.redu(train_X, train_Y, test_X, test_Y)   
        else:
            if self.model_name == 'RFC':
                self.model = RandomForestEval()
            elif self.model_name == 'DTC':
                self.model = DecisionTreeEval()
            elif self.model_name == 'MLP':
                self.model = MLPEval()
            if self.crossvalid_box.isChecked():
                data_X = pd.concat([self.data_list1.drop(columns = ['File']), self.data_list2.drop(columns = ['File'])], ignore_index=True)
                if self.normalize_box.isChecked():
                    data_X = (data_X - data_X.mean())/data_X.std()
                data_X.dropna()
                data_Y = pd.DataFrame({
                        'fatique' : [1] * len(self.data_list1) + [0] * len(self.data_list2)
                })
                data = pd.concat([data_X, data_Y], axis=1)
                data = data.sample(frac=1)
                data.to_csv('xx.csv', sep=';')
                data_Y = data['fatique']
                data_X = data.drop(columns=['fatique'])
                self.model.cross_edu(data_X, data_Y)
                self.f1_line.setText('F1: ' + format(self.model.f1,'.3f') + 
                                    ' Acc: ' + format(self.model.acc, '.3f'))
                self.crossvalid_label.setText('F1: ' + format(self.model.cross_f1,'.3f') + 
                                    ' Acc: ' + format(self.model.cross_acc, '.3f'))
            else:
                print(len(train_X), len(train_Y), len(test_X), len(test_Y))
                self.model.edu(train_X, train_Y, test_X, test_Y)
        #self.model = RandomForestEval.edu(train_X, train_Y, test_X, test_Y)

    def set_status(self, status):
        self.status = status
        self.status_text.setGeometry(0, self.height()-30, 3000, 30)
        self.reset_status_btn.setGeometry(self.width()-100, self.height()-30, 100, 30)
        self.status_img.setGeometry(0, self.height()-30, 3000, 30)

        '''
        for widget in self.data_group:
            widget.setEnabled(status == 0)
        for widget in self.edu_group:
            widget.setEnabled(status == 1)
        for widget in self.eval_group:
            widget.setEnabled(status > 1)
        for widget in self.res_group:
            widget.setEnabled(status == 3)
        '''

        if status == 0:
            self.status_text.setText('  Загрузите данные для обработки')
            self.status_img.setPixmap(QPixmap('UI/Red.png'))
        if status == 1:
            self.status_text.setText('  Обучите модель или загрузите уже обученную')
            self.status_img.setPixmap(QPixmap('UI/Orange.png'))
        if status == 2:
            self.status_text.setText('  Программа готова к запуску оценки')
            self.status_img.setPixmap(QPixmap('UI/Yellow.png'))
        if status == 3:
            self.status_text.setText('  Оценка выполнена')
            self.status_img.setPixmap(QPixmap('UI/Green.png'))


if __name__ == '__main__':
    app = QApplication(sys.argv)
    sleep(10)
    ex = EvalApp()
    sys.exit(app.exec_())

