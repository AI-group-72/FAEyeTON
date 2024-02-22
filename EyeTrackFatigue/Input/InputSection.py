import math
from .SingleData import SingleData
# класс для работы с отрезками данных
class InputSection:
    # инициализация
    def __init__(self):
        self.FOV = 82 * math.sqrt(2) # указывается угол обзора камеры сцены, далее по коду значение не меняется
        # параметр FOV может отличатся в зависимости от модели используемого окулографа, при необходимости требуется корректировка
        self.dotCount = 0
        self.positionData = []
        self.distanceData = []
        self.velocityData = []
    # добавление данных массивом
    def add_data_array(self, raw_data_array):
        for raw_data in raw_data_array:
            self.add_data(raw_data)
    # добавление отдельными строками
    def add_data(self, raw_data):
        self.dotCount += 1 # инкрементация количества кадров в отрезке
        self.positionData.append(SingleData(raw_data, self.FOV)) # формирование данных, с учётом угла обзора сцены
        if len(self.positionData) > 1: # добавление данных о дистанции и скорости движения для всех кадров, следующих за стартовым
            self.distanceData.append(self.positionData[-1].get_distance(self.positionData[-2]))
            self.velocityData.append(self.distanceData[-1] / (self.positionData[-1].time - self.positionData[-2].time))
    # прореживание данных - отбрасывание промежуточных кадров 
    # можно использовать для сокращения объема обрабатываемых данных, как следствие -> более быстрого ведения вычислений
    def thin_data(self, fraq=0.5): # fraq - доля оставляемых данных
        if fraq >= 1:
            return
        step = 1 / fraq 
        cur_i = 0
        cur_s = 0
        i = 0
        while i < self.dotCount-1:
            cur_s += step 
            cur_i = int(cur_s % 1) # определяем, сколько кадров вырезать на этом шаге
            cur_s -= cur_i 
            while cur_i > 0: 
                self.positionData.pop(i+1) # удаляем позицию следующего кадра
                self.distanceData.pop(i) # удаляем дистанцию
                self.velocityData.pop(i) # удаляем скорость
                self.dotCount -= 0
                cur_i -= 1
            self.distanceData.insert(i, self.positionData[i+1].get_distance(self.positionData[i])) # вставляем перерассчитанную дистанцию
            self.velocityData.insert(i, self.distanceData[i] / (self.positionData[i+1].time - self.positionData[i].time)) # вставляем перерассчитанную скорость
            i += 1

    # аппроксимация данных - добавление промежуточных кадров 
    # можно использовать для увеличение объема обрабатываемых данных, в случае работы с, например, сильно прореженной записью
    # потенциально увеличит точность вычислений за счёт более долгого время их проведения
    def aprox_data(self, frames=1): # frames - количество вставляемых кадров
        i = 0
        while i < self.dotCount-1:
            for j in range(frames+1):
                self.positionData.insert(i+j+1, SingleData.approx(self.positionData[i], self.positionData[i+j+1], j+1, frames+1)) # аппрокисируем позицию следующего кадра
                self.distanceData.insert(i, self.positionData[i+j+1].get_distance(self.positionData[i+j])) # вставляем перерассчитанную дистанцию
                self.velocityData.insert(i, self.distanceData[i+j] / (self.positionData[i+j+1].time - self.positionData[i+j].time)) # вставляем перерассчитанную скорость
                self.dotCount += 1
            i += 1 + frames # переходим через добавленные промежуточные кадры


    # запрос покрываемого отрезка времени
    def time_frame(self):
        return self.positionData[-1].time - self.positionData[0].time
    # разбиение отрезка на подотрезки фиксированного размера (по времени)
    def split(self, size):
        if self.time_frame() < size or size == -1: # проверка, следует ли проводить разбиение
            return [self]
        split_list = []
        count = self.time_frame() // size # вычисляем количество искомых подотрезков
        time_span = self.time_frame() / count # вычисляем оптимальную длительность подотрезков для равного разбиения
        i = 0
        time = 0
        section = InputSection() # создаем подотрезок
        while i < len(self.positionData):
            section.dotCount += 1
            section.positionData.append(self.positionData[i])
            if section.dotCount > 1:
                section.distanceData.append(section.positionData[-1].get_distance(section.positionData[-2]))
                section.velocityData.append(section.distanceData[-1] / (section.positionData[-1].time - section.positionData[-2].time))
                time += section.positionData[-1].time - section.positionData[-2].time # подсчёт времени
            if time > time_span and len(split_list) < count: # проверка на превышение оптимальной длительности (и границу отрезка)
                time = 0 
                split_list.append(section) # сохраняем сформированный подотрезок 
                section = InputSection() # создаём новый подотрезок
            i += 1
        
        if len(split_list) < count: # добавляем последний отрезок (в случае если разделение не ровное)
            split_list.append(section)

        return split_list 
    # отображение отрезка данных в строковом виде
    def __str__(self):
        s = 'Input Section:\n'
        for data in self.positionData:
            s += data.__str__() + '\n'
        return s
