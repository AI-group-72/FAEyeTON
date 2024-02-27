import datetime
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import (
    accuracy_score,
    f1_score
)

from ..Evaluate.Evaluator import Evaluator
# модель оценки "случайный лес"
class RandomForestEval(Evaluator):
    def __init__(self):
        self.model = None
        self.acc = -1
        self.f1 = -1
    
    def get_name(self):
        return 'RFC'
    
    def evaluate(self, data):
        if self.model == None:
            print('Not educated yet')
        else:
            return self.model.predict(data)

    def redu(self, train_X, train_Y, test_X, test_Y): # переобучение на новых данных со старыми параметрами
        self.model.fit(train_X, train_Y)
        y_pred = self.model.predict(test_X)
        self.acc = accuracy_score(test_Y, y_pred)
        self.f1 = f1_score(test_Y, y_pred)   

    def edu(self, train_X, train_Y, test_X, test_Y): # обучение на новых данных
        err = 0
        rand = -1
        c = ['gini', 'entropy', 'log_loss']  # набор используемых критериев
        n = [10, 20, 30, 40, 50, 60, 70, 80, 90, 100]  # набор количества "деревьев" в "лесу"
        now = datetime.datetime.now() 
        print(now) # замер времени
        for i in range(5): # перебор случайных состояний
            print(i)
            for N in n: # перебор вариантов количества
                for C in c: # перебор критериев
                    model = RandomForestClassifier(n_estimators = N , criterion = C, random_state = i)
                    model.fit(train_X, train_Y)
                    y_pred = model.predict(test_X)
                    f = f1_score(test_Y, y_pred)
                    if f > err: # выбор лучших параметров (по показателю Ф-меры)
                        print(f)
                        rand = i
                        err = f
                        n_e = N
                        cr = C
        now = datetime.datetime.now() - now
        print(now) # вывод времени
        print(rand)
        print(n_e)
        print (cr)
        # переобучение по лучшим выявленным параметрам
        self.model = RandomForestClassifier(n_estimators = n_e , criterion = cr, random_state = rand)
        self.model.fit(train_X, train_Y)
        y_pred = model.predict(test_X)
        f = f1_score(test_Y, y_pred)
        print(f)

    def cross_edu(self, data_X, data_Y): # обучение на новых данных с использованием кроссвалидации
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
        rand = -1
        c = ['gini', 'entropy', 'log_loss']
        n = [10, 20, 30, 40, 50, 60, 70, 80, 90, 100]
        err = 0
        for i in range(1):  # перебор случайных состояний / iterating through random states
            print(i)
            for N in n:  # Перебор параметров / Iterating through the parameters
                for C in c:  # Перебор параметров / Iterating through the parameters
                    model = RandomForestClassifier(n_estimators = N , criterion = C, random_state = i)
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
                        f += _f
                        acc += accuracy_score(test_Y, y_pred)
                    f = f / 5
                    acc = acc / 5
                    if f > err: # Сравнение текущей модели с лучшей / Comparing the current model with the best one
                        # Cохранение параметров и показателей / Saving parameters and indicators
                        print(f)
                        rand = i
                        err = f
                        n_e = N
                        cr = C
                        cross_acc = acc
        print(rand)
        print(cr)
        print(n_e)

        now = datetime.datetime.now()
        print(now)
        # Время окончания обучения / Training end timestamp 
        print('Total time:', now - now1)
        test_X = teX[cross]
        test_Y = teY[cross]
        train_X = trX[cross]
        train_Y = trY[cross]
        # обучение модели по параметрам лучший / training the model according to the best parameters
        self.model = RandomForestClassifier(n_estimators = n_e, criterion = cr, random_state = rand)
        self.model.fit(train_X, train_Y)
        y_pred = self.model.predict(test_X)
        self.f1 = f1_score(test_Y, y_pred) # результаты по одному из разбиений / results for one sample
        self.acc = accuracy_score(test_Y, y_pred)  
        self.cross_f1 = err # усреднённые результаты по всем разбиениям / averaged results for all samples
        self.cross_acc = cross_acc

    def edu_args(self, train_X, train_Y, test_X, test_Y, rand, n_e, cr):
        self.model = RandomForestClassifier(n_estimators = n_e , criterion = cr, random_state = rand)
        self.model.fit(train_X, train_Y)
        y_pred = self.model.predict(test_X)
        f = f1_score(test_Y, y_pred)
        print(f)
        
