import csv


class DeviceHandler:
    def __init__(self):
        self.path = 'System path'
        self.data = []
        self.line_count = 0

    def __init__(self, path):
        self.path = path
        self.data = []
        self.file = open(path, newline='')
        self.reader = csv.reader(self.file, delimiter=',')

    def request_data(self):
        i = 0
        i_time = i_x = i_y = 0
        i_h = -1
        first_line = self.reader.__next__()
        for key in first_line:
            if key.__contains__('time'):
                i_time = i
            if key.__contains__('head_pos_x'):
                i_x = i
            if key.__contains__('head_pos_y'):
                i_y = i
            #if key.__contains__('time'):
             #   i_h = i    
            i += 1

        print('Time column: ' + i_time.__str__() + ' X column: ' + i_x.__str__() + ' Y column: ' + i_y.__str__())
        row_count = 0
        for row in self.reader:
            self.data.append([row.__getitem__(i_time), row.__getitem__(i_x), row.__getitem__(i_y)])
            row_count += 1

        return self.data
