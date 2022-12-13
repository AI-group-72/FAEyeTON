# модуль анализа входных данных, выделяющий интересующие нас метрики
from Input import read_csv_file
from Analise.ParsedData import ParsedData


# стадия 1

def clear(input_section):
    # первичная обработка данных
    return input_section


def interpolation(input_section):
    # первичная обработка данных
    return input_section


def parse_ff_tf(file_from, file_to):
    section = read_csv_file(file_from)
    metrics = ParsedData()
    metrics.parse(section, 3, 5)
    metrics.to_csv(file_from, file_to)


def check_interpolation():
    section = read_csv_file('../test_data1.csv')
    s = 0
    d = 0.001
    for i in range(1, len(section.positionData) - 1):
        if abs(section.positionData[i].get_distance(section.positionData[i - 1])
               - section.positionData[i].get_distance(section.positionData[i + 1])) < d:
            s += 1
    print("Suspicion: " + (s / len(section.positionData)).__str__())
    print(s)

'''
section = read_csv_file('../test_data1.csv')
metrics = ParsedData()
metrics.parse(section, 1, 5, 2.5)
metrics.to_xls('test_data1', '../UI/masterfile.xlsx')
'''