import pandas as pd
import joblib
from EyeTrackFatigue.Evaluate.MLPEval import MLPEval
from EyeTrackFatigue.Evaluate.RandomForestEval import RandomForestEval
from sklearn.metrics import accuracy_score


file_name = 'TestData//all_au.csv' # путь к файлу с данными
data_list = pd.read_csv(file_name, delimiter=';')
data_list = data_list.sample(frac=1) # перемешивание данных
data_eval = data_list.pop('AU_cat') # выделение оценки утомления
data_list.drop(columns=['File'], inplace=True) # сброс лишней информации
data_list.dropna() # выброс
# выбор набора используемых характеристик
'''
std = ['x_mean', 'y_mean', 'Average Curve', 'Min Curve', 'Min Saccade Time', 'Average Fixation Speed', "% of Fixations < 150 ms, per minute", 'Average Fixation Speed, < 150ms']
data_list = data_list[std]
'''
data_list = (data_list - data_list.mean())/data_list.std() # нормализация
data_list = pd.concat([data_list, data_eval], axis=1)


data_Y = data_list['AU_cat'].dropna()
data_X = data_list.drop(columns=['AU_cat']).dropna()
model = RandomForestEval() # выбор модели
model.cross_edu(data_X, data_Y)

print(model.acc)
print(model.f1)
print(model.cross_f1)
print(model.cross_acc)

joblib.dump(model, 'test_model.sav')
