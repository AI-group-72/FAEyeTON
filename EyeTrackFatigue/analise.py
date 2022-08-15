# модуль анализа входных данных, выделяющий интересующие нас метрики

# стадия 1

def interpolation(input_section):
    # первичная обработка данных
    return input_section


class ParsedData:
    def __init__(self):
        self.fixations = 0
        self.saccades = 0
        # все остальные метрики

    def parse(self, input_section):
        self.fixations = 1
        # вынимаем метрики из отрезка данных

    # надо обсудить, нужен или нет, с Владом и остальными
    def add(self, input_section):
        self.fixations -= 1
        # корректируем метрики с учётом новых данных


# стадия 2
# дополнить метрики


# стадия 3
# сделать комбинированные метрики
# выглядит скудно, но плюс минус так и есть
