# input init file
# модуль загрузки данных в систему
# сюда относится всё, связанное с считыванием и форматированием входных данных


from .InputSection import InputSection
from ..DeviceManager.DeviceHandler import DeviceHandler
from ..DeviceManager.Synchronizer import Synchronizer


def read_video_file(path):
    # считывание файла
    return InputSection()


def read_csv_file(path):
    # считывание файла
    device = DeviceHandler(path)
    data = InputSection()
    data.add_data_array(device.request_data())
    return data

def init_reading_stream(path):
    # запуск потока ввода
    sync = Synchronizer(path)
    #sync.start_stream()
