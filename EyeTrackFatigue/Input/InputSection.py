import math

from .SingleData import SingleData


class InputSection:

    def __init__(self):
        self.FOV = 1 # 82 * math.sqrt(2)

        self.dotCount = 0
        self.positionData = []
        self.distanceData = []
        self.velocityData = []

    def add_data_array(self, raw_data_array):
        for raw_data in raw_data_array:
            self.add_data(raw_data)

    def add_data(self, raw_data):
        self.dotCount += 1
        self.positionData.append(SingleData(raw_data, self.FOV))
        if len(self.positionData) > 1:
            self.distanceData.append(self.positionData[-1].get_distance(self.positionData[-2]))
            self.velocityData.append(self.distanceData[-1] / (self.positionData[-1].time - self.positionData[-2].time))

    def time_frame(self):
        return self.positionData[-1].time - self.positionData[0].time

    def split(self, size):
        if self.time_frame() < size or size == -1:
            return [self]
        split_list = []
        count = self.time_frame() // size
        time_span = self.time_frame() / count
        i = 0
        time = 0
        section = InputSection()
        while i < len(self.positionData):
            section.dotCount += 1
            section.positionData.append(self.positionData[i])
            if section.dotCount > 1:
                section.distanceData.append(section.positionData[-1].get_distance(section.positionData[-2]))
                section.velocityData.append(section.distanceData[-1] / (section.positionData[-1].time - section.positionData[-2].time))
                time += section.positionData[-1].time - section.positionData[-2].time
            if time > time_span and len(split_list) < count:
                time = 0
                split_list.append(section)
                section = InputSection()
            i += 1
        
        if len(split_list) < count:
            split_list.append(section)

        return split_list

    def __str__(self):
        s = 'Input Section:\n'
        for data in self.positionData:
            s += data.__str__() + '\n'
        return s

    