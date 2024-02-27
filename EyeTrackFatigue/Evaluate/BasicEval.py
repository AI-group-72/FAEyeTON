from ..Evaluate.Evaluator import Evaluator
import numpy as np
# модель алгоретмической оценки утомления
class BasicEval(Evaluator):
    def __init__(self):
        self.corrs = []
    
    def get_name(self):
        return 'Basic'

    def edu(self, train_X, train_Y, test_X, test_Y):  # обучение - сигнатура метода выполнена в стандартном виде для моделей машинного обучения (для удодбства)
        # однако используется алгоритмический подход - математически вычисляются линйные корреляции по известным характеристикам на получаемом наборе данных
        self.corrs = []
        for col in train_X.columns:
            Sum_xy = sum((train_X[col]-train_X[col].mean())*(train_Y[train_Y.columns[0]]-train_Y[train_Y.columns[0]].mean()))
            Sum_x_squared = sum((train_X[col]-train_X[col].mean())**2)
            Sum_y_squared = sum((train_Y[train_Y.columns[0]]-train_Y[train_Y.columns[0]].mean())**2)       
            self.corrs.append(Sum_xy / np.sqrt(Sum_x_squared * Sum_y_squared))

    def evaluate(self, data):
        pred_Y = []
        # при оценке все признаки входных данных вносят вклад в итоговую классификаций в соответствии с показателем корреляции 
        for _, row in data.iterrows():
            fl = 0
            for i in range(len(row)):
                fl += row[i] * self.corrs[i]
                #fl += 1 if abs(row[i] - self.tired[i]) < abs(row[i] - self.fresh[i]) else -1
            pred_Y.append(0 if fl < 0 else 1)
        return pred_Y
            
