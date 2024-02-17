import csv
import random

# Константы:
GEN = 20 # количество поколений
Ch_Count = 10000 # количество потомков
delta = 2.0 # максимально отклонение веса одного признака в одном поколении
X_Number = 9 # количество признаков

# обычная регрессия,
class Func:
    def __init__(self, basis_weights=None, weights_delta=None):
        self.weights = []
        if basis_weights is None:
            self.weights = [2028, 2529, -1166, 335, -2335, -2411, -2322, -1576, -2391] # по корреляции

            '''
            for i in range(0, 9):  # у нас 9 признаков, заведём 9 весов
                self.weights.append(1.0)  # стартовые значения весов
            '''
        else:
            for weight in basis_weights:
                self.weights.append(weight * (random.random() - 0.5) * 2 * weights_delta)

    def calc(self, xs):
        value = 0
        for i in range(len(self.weights)):
            value += self.weights[i] * float(xs[i].replace(',', '.'))
        return value

    def __str__(self):
        return 'F:' + self.weights.__str__()
'''

def eval_func(func, work_list, _print=False):
    eval_list = []
    control_list = []
    for i in range(len(work_list)):
        eval_list.append([work_list[i][0], random.randint(1, 4)]) # func.calc(work_list[i][1][:9])
        control_list.append([work_list[i][0], float(work_list[i][1][-2].replace(',', '.'))])
    eval_list = sorted(eval_list, key=lambda x: x[-1])
    control_list = sorted(control_list, key=lambda x: x[-1])
    if _print:
        print('pre Q')
        print(eval_list)
        print(control_list)
    for i in range(len(eval_list)):
        eval_list[i].append(i * 4 // len(eval_list) + 1)
        control_list[i].append(i * 4 // len(eval_list) + 1)
    q = 0
    eval_list = sorted(eval_list, key=lambda x: x[0])
    control_list = sorted(control_list, key=lambda x: x[0])

    if _print:
        print('post Q')
        print(eval_list)
        print(control_list)

    for i in range(len(eval_list)):
        if control_list[i][-1] == eval_list[i][-1]:
            q += 1
    return q / len(eval_list)

'''
def eval_func(func, work_list):
    control_list = sorted(work_list, key=lambda x: float(x[1][9].replace(',', '.')))
    eval_list = work_list.copy()
    for i in range(len(eval_list)):
        eval_list[i].append(func.calc(eval_list[i][1][:9]))
    eval_list = sorted(eval_list, key=lambda x: x[-1])
    q = 0
    for i in range(len(eval_list)):
        if control_list[i][0] == eval_list[i][0]:
            q += 1
    return q / len(eval_list)


path = 'ann.csv'
reader = csv.reader(open(path, newline=''), delimiter=';')
#first_line = reader.__next__()
#print(first_line)
matrix = []
for row in reader:
    t_row = [row[0], row[2:]]
    matrix.append(t_row)#.__getitem__(2))

matrix = matrix[1:]
print(matrix) # входные данные
random.shuffle(matrix) # перемешаем данные

start = Func()
best = start
best_dist = eval_func(start, matrix[:len(matrix) * 8 // 10])
print(start, ' : ', best_dist)
I = 0
# for gen in range(0, GEN):      # фиксированное количество поколений
while best_dist < 0.8:           # считать, пока дистанция не сократится
    for ch_i in range(0, Ch_Count):
        child = Func(start.weights, delta)
        ch_dist = eval_func(child, matrix[:len(matrix) * 8 // 10]) # обучаем на 80% данных
        if ch_dist > best_dist:
            best_dist = ch_dist
            best = child
    if start == best:
        I += 1
        delta *= delta
        if I >= 15:
            start = Func()
            best = start
            best_dist = eval_func(start, matrix[:len(matrix) * 8 // 10])
            print('Reset')
            I = 0
            delta = 2.0
    else:
        I = 0
        start = best
        print(start, ' : ', best_dist)

print(best_dist)
print(eval_func(best, matrix[len(matrix) * 8 // 10+1:], True)) # контроль на 20% данных

for row in matrix:
    row.append(str(best.calc(row[1][:9])))

print(eval_func(best, matrix))

#print(our_list)

# F:[2028, 2529, -1166, 335, -2335, -2411, -2322, -1576, -2391]  :  0.3877551020408163
# F:[9516.496548884677, -1481.7470158300598, -24799.939347375548, -496.0585053880757, -8.202418612181155, -1827.531572733274, 2215.4052451615994, -35430.470695843134, 4732.063298066532]  :  0.6122448979591837