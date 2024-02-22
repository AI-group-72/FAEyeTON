import math

# Фрагмент данных
class SingleData:
    def __init__(self):
        self.x = 0
        self.y = 0
        self.time = 0
    # инициализация с учётом угла обзора камеры сцены (задаётся в классе InputSection)
    def __init__(self, raw_data, fov):
        self.time = float(raw_data[0])
        self.x = float(raw_data[1]) * fov
        self.y = float(raw_data[2]) * fov
    # инициализация промежуточного кадра (исползуется для апроскимации )
    def approx(data1, data2, j, count): # j - номер кадра в промежутке, count - их обзщее количество
        sd = SingleData()
        sd.time = data1.time + (data2.time-data1.time) / count * j
        sd.x = data1.x + (data2.x-data1.x) / count * j
        sd.y = data1.y + (data2.y-data1.y) / count * j
        return sd
    # отображение в стороков формате
    def __str__(self):
        return self.time.__str__() + ': ' + self.x.__str__() + ' ; ' + self.y.__str__()
    # рассчёт дистаниции между двумя точками
    def get_distance(self, other):
        return math.sqrt(math.pow(self.x-other.x, 2) + math.pow(self.y-other.y, 2))
