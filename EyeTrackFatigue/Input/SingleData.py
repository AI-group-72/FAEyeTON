import math


class SingleData:
    def __init__(self):
        self.x = 0
        self.y = 0
        self.time = 0
        # метрики поворота головы

    def __init__(self, raw_data):
        self.time = float(raw_data[0])
        self.x = float(raw_data[1])
        self.y = float(raw_data[2])
        # метрики поворота головы

    def __str__(self):
        return self.time.__str__() + ': ' + self.x.__str__() + ' ; ' + self.y.__str__()

    def get_distance(self, other):
        return math.sqrt(math.pow(self.x-other.x, 2) + math.pow(self.y-other.y, 2))