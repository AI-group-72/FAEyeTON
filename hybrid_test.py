import pandas as pd
from EyeTrackFatigue.Evaluate.HybridEval import HybridEval

def data_preprocessing(path):
    file_name = path 
    #считывание и подготовка данных
    data_list = pd.read_csv(file_name, delimiter=';')
    data_list = data_list.sample(frac=1)
    data_eval = data_list.pop('AU_cat')
    data_list.drop(columns=['File'], inplace=True) #, 'fatigue', 'Concen', 'Имя файла', 'Метод определения', 'деятельность', 'время суток'], inplace=True)
    data_list.dropna()
    #data_list.drop(columns=['duration_blink_mean', 'duration_blink_min', 'duration_blink_max', 'duration_fixation_mean', 'duration_fixation_min', 'duration_fixation_max', 'x_fixation_mean', 'x_fixation_min'], inplace=True)
    #data_list.drop(columns=['x_fixation_max', 'y_fixation_mean', 'y_fixation_min', 'y_fixation_max', 'azimuth_fixation_mean', 'azimuth_fixation_min', 'azimuth_fixation_max', 'elevation_fixation_max', 'elevation_fixation_min', 'elevation_fixation_mean'], inplace=True)
    data_list = (data_list - data_list.mean())/data_list.std() # normalization
    data_list = pd.concat([data_list, data_eval], axis=1)
    # разбиение выборок
    edu_list = data_list.sample(n=int(0.8*len(data_list)))
    eval_list = pd.concat([data_list, edu_list]).drop_duplicates(keep=False)
    train_Y = edu_list['AU_cat']
    train_X = edu_list.drop(columns=['AU_cat'])
    test_Y = eval_list['AU_cat']
    test_X = eval_list.drop(columns=['AU_cat'])
    # сохранение данных
    train_X.to_csv('TestData/train_X.csv', sep=';', index=False)
    train_Y.to_csv('TestData/train_Y.csv', sep=';', index=False)
    test_X.to_csv('TestData/test_X.csv', sep=';', index=False)
    test_Y.to_csv('TestData/test_Y.csv', sep=';', index=False)

# вызов подготовки данных - разделение заранее посчитанных данных на обучающую и контрольную выборку
#data_preprocessing('D:\\PythonProjects\\EyeTrackFatigue\\e.csv')
# загрузка данных
train_X = pd.read_csv('TestData/train_X.csv', sep=';')
train_Y = pd.read_csv('TestData/train_Y.csv', sep=';')
test_X = pd.read_csv('TestData/test_X.csv', sep=';')
test_Y = pd.read_csv('TestData/test_Y.csv', sep=';')


'''
# выбор набора используемых характеристик
std = ['x_mean', 'y_mean', 'Average Curve', 'Min Curve', 'Min Saccade Time', 'Average Fixation Speed', "% of Fixations < 150 ms, per minute", 'Average Fixation Speed, < 150ms']
train_X = train_X[std]
test_X = test_X[std]
'''
model = HybridEval()

# обучение моделей (с сохранением)
# model.edu(train_X, train_Y, test_X, test_Y, ['Basic', 'MLP', 'RFC', 'DCT']) # 'MLP', 'RFC', 'DCT'
# загрузка уже обученных моделей
model.load(['Basic', 'MLP', 'RFC', 'DCT' ]) # 'MLP', 'RFC', 'DCT'

# оценка точности моделей
print(model.eval(test_X, test_Y))
# оценка данных
# data_eval = pd.DataFrame({'Eval' : model.evaluate(data_list)})
# data_eval.to_csv('mm_eval.csv', sep=';', index=False)

#data_files = pd.concat([data_files, data_eval], axis=1)
#data_files.to_csv('mm_eval.csv', sep=';', index=False)