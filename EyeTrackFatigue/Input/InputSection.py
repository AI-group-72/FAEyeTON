import math

from Input.SingleData import SingleData


class InputSection:
    def __init__(self):
        self.dotCount = 0
        self.positionData = []
        self.distanceData = []
        self.velocityData = []

    def add_data_array(self, raw_data_array):
        for raw_data in raw_data_array:
            self.add_data(raw_data)

    def add_data(self, raw_data):
        self.dotCount += 1
        self.positionData.append(SingleData(raw_data))
        if len(self.positionData) > 1:
            self.distanceData.append(self.positionData[-1].get_distance(self.positionData[-2]))
            self.velocityData.append(self.distanceData[-1] / (self.positionData[-1].time - self.positionData[-2].time))

    def time_frame(self):
        return self.positionData[-1].time - self.positionData[0].time

    def __str__(self):
        s = 'Input Section:\n'
        for data in self.positionData:
            s += data.__str__() + '\n'
        return s
