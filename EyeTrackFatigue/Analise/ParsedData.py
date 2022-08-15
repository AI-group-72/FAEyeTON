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
