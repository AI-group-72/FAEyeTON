import csv
import random
path = 'ann.csv'
reader = csv.reader(open(path, newline=''), delimiter=';')
#first_line = reader.__next__()
#print(first_line)
matrix = []
for row in reader:
    t_row = [row[0], row[2:]]
    matrix.append(t_row)#.__getitem__(2))

matrix = matrix[1:]

matrix1 = matrix.copy()
random.shuffle(matrix1) # перемешаем данные
print(matrix) # входные данные
print(matrix1)
q = 0
for i in range(len(matrix)):
    if matrix[i][0] == matrix1[i][0]:
        q += 1

print(q / len(matrix1))
