# модуль анализа входных данных, выделяющий количественные характеристики
# основной класс - ParsedData, объединяет методы вычисления, обработки и хранение данных о количественных характеристиках
from ..Input import read_csv_file
from ..Analise.ParsedData import ParsedData


# Парсинг по умолчанию
def parse_ff_tf(file_from, file_to):
    section = read_csv_file(file_from)
    metrics = ParsedData()
    metrics.parse(section, 3, 5)
    metrics.to_csv(file_from, file_to)

# Проверка данных на наличие пред-обработки / интерполяции
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
