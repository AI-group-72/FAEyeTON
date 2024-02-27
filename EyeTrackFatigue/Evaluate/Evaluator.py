from abc import ABC, abstractmethod
# абстрактный класс, задающий основную логику для классов описывающих различные модели оценки
class Evaluator(ABC):
    @abstractmethod
    def evaluate(self, data):
        return False
