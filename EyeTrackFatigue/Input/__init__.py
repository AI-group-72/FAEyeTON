# input init file
# модуль загрузки данных в систему
# сюда относится всё, связанное с считыванием и форматированием входных данных

# 1 : сделать считывание из csv или ещё как-то из айтрекера

# 2 : сделать потоковое считывание, хотя бы из эмулятора

# 3 : максимально отладить считывание, приваять UI для лйгкой настройки

from Input.SingleData import SingleData
from Input.InputSection import InputSection
from Input.InputStream import InputStream
from DeviceManager import DeviceHandler as dh


def read_video_file(path):
    # считывание файла

    return InputSection()


def read_csv_file(path):
    # считывание файла
    device = dh.DeviceHandler
    data = InputSection()
    data.add_data(device.request_data(path))
    return data


def init_reading_stream():
    # запуск потока ввода
    InputStream(dh.DeviceHandler())

