# модуль с финальной оценкой данных, получаемых после работы модуля analise
# в основном работа ИИ

# стадия 1


# я думаю, лучше будет в классы запихнуть разные оценки
class BasicEval:
    def __init__(self):
        self.tired = False

    def eval(self, parsed_data):
        self.tired = True


# стадия 2


class RandomForestEval:
    def __init__(self):
        self.tired = False

    def eval(self, parsed_data):
        self.tired = True


class ANNEval:
    def __init__(self):
        self.tired = False

    def eval(self, parsed_data):
        self.tired = True


# плюс реестр обучающих выборок, но это ещё обсудить надо

# стадия 3
# тут будем доделывать по заявке
