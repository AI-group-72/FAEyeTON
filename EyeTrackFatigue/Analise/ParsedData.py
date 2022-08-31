import math


class ParsedData:
    def __init__(self):
        self.FOV = 82 * math.sqrt(2)
        self.dots = 0
        self.time_frame = 0
        self.minSpeed = 0
        self.avrSpeed = 0
        self.maxSpeed = 0
        self.minDist = 0
        self.maxDist = 0
        self.fixations = 0
        self.saccades = 0
        # все остальные метрики

    def parse(self, input_section):
        self.dots = len(input_section.positionData)
        self.time_frame = input_section.time_frame()
        self.minSpeed = min(input_section.velocityData) * self.FOV
        self.maxSpeed = max(input_section.velocityData) * self.FOV
        self.avrSpeed = sum(input_section.distanceData) / self.time_frame * self.FOV
        self.minDist = min(input_section.distanceData) * self.FOV
        self.maxDist = max(input_section.distanceData) * self.FOV

        self.fixations = 1
        # вынимаем метрики из отрезка данных

    # надо обсудить, нужен или нет, с Владом и остальными
    def add(self, input_section):
        self.fixations -= 1
        # корректируем метрики с учётом новых данных

    def __str__(self):
        s = '__Metrics:__\n'
        s += 'Time Frame: ' + self.time_frame.__str__() + ' Dots count: ' + self.dots.__str__() + '\n'
        s += 'Estimated Hrz: ' + (self.dots / self.time_frame).__str__() + '\n'
        s += 'Min Speed: ' + f'{self.minSpeed:.6f}' + '\n'
        s += 'Max Speed: ' + f'{self.maxSpeed:.6f}' + '\n'
        s += 'Avr Speed: ' + f'{self.avrSpeed:.6f}' + '\n'
        s += 'Min Distance: ' + f'{self.minDist:.6f}' + '\n'
        s += 'Max Distance: ' + f'{self.maxDist:.6f}' + '\n'
        return s
