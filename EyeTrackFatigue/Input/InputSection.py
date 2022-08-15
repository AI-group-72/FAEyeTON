import SingleData as SD

class InputSection:
    def __init__(self):
        self.data = []

    def add_data(self, single_data):
        if single_data is SD.SingleData:
            self.data.append(single_data)
