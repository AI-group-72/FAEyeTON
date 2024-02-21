import pickle
from Evaluate.MLPEval import MLPEval
from Evaluate.DecisionTreeEval import DecisionTreeEval
from Evaluate.RandomForestEval import RandomForestEval
from Evaluate.BasicEval import BasicEval
from sklearn.metrics import (
    accuracy_score,
    f1_score
)
# класс, реализующий гибридную оценку
class HybridEval():
    def __init__(self):
        self.models = []
        self.acc = -1
        self.f1 = -1


    def edu(self, train_X, train_Y, test_X, test_Y, model_names):
        if model_names.__contains__('Basic'):
            basic = BasicEval()
            basic.edu(train_X, train_Y, test_X, test_Y)
            self.models.append(basic)
            pickle.dump(basic, open('H_bsc', 'wb')) 
        if model_names.__contains__('DCT'):
            dct = DecisionTreeEval()
            dct.edu(train_X, train_Y, test_X, test_Y)
            self.models.append(dct)
            pickle.dump(dct, open('H_dct', 'wb')) 
        if model_names.__contains__('RFC'):
            rfc = RandomForestEval()
            rfc.edu(train_X, train_Y, test_X, test_Y)
            self.models.append(rfc)
            pickle.dump(rfc, open('H_rfc', 'wb')) 
        if model_names.__contains__('MLP'):
            mlp = MLPEval()
            mlp.edu(train_X, train_Y, test_X, test_Y)
            self.models.append(mlp)
            pickle.dump(mlp, open('H_mlp', 'wb')) 
        
    def load(self, model_names):
        if model_names.__contains__('Basic'):
            basic = pickle.load(open('H_bsc', 'rb')) 
            self.models.append(basic)
        if model_names.__contains__('DCT'):
            dct = pickle.load(open('H_dct', 'rb')) 
            self.models.append(dct)
        if model_names.__contains__('RFC'):
            rfc = pickle.load(open('H_rfc', 'rb')) 
            self.models.append(rfc)
        if model_names.__contains__('MLP'):
            mlp = pickle.load(open('H_mlp', 'rb')) 
            self.models.append(mlp)

    def eval(self, test_X, test_Y):
        preds = []
        for model in self.models:
            y_pred = model.evaluate(test_X)
            preds.append(y_pred)
            self.f1 = f1_score(test_Y, y_pred) # результаты по одному из разбиений / results for one sample
            self.acc = accuracy_score(test_Y, y_pred)
        
        sure = []
        unsure = []
        test_sure = []
        test_unsure = []
        for j in range(len(preds[0])):
            p_sum = preds[0][j]
            for i in range(1,len(self.models)):
                p_sum += preds[i][j]
            if p_sum == 0 or p_sum == len(self.models):
                sure.append(preds[0][j])
                test_sure.append(test_Y['AU_cat'][j])
            else:
                unsure.append(p_sum / len(self.models))
                test_unsure.append(test_Y['AU_cat'][j])

        print('Sure:', format(len(sure) / (len(sure) + len(unsure)) * 100, '.2f') + '%', 'F1:', f1_score(sure, test_sure))
        unsure = self.filter(unsure, 0.1)
        print('UnSure:', format(len(unsure) / (len(sure) + len(unsure)) * 100, '.2f') + '%', 'F1:', f1_score(unsure, test_unsure))
        
    def filter(self, pred, treshold):
        for i in range(len(pred)):
            if pred[i] >= treshold:
                pred[i] = 1
            else:
                pred[i] = 0
        return pred



#D:\PythonProjects\Faeyeton\_Data