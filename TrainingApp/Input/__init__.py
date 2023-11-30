# input init file
# модуль загрузки данных в систему
# сюда относится всё, связанное с считыванием и форматированием входных данных

# 1 : сделать считывание из csv или ещё как-то из айтрекера

# 2 : сделать потоковое считывание, хотя бы из эмулятора

# 3 : максимально отладить считывание, приваять UI для лйгкой настройки


from .InputSection import InputSection
from .InputStream import InputStream
from DeviceManager import DeviceHandler


def read_video_file(path):
    # считывание файла
    return InputSection()


def read_csv_file(path):
    # считывание файла
    device = DeviceHandler(path)
    data = InputSection()
    data.add_data_array(device.request_data())
    return data


def init_reading_stream():
    # запуск потока ввода
    InputStream(DeviceHandler())


# section = read_csv_file('../test_data.csv')
# print(section)
#
