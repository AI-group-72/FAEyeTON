# модуль для построения графиков данных, получаемых в ходе работы программы,
# а также имитации работы программы в реальном времени
# нужен для отладки и демонстрации работы программы

# стадия 1

def plot_input_data(input_section):
    # построение считанных данных, например хит-мапом
    a = 0


def plot_parsed_data(parsed_data):
    # построение графиков фиксаций, саккад
    a = 0

# стадия 2
# тут нужно будет доработать/откопировать прошлые методы для построения графиков во времени

# и добавить потоковую эмуляцию, например считывающую группу видео (или просто большой ролик)
# чтобы по кускам подавать на вход


def emulate(path_to_files):
    a = 0


# можно попробовать сделать эмулятор рандомизирующий данные от каких-то параметров, если тестовых данных будет мало
def random_emulate():
    a = 1


def plot_f_value(result, check):
    # сравнение результатов оценки с экспертным, вычисление ф-меры
    a = 2

# стадия 3
# здесь нужно будет сделать гибкий выбор параметров, по которым строить графики, и запускать перекрёстный тест
# например что нам на одинх и тех же данных даёт рандом-форест, а что нейросетка
# или что нам даёт проверка одних метрик в сравнении с другими, и т.д.
