# модуль анализа входных данных, выделяющий интересующие нас метрики
from Input import read_csv_file
from ParsedData import ParsedData
# стадия 1

def clear(input_section):
    # первичная обработка данных
    return input_section


def interpolation(input_section):
    # первичная обработка данных
    return input_section


section = read_csv_file('../test_data.csv')
metrics = ParsedData()
metrics.parse(section)
print(metrics)