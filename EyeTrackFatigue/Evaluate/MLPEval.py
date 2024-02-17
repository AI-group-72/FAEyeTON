import datetime
import pandas as pd
import warnings
warnings.filterwarnings("ignore")
from sklearn.neural_network import MLPClassifier
from sklearn.metrics import (
    confusion_matrix,
    accuracy_score,
    precision_score,
    recall_score,
    f1_score
)

from Evaluate.Evaluator import Evaluator

class MLPEval(Evaluator):
    def __init__(self):
        self.model = None
        self.acc = -1
        self.f1 = -1

    def get_name(self):
        return 'MLP'
    
    def evaluate(self, data):
        if self.model == None:
            print('Not educated yet')
        else:
            return self.model.predict(data)

    def redu(self, train_X, train_Y, test_X, test_Y):
        self.model.fit(train_X, train_Y)
        y_pred = self.model.predict(test_X)
        self.acc = accuracy_score(test_Y, y_pred)
        self.f1 = f1_score(test_Y, y_pred)        

    def edu(self, train_X, train_Y, test_X, test_Y):
        sol = ['lbfgs', 'sgd', 'adam']
        ac = ['identity', 'logistic', 'tanh', 'relu']
        err = 0
        now1 = datetime.datetime.now()
        print(now1)
        for i in range(1, 100):
            print(i)
            for j in range(1,20):
                for s in sol:
                    for a in ac:
                        model = MLPClassifier(solver=s, activation = a, alpha=1e-5, hidden_layer_sizes=(j), random_state=i)
                        model.fit(train_X, train_Y)
                        y_pred = model.predict(test_X)
                        f = f1_score(test_Y, y_pred)
                        if f > err:
                            print(f)
                            rand = i
                            err = f
                            h = j
                            Ac = a
                            S = s
        print(h)
        print(rand)
        print(Ac)
        print(S)
        
        now = datetime.datetime.now()
        print(now)
        print('Total time:', now - now1)

        self.model = MLPClassifier(solver=S, activation = Ac, alpha=1e-5, hidden_layer_sizes=(h), random_state=rand)
        self.model.fit(train_X, train_Y)
        y_pred = self.model.predict(test_X)
        m = accuracy_score(test_Y, y_pred)
        f = f1_score(test_Y, y_pred)
        self.acc = accuracy_score(test_Y, y_pred)
        self.f1 = f1_score(test_Y, y_pred)  
        print(m)
        print(f)

    # Обучение с кроссвалидацией / Training with crossvalidation
    def cross_edu(self, data_X, data_Y):
        now1 = datetime.datetime.now()
        print(now1) # Время начала обучения / Training start timestamp 
        # Формирования выборок для 5-фолдовой кроссвалидции
        # Formimng datasamples for 5-fold crossvalidation
        teX = []
        teY = []
        trX = []
        trY = [] 
        step = len(data_X) // 5
        for cross in range(5):                                     
            test_X = data_X.iloc[cross * step : (cross + 1) * step]
            test_Y = data_Y.iloc[cross * step : (cross + 1) * step]
            train_X = pd.concat([data_X.iloc[:cross * step], data_X.iloc[(cross + 1) * step:]], ignore_index=True)
            train_Y = pd.concat([data_Y.iloc[:cross * step], data_Y.iloc[(cross + 1) * step:]], ignore_index=True)
            teX.append(test_X)
            teY.append(test_Y)
            trX.append(train_X)
            trY.append(train_Y)
            print(len(trX[cross]))
            print(sum(trY[cross]))
            print(len(teX[cross]))
            print(sum(teY[cross]))
        # Обучение / Training
        sol = ['lbfgs', 'sgd', 'adam']
        ac = ['identity', 'logistic', 'tanh', 'relu']
        err = 0
        for i in range(5): # перебор случайных состояний / iterating through random states
            print(i)
            for j in range(1,20): # Перебор параметров / Iterating through the parameters
                for s in sol:
                    for a in ac:
                        model = MLPClassifier(solver=s, activation = a, alpha=1e-5, hidden_layer_sizes=(j), random_state=i)
                        f = 0
                        acc = 0
                        cur_f = 0
                        for cross in range(5): # Кроссвалидированное обучение / Cross-validated training
                            test_X = teX[cross]
                            test_Y = teY[cross]
                            train_X = trX[cross]
                            train_Y = trY[cross]
                            model.fit(train_X, train_Y)
                            y_pred = model.predict(test_X)
                            _f = f1_score(test_Y, y_pred)
                            if _f < 0.60 or _f < (cur_f-0.15): # Досрочное отбрасываение - опционально, для оптимизации
                                break
                            if _f > cur_f:
                                cr = cross
                            f += _f
                            acc += accuracy_score(test_Y, y_pred)
                        f = f / 5
                        acc = acc / 5
                        if f > err: # Сравнение текущей модели с лучшей / Comparing the current model with the best one
                            # Cохранение параметров и показателей / Saving parameters and indicators
                            print(f)
                            cross_acc = acc 
                            rand = i
                            err = f
                            h = j
                            Ac = a
                            S = s
        print(h)
        print(rand)
        print(Ac)
        print(S)
        
        now = datetime.datetime.now()
        print(now)
        # Время окончания обучения / Training end timestamp 
        print('Total time:', now - now1)
        test_X = teX[cr]
        test_Y = teY[cr]
        train_X = trX[cr]
        train_Y = trY[cr] 
        # обучение модели по параметрам лучший / training the model according to the best parameters
        self.model = MLPClassifier(solver=S, activation = Ac, alpha=1e-5, hidden_layer_sizes=(h), random_state=rand)
        self.model.fit(train_X, train_Y)
        y_pred = self.model.predict(test_X)
        self.acc = accuracy_score(test_Y, y_pred) # результаты по одному из разбиений / results for one sample
        self.f1 = f1_score(test_Y, y_pred)
        self.cross_f1 = err # усреднённые результаты по всем разбиениям / averaged results for all samples
        self.cross_acc = cross_acc

    
    def edu_args(self, train_X, train_Y, test_X, test_Y, solver, activation, h_l_s, rand_state):
        #for i in range(100):
        model = MLPClassifier(solver=solver, activation=activation, alpha=1e-5, hidden_layer_sizes=(h_l_s), random_state=rand_state)
        model.fit(train_X, train_Y)
        y_pred = model.predict(test_X)
        self.acc = accuracy_score(test_Y, y_pred)
        self.f1 = f1_score(test_Y, y_pred)  
        #solver='lbfgs', activation = 'logistic', hidden_layer_sizes=(12)
        
# 18
# 30
        
# gini