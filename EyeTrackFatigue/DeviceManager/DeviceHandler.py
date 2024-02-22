import csv

class DeviceHandler:
    # вариант инициализации с предзаданым путём
    def __init__(self):
        self.path = 'System path' # необходимо указать системный путь
        self.data = []
        self.line_count = 0
    # инициализация по указанному пути
    def __init__(self, path):
        self.path = path
        self.data = []
        # по умолчанию работает со стандартными таблицами формата .csv
        self.file = open(path, newline='')
        self.reader = csv.reader(self.file, delimiter=',')
    # функция запроса данных
    def request_data(self):
        i = 0
        i_time = i_x = i_y = 0
        i_h = -1
        first_line = self.reader.__next__()
        # автоматическое определение ключей данных
        # необходимо скорректировать ключи если формат используемых данных у используемого окулографа отличается
        for key in first_line:  
            if key.__contains__('time'): # ячейка времени, меняется в зависимости от формата данных окулографа
                i_time = i 
            if key.__contains__('pos_x'): # ячейка позиции по оси X, меняется в зависимости от формата данных окулографа
                i_x = i 
            if key.__contains__('pos_y'): # ячейка позиции по оси Y, меняется в зависимости от формата данных окулографа
                i_y = i
            i += 1
        # опциональное подтверждение корректного определения нужных колонок данных
        print('Time column: ' + i_time.__str__() + ' X column: ' + i_x.__str__() + ' Y column: ' + i_y.__str__())
        row_count = 0
        # считывание данных
        for row in self.reader:
            self.data.append([row.__getitem__(i_time), row.__getitem__(i_x), row.__getitem__(i_y)])
            row_count += 1

        return self.data
