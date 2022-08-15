# модуль загрузки данных в систему

# стадия 1

class SingleData:
    def __init__(self):
        self.x = 0
        self.y = 0
        self.time = 0
        # метрики поворота головы


class InputSection:
    def __init__(self):
        self.data = []

    def add_data(self, single_data):
        self.data.append(single_data)


def read_video_file(path):
    # считывание файла
    return InputSection()

# стадия 2


def read_csv_file(path):
    # считывание файла
    return InputSection()


def init_reading_stream(path):
    # запуск потока ввода
    path = path


# вероятно нужно будет завексти класс на поток ввода
class InputStream:
    def __init__(self, path):
        self.path = path


# стадия 3


# тут уже пойдёт UI в основном
