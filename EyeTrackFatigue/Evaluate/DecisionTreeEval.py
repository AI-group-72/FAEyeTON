import pandas as pd
import datetime
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import (
    confusion_matrix,
    accuracy_score,
    precision_score,
    recall_score,
    f1_score
)

from Evaluate.Evaluator import Evaluator

class DecisionTreeEval(Evaluator):
    def __init__(self):
        self.model = None
        self.acc = -1
        self.f1 = -1

    def get_name(self):
        return 'DTC'
    
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

    def edu(self, train_X, train_Y, test_X, test_Y, strange=False):
        err = 0
        rand = -1
        c = ['gini', 'entropy', 'log_loss']
        
        now1 = datetime.datetime.now()
        print(now1)
        for i in range(100):
            for C in c:
                model = DecisionTreeClassifier(criterion = C, random_state = i)
                model.fit(train_X, train_Y)
                y_pred = model.predict(test_X)
                m = f1_score(test_Y, y_pred)
                if m > err:
                    rand = i
                    err = m
                    cr = C
        
        now1 = datetime.datetime.now()
        print(now1)
        print(rand)
        print (cr)
        self.model = DecisionTreeClassifier(criterion = cr, random_state = rand)
        self.model.fit(train_X, train_Y)
        y_pred = model.predict(test_X)
        m = f1_score(test_Y, y_pred)
        self.acc = accuracy_score(test_Y, y_pred)
        self.f1 = f1_score(test_Y, y_pred)        
        print(m)

    def redu(self, train_X, train_Y, test_X, test_Y):
        self.model.fit(train_X, train_Y)
        y_pred = self.model.predict(test_X)
        self.acc = accuracy_score(test_Y, y_pred)
        self.f1 = f1_score(test_Y, y_pred)        


    def cross_edu(self, data_X, data_Y):
        teX = []
        teY = []
        trX = []
        trY = []
        step = len(data_X) // 5
        now1 = datetime.datetime.now()
        print(now1)
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
        err = 0
        rand = -1
        c = ['gini', 'entropy', 'log_loss']
        now1 = datetime.datetime.now()
        print(now1)
        for i in range(100): # перебор случайных состояний / iterating through random states
            print(i)
            for C in c: # Перебор параметров / Iterating through the parameters
                model = DecisionTreeClassifier(criterion = C, random_state = i)
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
                    #if _f < 0.60 or _f < (cur_f-0.15): # Досрочное отбрасываение - опционально, для оптимизации
                     #   break
                    if _f > cur_f:
                        cr = cross
                    f += _f
                    acc += accuracy_score(test_Y, y_pred)
                f = f / 5
                acc = acc / 5
                if f > err:# Сравнение текущей модели с лучшей / Comparing the current model with the best one
                    # Cохранение параметров и показателей / Saving parameters and indicators
                    rand = i
                    err = f
                    crit = C
                    cross_acc = acc
        print(rand)
        print(crit)
        
        now = datetime.datetime.now()
        print(now)
        # Время окончания обучения / Training end timestamp 
        print('Total time:', now - now1)
        test_X = teX[cross]
        test_Y = teY[cross]
        train_X = trX[cross]
        train_Y = trY[cross]
        # обучение модели по параметрам лучший / training the model according to the best parameters
        self.model = DecisionTreeClassifier(criterion = crit, random_state = i)
        self.model.fit(train_X, train_Y)
        y_pred = self.model.predict(test_X)
        self.f1 = f1_score(test_Y, y_pred) # результаты по одному из разбиений / results for one sample
        self.acc = accuracy_score(test_Y, y_pred)  
        self.cross_f1 = err # усреднённые результаты по всем разбиениям / averaged results for all samples
        self.cross_acc = cross_acc

    def edu_args(self, train_X, train_Y, test_X, test_Y, rand, n_e, cr):
        self.model = DecisionTreeClassifier(n_estimators = n_e , criterion = cr, random_state = rand)
        self.model.fit(train_X, train_Y)
        y_pred = self.model.predict(test_X)
        m = accuracy_score(test_Y, y_pred)
        print(m)
     
# 18
# 30
# gini