import pandas as pd
import joblib
from Evaluate.MLPEval import MLPEval
from Evaluate.RandomForestEval import RandomForestEval
from sklearn.metrics import accuracy_score

#model.predict()

extra = ['File', 'fatigue', 'False Fixation, per minute', 'False Saccades, per minute', 'Saccades with amplitude > 6 degrees, per minute',
        'Saccades with amplitude < 6 degrees, per minute', 'Max Curve', 'Average Curve', 'Min Curve', 'Time Frame',
        'Saccades time', 'Fixation time < 150 ms', 'Fixation time > 150 ms', 'Fixation time between 150 and 900 ms',
        'Fixation time > 900 ms', 'Fixation time < 180 ms', 'Fixation time > 180 ms', '% of Fixations < 150 ms',
        '% of Fixations > 150 ms', '% of Fixations between 150 and 900 ms', '% of Fixations > 900 ms',
        '% of Fixations < 180 ms', '% of Fixations > 180 ms', 'Fixation time < 150 ms, per time',
        'Fixation time > 150 ms, per time', 'Fixation time between 150 and 900 ms, per time', 'Fixation time > 900 ms, per time',
        'Fixation time < 180 ms, per time', 'Fixation time > 180 ms, per time', '% of Fixations < 150 ms, per minute',
        '% of Fixations > 150 ms, per minute', '% of Fixations between 150 and 900 ms, per minute', '% of Fixations > 900 ms, per minute',
        '% of Fixations < 180 ms, per minute', '% of Fixations > 180 ms, per minute', 'Fixation Frequency',
        'Average Fix Frequency in interval (1s)',
        'Max Fix Frequency in interval (1s)',
        'Average Acceleration',
        'Min Acceleration',
        'Max Acceleration',
        'Average Speed',
        'Min Speed',
        'Max Speed',
        'Average Acceleration in interval (1s)',
        'Min Acceleration in interval (1s)',
        'Max Acceleration in interval (1s)',
        'Average Speed in interval (1s)',
        'Min Speed in interval (1s)',
        'Max Speed in interval (1s)',
        'Average Fixation Speed',
        'Min Fixation Speed',
        'Max Fixation Speed',
        'Average Fixation Speed, < 150ms',
        'Min Fixation Speed, < 150ms',
        'Max Fixation Speed, < 150ms',
        'Average Fixation Speed, > 150ms',
        'Min Fixation Speed, > 150ms',
        'Max Fixation Speed, > 150ms',
        'Average Saccade Speed',
        'Min Saccade Speed',
        'Max Saccade Speed',
        'Average Saccade Length',
        'Min Saccade Length',
        'Max Saccade Length',
        'Average Saccade Time',
        'Min Saccade Time',
        'Max Saccade Time']

file_name = 'D:\\PythonProjects\\Faeyeton\\_Data//head_data_au.csv'
data_list = pd.read_csv(file_name, delimiter=';')
#data_list = pd.concat([data_list, pd.read_csv('D:\PythonProjects\Faeyeton\_Data/all_q.csv', delimiter=';')], axis=1)
data_list = data_list.sample(frac=1)
data_eval = data_list.pop('AU_cat')
#data_eval = pd.read_csv('D:\PythonProjects\Faeyeton\_Data/all_q.csv', delimiter=';')
data_list.drop(columns=['File'], inplace=True) #, 'fatigue', 'Concen', 'Имя файла', 'Метод определения', 'деятельность', 'время суток'], inplace=True)
data_list.dropna()
#data_list.drop(columns=['duration_blink_mean', 'duration_blink_min', 'duration_blink_max', 'duration_fixation_mean', 'duration_fixation_min', 'duration_fixation_max', 'x_fixation_mean', 'x_fixation_min'], inplace=True)
#data_list.drop(columns=['x_fixation_max', 'y_fixation_mean', 'y_fixation_min', 'y_fixation_max', 'azimuth_fixation_mean', 'azimuth_fixation_min', 'azimuth_fixation_max', 'elevation_fixation_max', 'elevation_fixation_min', 'elevation_fixation_mean'], inplace=True)
data_list = (data_list - data_list.mean())/data_list.std() # normalization
data_list = pd.concat([data_list, data_eval], axis=1)

'''
edu_list = data_list.sample(n=int(0.8*len(data_list)))
eval_list = pd.concat([data_list, edu_list]).drop_duplicates(keep=False)

train_Y = edu_list['Eval']
train_X = edu_list.drop(columns=['Eval'])

test_Y = eval_list['Eval']
test_X = eval_list.drop(columns=['Eval'])
'''
data_Y = data_list['AU_cat'].dropna()
data_X = data_list.drop(columns=['AU_cat']).dropna()
model = RandomForestEval()
model.cross_edu(data_X, data_Y)

print(model.acc)
print(model.f1)
print(model.cross_f1)
print(model.cross_acc)

joblib.dump(model, 'all_ssssssq_RFCcr.sav')

'''
4
entropy
80
Total time: 0:10:17.618459
max acc 0.8267716535433071
max f1  0.8690476190476191
cross acc 0.8023622047244094
cross f1  0.8483332037551342
'''
'''
RFC Q
0
logistic
adam
2024-01-28 00:38:29.510148
Total time: 0:33:30.719944
0.7125984251968503
0.7999999999999999
0.8291489708554971
0.7488188976377953
'''
"""
RFC Q 1.36
2
0
logistic
adam
2024-01-28 01:34:22.334544
Total time: 0:33:09.769249
0.6850393700787402
0.7837837837837839
0.7899238538241211
0.7070866141732284
"""

'''
19
4
tanh
adam
2024-01-27 23:55:57.588645
Total time: 0:30:55.286679
0.7440944881889764
0.8104956268221574
0.8409144947167058
0.7952755905511811
'''


'''
1
9
relu
adam
0.8288288288288288
0.8789808917197452
'''
'''
9
3
relu
adam
2024-01-15 23:10:33.915441
Total time: 2:09:54.054199
0.8108108108108109
0.8320000000000001
0.8190372136187941
0.8027027027027026

'''
'''
2
63
tanh
lbfgs
'''




'''
1
gini
50
2024-02-06 00:52:30.987094
Total time: 0:08:27.646933
0.7630522088353414
0.8206686930091186
0.8275103376805714
0.789558232931727
'''