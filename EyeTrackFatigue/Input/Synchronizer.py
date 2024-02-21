import csv
import threading
import time
'''
класс для синхронизации подачи данных в режиме реального времени
'''

class Synchronizer:

    def __init__(self, path): # инициализация от пути к источнику данных
        self.path = path
        self.data = []
        self.file = open(path, newline='')
        self.reader = csv.reader(self.file, delimiter=',')
        self.prep_data()

    def prep_data(self): # подготовка данных
        i = 0
        i_time = i_x = i_y = 0
        first_line = self.reader.__next__()
        for key in first_line:  # автоматическое определение ключей данных
            if key.__contains__('time'): # ячейка времени, меняется в зависимости от формата данных окулографа
                i_time = i 
            if key.__contains__('pos_x'): # ячейка позиции по оси X, меняется в зависимости от формата данных окулографа
                i_x = i 
            if key.__contains__('pos_y'): # ячейка позиции по оси Y, меняется в зависимости от формата данных окулографа
                i_y = i
            i += 1
        row_count = 0
        for row in self.reader:
            self.data.append([row.__getitem__(i_time), row.__getitem__(i_x), row.__getitem__(i_y)])
            row_count += 1
        return self.data
    
    def start_stream(self): # запуск потока данных
        self.i = 0 # счетчик текущей позиции чтения данных
        self.time = self.data[self.i][0]
        self.last_request = 0
        self.thread = threading.Thread(target=self.run_stream)
        self.thread.start()

    def run_stream(self): # чтение данных в режиме реального времени
        while self.i < len(self.data):
            self.i += 1 # сдвиг позиции чтения данных
            self.time = self.data[self.i][0]
            time.sleep(self.time - self.data[self.i - 1][0]) # ожидание потока равно задержке между кадрами записи окулографа
    
    def request_data(self): # запрос данных выдаёт отрезок данных от предыдущего запроса до текущего
        data = self.data[self.last_request: self.i]
        print('Time since last request:',data[-1] - data[0])
        self.last_request = self.i
        


