# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

# Use a breakpoint in the code line below to debug your script.
# Press Ctrl+F8 to toggle the breakpoint.

# Press the green button in the gutter to run the script.

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
from array import *

import numpy as np


import math
import re
import cv2


#задает число знаков после запятой
def toFixed(numObj, digits=0):
    return f"{numObj:.{digits}f}"

name_of_all_files="22-08-29-paper-evening-sync"#одинаковое имя всех файлов, разница только в форматах и путях
gaze_positions_file_path="Gaze-positions/"+ name_of_all_files+".csv"#название файла с координатами направления взгляда
out_static_parameters_file_path=name_of_all_files+"-static-parameters.txt"#название файла куда выводятся статические параметры
ppi_file_path="PPI/"+name_of_all_files+".txt"#название файла откуда берём значения PPI
#ppi_file_path="PPI/no_ppi.txt"#название файла откуда берём значения PPI
out_all_videos_static_parameters_file_path="out_all_videos_static_parameters/out_all_videos_static_parameters.txt"#название файла куда выводим статические параметры со всех видео
out_name_of_video="fixations-saccades-videos/12-05-22-paper-morning-sync-gaze.avi"#название видео, которое получим на выходе
#пока что видео не обрабатываем, поэтому строчка ниже закомментирована
in_name_of_video="original-videos/22-05-30-paper-morning-sync.mp4"#название видео, которое обрабатываем

#f2 = open(gaze_positions_file_path,"r")
f3=open(out_static_parameters_file_path, "w")#выводим статические параметры в файл
f4=open(gaze_positions_file_path,"r")#для того, чтобы прочитать последнюю строчку
f5=open(out_all_videos_static_parameters_file_path, "a")#файл для вывода статических параметров со всех видео


#string = f2.readline()
#string = f2.readlines()[2:]
#string = re.findall(r'\d+[.]\d+|\d+', string[0])

#получаем вторую строку файла
with open(gaze_positions_file_path, 'r') as f2:
    for i in range(1):
        f2.readline()
    string = f2.readline()

string = re.findall(r'\d+[.]\d+|\d+', string)
string2=f4.readlines()[-1]#для того, чтобы прочитать последнюю строчку
string2= re.findall(r'\d+[.]\d+|\d+', string2)


start_time_plus_30=float(string[0])+30.0#временная метка старта плюс 30 секунд для подсчета статических параметров,
#без учета первых 30 секунд на которых могут быть некоррректные данные
end_time_minus_30=float(string2[0])-30.0#временная метка конца минус 30 секунд для подсчета статических параметров,
#без учета последних 30 секунд на которых могут быть некоррректные данные
#надо понять как прыгнуть на строку файла, содержащего временную метку start_time_plus_30.

#из lines-on-video
num_f1 = int(string[1])#текущий номер кадра
num_f2 = int(string[1])#следующий номер кадра

'''
#ВОЗМОЖНО ЗДЕСЬ ВСЕМУ МОЖНО ПРИСВОИТЬ ЗНАЧЕНИЕ НОЛЬ КАК P5!!!
p1=(int(float(string[3])*1088), int(1080-float(string[4])*1080))#x1 и y1 gaze_positions_2
p2=(int(float(string[3])*1088), int(1080-float(string[4])*1080))#x1 и y1 gaze_positions_2
p3=(int(float(string[3])*1088), int(1080-float(string[4])*1080))#x1 и y1 gaze_positions_2
p4=(int(float(string[3])*1088), int(1080-float(string[4])*1080))#x1 и y1 gaze_positions_2
p5=0#(int(float(string[3])*1088), int(1080-float(string[4])*1080))#x1 и y1 gaze_positions_2 отличные значения для мин, макс и средней скорости
p6=(int(float(string[3])*1088), int(1080-float(string[4])*1080))#x1 и y1 gaze_positions_2 отличные значения для мин, макс и средней скорости

p_circle1=(int(float(string[3])*1088), int(1080-float(string[4])*1080))#радиусы рисуемых кругов (фиксакций)
p_circle2=(int(float(string[3])*1088), int(1080-float(string[4])*1080))
p_circle3=(int(float(string[3])*1088), int(1080-float(string[4])*1080))
'''
#ВОЗМОЖНО ЗДЕСЬ ВСЕМУ МОЖНО ПРИСВОИТЬ ЗНАЧЕНИЕ НОЛЬ КАК P5!!!
p1=(0,0)#0#(int(float(string[3])*1088), int(1080-float(string[4])*1080))#x1 и y1 gaze_positions_2
p2=(0,0)#0#(int(float(string[3])*1088), int(1080-float(string[4])*1080))#x1 и y1 gaze_positions_2
p3=0#(int(float(string[3])*1088), int(1080-float(string[4])*1080))#x1 и y1 gaze_positions_2
p4=0#(int(float(string[3])*1088), int(1080-float(string[4])*1080))#x1 и y1 gaze_positions_2
p5=0#(int(float(string[3])*1088), int(1080-float(string[4])*1080))#x1 и y1 gaze_positions_2 отличные значения для мин, макс и средней скорости
p6=0#(int(float(string[3])*1088), int(1080-float(string[4])*1080))#x1 и y1 gaze_positions_2 отличные значения для мин, макс и средней скорости

p_circle1=(0,0)#0#(int(float(string[3])*1088), int(1080-float(string[4])*1080))#радиусы рисуемых кругов (фиксакций)
p_circle2=(0,0)#0#(int(float(string[3])*1088), int(1080-float(string[4])*1080))
p_circle3=(0,0)#0#(int(float(string[3])*1088), int(1080-float(string[4])*1080))
radius=100#радиус рисуемых кругов (фиксакций), подходят:80,70,60,50,40,30
distance2=0#пройденная дистанция от центра круга (фиксации)
saccade=18#если дистаниция больше этого значения, то определяется саккада
sac_per_time=0#сумма длин саккад за время (1 секунда)
sac_new=0#новая длина саккады
per_time_sac=1#через сколько секунд выводить среднюю длину саккады
sac_all=0#суммируем все саккады
sac_counter1=0#счетчик саккад
sac_counter2=0#счетчик саккад
sac_average=0#средняя длина саккады
sac_all_average=0#средняя длина саккады за всё видео
circle_counter=0#счётчик нарисованых кругов (фиксаций)
flag1=0#определяет какого цвета будет нарисован круг (фиксакция)
cur_circle=(int(float(string[3])*1088), int(1080-float(string[4])*1080))#центр последнего нарисованного круга (фиксации)
list_saccade=[]# список длин саккад distance1
length_list_saccade = 0# длина списка саккад distance1
list_saccade_cut = 0  # какое число минимальных и максимальных значений длин саккад удалить

#для синхронизированных видео это не используем
#f_f_number=int(string[1])#номер первого кадра
#f_counter=0#Счётчик кадров



#из gaze_directory
x = 0
y = 0

#из speed_calc
real_time=0.0
real_time2=0.0#отличные значения для мин, макс и средней скорости
distance1=0

'''
time_line=float(string[0])+0.5#временная граница до которой складываем траектории, начальное значение зависит от файла с координатами gaze_positions_file_path (используется для рассчета)
time_line2=float(string[0])+0.5#временная граница, которую сравниваем со временем на видео для вывода скорости раз в 0.5 сек (используется для вывода скороти)
time_line3=float(string[0])+1.0#используется для рассчета скорости за 1 секунду все видео
time_line4=float(string[0])+0.5#временная граница, которую сравниваем со временем на видео для вывода длины саккады раз в 1 сек
time_line5=float(string[0])+0.5#временная граница, которую используем для вывода средней длины саккады раз в 1 сек
time_line6=float(string[0])+60.0#временная граница, которую сравниваем со временем на видео для вывода средней скорости раз в 60 сек
time_line7=float(string[0])+60.0#временная граница, которую используем для вывода средней скорости раз в 60 сек
time_line8=float(string[0])+10.0#временная граница, которую сравниваем со временем на видео для вывода средней частоты рисования круга раз в 10 сек
time_line9=float(string[0])+10.0#временная граница, которую используем для вывода средней частоты рисования нового круга раз в 10 сек
time_line10=float(string[0])+1.0#временная граница до которой складываем траектории. Используется для вычисления скорости за 1 секунду и затем рассчета усорения за 1 секунду
time_line11=float(string[0])+4.0#временная граница до которой складываем траектории для вычисления обобщённой кривизны траекторий
time_line12=float(string[0])+1.0#временная граница для вычисления минимальной и максимальной частоты появления новой области фиксации за 1 секунду
time_line13=float(string[0])+10.0#временная граница для вычисления минимальной и максимальной частоты появления новой области фиксации раз в 10 сек
'''

time_line=start_time_plus_30+0.5#временная граница до которой складываем траектории, начальное значение зависит от файла с координатами gaze_positions_file_path (используется для рассчета)
time_line2=start_time_plus_30+0.5#временная граница, которую сравниваем со временем на видео для вывода скорости раз в 0.5 сек (используется для вывода скороти)
time_line3=start_time_plus_30+1.0#используется для рассчета скорости за 1 секунду все видео
time_line4=start_time_plus_30+0.5#временная граница, которую сравниваем со временем на видео для вывода длины саккады раз в 1 сек
time_line5=start_time_plus_30+0.5#временная граница, которую используем для вывода средней длины саккады раз в 1 сек
time_line6=start_time_plus_30+60.0#временная граница, которую сравниваем со временем на видео для вывода средней скорости раз в 60 сек
time_line7=start_time_plus_30+60.0#временная граница, которую используем для вывода средней скорости раз в 60 сек
time_line8=start_time_plus_30+10.0#временная граница, которую сравниваем со временем на видео для вывода средней частоты рисования круга раз в 10 сек
time_line9=start_time_plus_30+10.0#временная граница, которую используем для вывода средней частоты рисования нового круга раз в 10 сек
time_line10=start_time_plus_30+1.0#временная граница до которой складываем траектории. Используется для вычисления скорости за 1 секунду и затем рассчета усорения за 1 секунду
time_line11=start_time_plus_30+4.0#временная граница до которой складываем траектории для вычисления обобщённой кривизны траекторий
time_line12=start_time_plus_30+1.0#временная граница для вычисления минимальной и максимальной частоты появления новой области фиксации за 1 секунду
time_line13=start_time_plus_30+10.0#временная граница для вычисления минимальной и максимальной частоты появления новой области фиксации раз в 10 сек
time_line14=start_time_plus_30+1#используется для рассчета скорости за 1 секунду внутри области фиксации
time_line15=start_time_plus_30+1#используется для рассчета скорости саккады за 1 секунду

#СКОРОСТЬ ЗА 0,5 СЕКУНДЫ ДЛЯ ВЫВОДА НА ВИДЕО
per_time=0.5#временной промежуток за который вычисляем скорость
speed=0.0
new_speed=0.0#скорость, которую выводим через каждые 0.5 секунды (после сравнения времени на видео real_time и time_line)
dist_per_time=0

#какой процент минимальных и максимальных значений удалить
proc=10#какой процент минимальных и максимальных значений удалить

#СРЕДНЯЯ МИНИМАЛЬНАЯ И МАКСИМАЛЬНАЯ СКОРОСТЬ ЗА 1 СЕКУНДУ
dist_per_time4=0
speed4=0#начение скорости
per_time8=1.0#временной промежуток за который вычисляем скорость
average_speed=0.0
min_speed=0
max_speed=0
init_min=0
min_speed_flag=0
speed4_zero_counter=0#счётчик нулевых значение speed4
buf_time = 0 #буфер для суммирования времени за которое суммировались расстояния
time_per_distance =0 # время за которое суммировались расстояния. Это время <= per_time8=1 секунда
all_distance=0  # считает всё пройденное расстояние
all_time=0#считает всё время
list_speed=[]#список скоростей speed4
list_distance=[]#список всей дистанции
list_time=[]# список всего времени
length_list_distance=0#число элементов в списке list_distance
length_list_time=0#число элементов в списке list_time
length_list_speed=0#число элементов в списке list_speed
list_distance_cut=0#какой число минимальных и максимальных значений дистанции удалить
list_time_cut=0#какое число минимальных и максимальных значений времени удалить
list_speed_cut=0#какое число минимальных и максимальных значений скорости удалить


#МАКСИМАЛЬНАЯ И МИНИМАЛЬНАЯ ДЛИНА САККАДЫ
min_sac=0
max_sac=0#максимальная длина саккады
init_min4=0

#переменные для вычисления и вывода средней скорости за 1 минуту
per_time2=60.0#временной промежуток за который вычисляем скорость
speed2=0.0
new_speed2=0.0#скорость, которую выводим через каждые 60 секунд (после сравнения времени на видео real_time и time_line)
dist_per_time2=0

#переменные для вычисления частоты появления всех новых областей фиксации



#переменные для вычисления СРЕДНЕЙ МИНИМАЛЬНОЙ И МАКСИМАЛЬНОЙ частоты появления новых областей фиксации за 1 секунду
per_time6=1.0#Временной промежуток для вычисления частоты появления новых областей фиксации
fixation_counter3=0#счётчик среднего числа новых областей фиксации (за 1 секунду)
fixation_counter4=0#счётчик для вычисления минимального и максимального числа новых областей фиксации (за 1 секунду)
time_period_1_counter=0#счётчик 1-секундных интервалов
init_min5=0
fix_freq_1=0#Средняя частота рисования нового круга за 1 секунду
fix_freq_1_min=0#минимальная частота рисования нового круга за 1 секунду
fix_freq_1_max=0#максимальная частота рисования нового круга за 1 секунду
fixation_counter4_zero_counter=0  # счётчик нулевых значений fixation_counter4
start_fixation_point_1=0#координаты центра области фиксчации
distance_to_new_fixation=0#расстояние от центра области фиксации
list_fix_freq_1=[]# список числа новых областей фиксации за 1 секунду
length_list_fix_freq_1 = 0# длина списка числа новых областей фиксации за 1 секунду
list_fix_freq_1_cut = 0  # какое число минимальных и максимальных значений числа новых областей фиксации за 1 секунду удалить


#переменные для вычисления СРЕДНЕЙ МИНИМАЛЬНОЙ И МАКСИМАЛЬНОЙ частоты появления новых областей фиксации за 10 секунду
per_time7=10.0
fixation_counter5=0#считает фиксации за всё видео (за 10 секунду)
fixation_counter6=0#считает фиксации за 10-секундные интервалы
time_period_10_counter=0#счётчик 10-секундных интервалов
init_min6=0
fix_freq_10=0#Средняя частота рисования нового круга за 10 секунду
fix_freq_10_min=0#минимальная частота рисования нового круга за 10 секунду
fix_freq_10_max=0#максимальная частота рисования нового круга за 10 секунду
fixation_counter6_zero_counter =0  # счётчик нулевых значений fixation_counter6
start_fixation_point_10=0#координаты центра области фиксчации
list_fix_freq_10=[]  # список числа новых областей фиксации за 10 секунд
length_list_fix_freq_10 = 0# длина списка числа новых областей фиксации за 10 секунд
list_fix_freq_10_cut = 0# какое число минимальных и максимальных значений числа новых областей фиксации за 10 секунд удалить



#переменные для вычисления числа новых областей фиксации за 10 секунд и вывода на видео
fixation_counter1=0#счетчик числа новых областей фиксации за 10 секунд
fixation_counter2=0#
fixation_frequency_per_10=0#Средняя частота рисования нового круга за 10 сек
per_time3=10.0#временной промежуток за который считаем чило новых кругов


#переменные для вычисления числа фиксаций короче 80 мс и продолжительнее 1000 мс
fix_time1=0.0
fix_time2=0.0
fix_time=0.0
fix_shorter_80=0
fix_longer_1000=0
flag2=0

#переменные для вычисления средней скорости внутри области фиксации
all_distance_in_fix=0#считает расстояние внутри всех фиксации
distance_in_fix=0#считает расстояние внутри одной фиксации
all_time_in_fix=0.0#считает время внутри всех фиксации за все видео
time_in_fix=0.0#считает время внутри одной фиксации
buf_time_in_fix=0.0#время одного перемещения внутри фиксации
average_speed_in_fix=0.0
speed_in_fix=0#скорость внутри области фиксации
per_time9=1#временной промежуток за который вычисляем скорость внутри области фиксации
fix_flag=0#показывает, что произошла область фиксации и посчитана дистанция внутри области фиксации
list_all_distance_in_fix=[]#список всех длин дистанций внутри области фиксации
list_all_time_in_fix=[]#список всех времен внутри области фиксации
list_speed_in_fix=[]#список всех скоростей внутри области фиксации
length_list_all_distance_in_fix=0#длина списка всех длин дистанций внутри области фиксации
list_all_distance_in_fix_cut=0#какое число минимальных и максимальных значений дистанции удалить
length_list_all_time_in_fix=0#длина списка всех времен внутри области фиксации
list_all_time_in_fix_cut=0#какое число минимальных и максимальных значений времени внутри области фиксации удалить
length_list_speed_in_fix=0#длина списка всех скоростей внутри области фиксации
list_speed_in_fix_cut=0#какое число минимальных и максимальных значений скорости внутри области фиксации удалить

#переменные для вычисления средней скорости саккады
all_distance_in_sac=0#считает расстояние всех саккад
distance_in_sac=0
all_time_in_sac=0.0#считает время всех саккад за все видео
time_in_sac=0.0
average_time_in_sac=0.0
buf_time_in_sac=0.0
average_speed_in_sac=0.0
speed_in_sac=0#скорость вне области фиксации
per_time10=1#временной промежуток за который вычисляем скорость саккады
sac_flag=0#показывает, что произошла саккада и посчитана дистанция внутри саккады
list_all_distance_in_sac=[]# список всех длин дистанций внутри саккады
list_all_time_in_sac=[]# список всех времен внутри саккады
list_speed_in_sac=[]# список всех скоростей внутри саккады
length_list_all_distance_in_sac=0#длина списка всех длин дистанций  саккады
list_all_distance_in_sac_cut=0#какое число минимальных и максимальных значений дистанции саккады удалить
length_list_all_time_in_sac=0#длина списка всех времен саккады
list_all_time_in_sac_cut=0#какое число минимальных и максимальных значений времени саккады удалить
length_list_speed_in_sac=0#длина списка всех скоростей саккады
list_speed_in_sac_cut=0#какое число минимальных и максимальных значений скорости саккады удалить

#минимальная и максимальная скорость внутри области фиксации
init_min7=0
min_speed_in_fix=0
max_speed_in_fix=0
speed_in_fix_zero_counter =0  # счётчик нулевых значений speed_in_fix

#минимальная и максимальная скорость саккады
init_min8=0
min_speed_in_sac=0
max_speed_in_sac=0
speed_in_sac_zero_counter=0# счётчик нулевых значений speed_in_sac


#ПРЕДЫДУЩАЯ ВРЕМЕННАЯ МЕТКА
previous_time_stamp=0.0


#максимальная мгновенная скорость
time_max_velocity=0.0
max_velocity=0
new_max_velocity=0#значение для проверки обновилось ли максимальное значение мгновенной скорости
list_velocity=[]# список всех мгновенных скоростей
length_list_velocity=0#длина списка мгновенных скоростей
list_velocity_cut=0#какое число минимальных и максимальных значений значений мгновенной скорости удалить

debug_counter=0
debug_counter2=0

#модуль ускорения за одну секунду
per_time4=1.0#временной промежуток за который вычисляем скорость и ускорение
speed3=0.0
end_speed=0.0#скорость, которую выводим через каждые 0.5 секунды (после сравнения времени на видео real_time и time_line)
start_speed=0.0
dist_per_time3=0
acceleration=0.0#модуль ускорения за 1 секунду
new_acceleration=0.0#ускорение, которое выводим через каждую 1 секунд (после сравнения времени на видео real_time и time_line10)

#параметры для вычисления среднего модуля ускорения за всё видео
end_speed2 = 0.0
acceleration2 = 0.0
start_speed2 = 0.0
acc_counter=0# количество всех ускорений
average_acc=0.0
all_acc=0.0# сумма всех ускорений
#мин и макс значения ускорения
acc_min=0.0
acc_max=0.0
init_min3=0
acceleration2_zero_counter =0#счётчик нулевых значений acceleration2
list_acceleration=[]# список ускорений acceleration2
length_list_acceleration=0#длина списка с ускорениями
list_acceleration_cut=0#какое число минимальных и максимальных значений ускорения удалить



#параметры для вычисления кривизны
per_time5=4.0#временной промежуток за который вычисляем кривизну
length_of_path=0
p_start=(int(float(string[3])*1088), int(1080-float(string[4])*1080))#координата стартовой точки пути
p_end=(int(float(string[3])*1088), int(1080-float(string[4])*1080))#координата конечной точки пути
distance_of_path=0
curvature=0.0
curvature_sum=0.0
curvature_aver=0.0
curvature_counter=0
list_curvature=[]#список значений кривизны траекторий

#мин и макс значения кривизны
min_curvature=0.0
max_curvature=0.0
init_min2=0
curvature_zero_counter=0  # счётчик нулевых значений curvature

#СКОРОСТЬ САККАДЫ К ДЛИНЕ САККАДЫ (СРЕДНЕЕ, МИНИМУМ, МАКСИМУМ)
length_sac=0#длина саккады
time_sac =0.0#время конца саккады
speed_sac =0.0#мгновенная скорость саккады
speed_to_length=0.0#мгновенная скорость саккады
speed_to_length_sum=0.0#сумма мгновенных скоростей саккад
speed_to_length_counter=0#счетчик числа speed_to_length
average_speed_to_length=0.0# среднее значение скорости саккады к длине саккады
init_min9=0
min_speed_to_length =0.0#минимальная скорость саккады к длине саккады
max_speed_to_length=0.0#максимальная скорость саккады к длине саккады
speed_to_length_zero_counter=0  # счётчик нулевых значений speed_to_length
list_speed_to_length=[]#список значений средней скорости саккады к длине саккады
length_list_speed_to_length=0#длина списка значений средней скорости саккады к длине саккады
list_speed_to_length_cut=0#какое число минимальных и максимальных значений средней скорости саккады к длине саккады удалить

#СРЕДНИЙ, МИНИМАЛЬНЫЙ, МАКСИМАЛЬНЫЙ PPI
ppi=0#значение ppi
ppi_sum=0#сумма всех ppi
ppi_counter=0#счетчик ppi
ppi_average=0#среднее значение ppi
ppi_min=0#минимальное значение ppi
ppi_max=0#максимальное значение ppi
init_min10=0
ppi_zero_counter =0# счётчик нулевых значений ppi
list_ppi=[]#список значений ppi
length_list_ppi=0#длина списка значений PPI
list_ppi_cut=0#какое число минимальных и максимальных значений PPI удалить


#РАСПРЕДЕЛЕНИЕ ТОЧЕК ФИКСАЦИИ
sac_amplitude=42#амплитуда саккады равная 6 угловым градусам
more_6_FOV_counter=0#счётчик саккад больше 6 угловых градусов
less_6_FOV_counter=0##счётчик саккад меньше 6 угловых градусов
time_of_fix_line=0.18#время фиксации равное 180 мс
buf_time_of_fix = 0#буфер подсчёта времени между двумя соседними фиксациями
time_of_fix = 0#время одной фиксации
more_180_ms_counter=0#счётчик фиксаций больше 180 мс
less_180_ms_counter=0#счётчик фиксаций меньше 180 мс
first_fix_coordinate = 0  # координаты первой точки фиксации
distance_from_first_fix =0# вычисляем расстояние от точки первой фиксации
flag3=0#флаг инициализации first_fix_coordinate, distance_from_first_fix, time_of_fix


#f2.close()
f4.close()

#пока что видео не обрабатываем, поэтому строчка ниже закомментирована
cap = cv2.VideoCapture(in_name_of_video)

#пока что видео не обрабатываем, поэтому строчка ниже закомментирована
if (cap.isOpened() == False):
    print("Ошибка открытия видеофайла")


f1 = open(gaze_positions_file_path)
#f2 = open("gaze_positions_file_path-15-42.csv")

#пока что видео не обрабатываем, поэтому строчка ниже закомментирована
frame_width = int(cap.get(3))
frame_height = int(cap.get(4))

#пока что видео не обрабатываем, поэтому строчка ниже закомментирована
out = cv2.VideoWriter(out_name_of_video, cv2.VideoWriter_fourcc('M', 'J', 'P', 'G'), 30, (frame_width, frame_height))

with open(gaze_positions_file_path, "r") as f:
    for string in f.readlines()[1:]:#читает со второй строки

        string = re.findall(r'\d+[.]\d+|\d+', string)
        real_time2 = float(string[0])
        if (real_time2>start_time_plus_30) and (real_time2<end_time_minus_30):

            p6=(int(float(string[3])*1088), int(1080-float(string[4])*1080))#x2 и y2


            if (previous_time_stamp != 0) and (p5!=0):  # проверяем получил ли предыдущее значение времени previous_time_stamp
                # и координаты предыдущей точки p5
                distance1 = int(math.hypot(p6[0] - p5[0], p6[1] - p5[1]))  # вычисляем длину вектора (траекторию движения взгляда)


                if (distance_to_new_fixation==0)or(distance_to_new_fixation>saccade):
                    start_fixation_point_1 = p5#координаты центра области фиксации
                distance_to_new_fixation = int(math.hypot(p6[0] - start_fixation_point_1[0], p6[1] -start_fixation_point_1[1]))  # вычисляем длину вектора от центра области фиксации


                #СРЕДНЯЯ СКОРОСТЬ В СЕКУНДУ
                # если real_time2<time_line3, то  dist_per_time4+=distance1
                # иначе speed4=dist_per_time4/time_line3
                # выводим speed4
                if float(real_time2) < time_line3:
                    dist_per_time4 += distance1
                    buf_time = float(real_time2)
                    buf_time = buf_time - previous_time_stamp  # время одного расстояния
                    time_per_distance += buf_time  # время за которое суммировались расстояния. Это время <= per_time8=1 секунда
                else:
                    speed4 = dist_per_time4 / time_per_distance#считаем скорость
                    dist_per_time4 = distance1
                    buf_time = float(real_time2)
                    buf_time = buf_time - previous_time_stamp  # время одного расстояния
                    time_per_distance = buf_time  # время за которое суммировались расстояния. Это время <= per_time8=1 секунда
                    time_line3 += per_time8
                    list_speed.append(speed4)  # список скоростей speed4

                    # МОДУЛЬ СРЕДНЕГО УСКОРЕНИЯ В СЕКУНДУ
                    end_speed2 = speed4
                    acceleration2 = int(abs(end_speed2 - start_speed2))
                    start_speed2 = speed4
                    list_acceleration.append(acceleration2)  # список ускорений acceleration2

                list_distance.append(distance1)  # список всей дистанции
                list_time.append(buf_time)  # список всего времени


                # СРЕДНЯЯ ДЛИНА САККАДЫ
                if (distance1 > saccade):
                    list_saccade.append(distance1)  # список длин саккад distance1


                #СРЕДНЯЯ ЧАСТОТА ПОЯВЛЕНИЯ НОВОЙ ОБЛАСТИ ФИКСАЦИИ ЗА 1 СЕКУНДУ
                if float(real_time2) < time_line12:
                    if (distance_to_new_fixation > saccade):
                        fixation_counter3 += 1#считает фиксации за всё видео
                        fixation_counter4 += 1  # считает фиксации за 1-секундные интервалы
                        #distance_to_new_fixation=0#обнуляем расстояние от центра области фиксации
                else:
                    #нужна ещё проверка if (distance_to_new_fixation > saccade), вдруг это тоже фиксация и она входит в другой временной интервал
                    if (distance_to_new_fixation > saccade):
                        fixation_counter3 += 1
                        #distance_to_new_fixation=0#обнуляем расстояние от центра области фиксации

                    if (distance_to_new_fixation > saccade):#возможное появление области фиксации в следующем временном промежутке
                        fixation_counter4=1
                    else:
                        fixation_counter4=0

                    time_period_1_counter += 1  # считает число 1 секундных интервалов
                    time_line12 += per_time6

                list_fix_freq_1.append(fixation_counter4)# список числа новых областей фиксации за 1 секунду


                #СРЕДНЯЯ ЧАСТОТА ПОЯВЛЕНИЯ НОВОЙ ОБЛАСТИ ФИКСАЦИИ ЗА 10 СЕКУНД
                if float(real_time2) < time_line13:
                    if (distance_to_new_fixation > saccade):
                        fixation_counter5 += 1#считает фиксации за всё видео
                        fixation_counter6 += 1#считает фиксации за 10-секундные интервалы
                        #distance_to_new_fixation = 0  # обнуляем расстояние от центра области фиксации
                else:

                    # нужна ещё проверка if (distance_to_new_fixation > saccade):, вдруг это тоже фиксация и она входит в другой временной интервал
                    if (distance_to_new_fixation > saccade):
                        fixation_counter5 += 1
                        #distance_to_new_fixation = 0  # обнуляем расстояние от центра области фиксации

                    if (distance_to_new_fixation > saccade):  # возможное появление области фиксации в следующем временном промежутке
                        fixation_counter6 = 1
                    else:
                        fixation_counter6 = 0

                    time_period_10_counter+=1#считает число 10 секундных интервалов
                    time_line13+=per_time7

                list_fix_freq_10.append(fixation_counter6)  # список числа новых областей фиксации за 10 секунд


                # ЧИСЛО ФИКСАЦИЙ КОРОЧЕ 80 МС И ПРОДОЛЖИТЕЛЬНЕЕ 1000 мс
                if (distance_to_new_fixation > saccade):
                    # Выполняется только один раз. Записывется время первой фиксации.
                    if (flag2 == 0):
                        fix_time1 = float(real_time2)

                    if (flag2 == 1):
                        fix_time2 = float(real_time2)
                        fix_time = fix_time2 - fix_time1  # считаем время
                        fix_time1 = float(real_time2)

                    if (fix_time < 0.080):
                        fix_shorter_80 += 1
                    if (fix_time > 1):
                        fix_longer_1000 += 1

                    flag2 = 1

                debug_counter2+=1


                #АМПЛИТУДА САККАД МЕНЬШЕ/БОЛЬШЕ 6 УГЛОВЫХ ГРАДУСОВ

                if(distance1>sac_amplitude):#амплитуда саккады sac_amplitude равна 42 пикселям
                    more_6_FOV_counter+=1#счётчик саккад больше 6 угловых градусов
                else:
                    less_6_FOV_counter += 1#счётчик саккад меньше 6 угловых градусов


                #ДЛИТЕЛЬНОСТЬ ФИКСАЦИЙ МЕНЬШЕ/БОЛЬШЕ 180 МИЛИСЕКУНД
                buf_time_of_fix = float(real_time2)#буфер подсчёта времени между двумя соседними фиксациями
                buf_time_of_fix =buf_time_of_fix - previous_time_stamp

                #выполняется только один раз. Инициализация first_fix_coordinate, distance_from_first_fix, time_of_fix
                if(flag3==0):
                    first_fix_coordinate = p5  # координаты первой точки фиксации
                    #distance_from_first_fix = int(math.hypot(p6[0] - first_fix_coordinate[0],p6[1] - first_fix_coordinate[1]))  # вычисляем
                    # расстояние от точки первой фиксации
                    #time_of_fix = buf_time_of_fix  # время между двумя соседними фиксациями
                    flag3=1

                distance_from_first_fix = int(math.hypot(p6[0] - first_fix_coordinate[0],p6[1] - first_fix_coordinate[1]))  # вычисляем
                # расстояние от точки первой фиксации


                if(distance_from_first_fix<=saccade):#если взгляд не переместился в новую точку, то прибаляем это время к предыдущему времени фиксации
                    # (погрешность 1 пиксель). Если ставить distance1<=2 или больше, то time_of_fix растёт, а  more_180_ms_counter падает
                    #добавил distance_from_first_fix, что считаем
                    # погрешность от начальной точки, чтобы исключить ситуацию, когда взгляд будет упрыгивать по 1 пикселю
                    time_of_fix +=buf_time_of_fix   #время между двумя соседними фиксациями

                    #distance_from_first_fix = int(math.hypot(p6[0] - first_fix_coordinate[0],p6[1] - first_fix_coordinate[1]))  # вычисляем
                    # расстояние от точки первой фиксации

                else:
                    time_of_fix += buf_time_of_fix  # время между двумя соседними фиксациями
                    if(time_of_fix>time_of_fix_line):#time_of_fix_line время фиксации равное 180 мс
                        more_180_ms_counter+=1#счётчик фиксаций больше 180 мс
                    else:
                        less_180_ms_counter += 1#счётчик фиксаций больше 180 мс

                    time_of_fix = 0
                    first_fix_coordinate = p6  # координаты первой точки фиксации


                # СРЕДНЯЯ СКОРОСТЬ ВНУТРИ ОБЛАСТИ ФИКСАЦИИ
                # ИСПОЛЬЗОВАТЬ distance1 ИЛИ distance_to_new_fixation
                # ПОПРОБОВАТЬ НЕ СЧИТАТЬ расстояние внутри всех фиксации, складывать полученные скорости за 1 секунду и разделить на счетчик таких скоростей
                if (float(real_time2) < time_line14):

                    if (distance_to_new_fixation <= saccade):
                        distance_in_fix += distance1  # считает расстояние внутри одной фиксации
                        buf_time_in_fix = float(real_time2)
                        buf_time_in_fix = buf_time_in_fix - previous_time_stamp  # время одного перемещения внутри фиксации
                        time_in_fix += buf_time_in_fix  # считает время внутри одной фиксации
                        fix_flag = 1
                        list_all_distance_in_fix.append(distance1)#список всех длин дистанций внутри области фиксации
                        list_all_time_in_fix.append(buf_time_in_fix)#список всех времен внутри области фиксации
                    else:
                        if (fix_flag == 1):  # это сделано для того, чтобы считать скорость в области фиксации подряд в течении 1 секунды,
                            # если за эту секунду вклинивается саккада, то мы сразу считаем скорость в области фиксации,
                            # то есть делим полученную сумму расстояний в области фиксации на время
                            # а затем, если в эту секунду опять появятся области фиксации, то мы их опять складываем
                            # если один раз за секунду мы прибавили расстояние в области фиксации, а потом в эту же секунду была саккада (distance1 > saccade),
                            # то мы больше не складываем расстояния для этой области фиксации, а считаем скорость внутри неё
                            # и затем складываем следующие расстояния для следующей областей фиксации за эту секунду, если такие будут
                            if (time_in_fix == 0):  # в теории такого быть не может, т.к. все временные метки имеют разные значения
                                speed_in_fix = 0
                            else:
                                speed_in_fix = distance_in_fix / time_in_fix  # считаем скорость внутри области фиксации
                                distance_in_fix = 0
                                time_in_fix = 0
                            fix_flag = 0
                            list_speed_in_fix.append(speed_in_fix)  # список всех скоростей внутри области фиксации
                else:
                    time_line14 += per_time9
                    if (fix_flag == 1):  # это сделано для того, чтобы считать скорость в области фиксации подряд в течении 1 секунды,
                        # если за эту секунду вклинивается саккада, то мы сразу считаем скорость в области фиксации,
                        # то есть делим полученную сумму расстояний в области фиксации на время
                        # а затем, если в эту секунду опять появятся области фиксации, то мы их опять складываем
                        # если один раз за секунду мы прибавили расстояние в области фиксации, а потом в эту же секунду была саккада (distance1 > saccade),
                        # то мы больше не складываем расстояния для этой области фиксации, а считаем скорость внутри неё
                        # и затем складываем следующие расстояния для следующей областей фиксации за эту секунду, если такие будут
                        if (time_in_fix == 0):  # в теории такого быть не может, т.к. все временные метки имеют разные значения
                            speed_in_fix = 0
                        else:
                            speed_in_fix = distance_in_fix / time_in_fix  # считаем скорость внутри области фиксации
                            distance_in_fix = 0
                            time_in_fix = 0
                        fix_flag = 0
                        list_speed_in_fix.append(speed_in_fix)  # список всех скоростей внутри области фиксации


                # СРЕДНЯЯ СКОРОСТЬ САККАДЫ
                # ИСПОЛЬЗОВАТЬ distance1 ИЛИ distance_to_new_fixation, ИЛИ ОБА
                # ДОБАВИТЬ МАРКЕР БЫЛ ЛИ ЗА ЭТУ СЕКУНДУ ВХОД В ОБЛАСТЬ ФИКСАЦИИ
                if (float(real_time2) < time_line15):

                    if (distance_to_new_fixation > saccade) and (distance1 > saccade):
                        distance_in_sac += distance1  # считает расстояние одной саккады
                        buf_time_in_sac = float(real_time2)
                        buf_time_in_sac = buf_time_in_sac - previous_time_stamp
                        time_in_sac += buf_time_in_sac  # считает время одной саккады
                        sac_flag = 1
                        list_all_distance_in_sac.append(distance1)  # список всех длин дистанций внутри саккады
                        list_all_time_in_sac.append(buf_time_in_sac)  # список всех времен внутри саккады
                    else:
                        if (sac_flag == 1):  # это сделано для того, чтобы считать скорость саккад подряд в течении 1 секунды,
                            # если один раз за секунду мы прибавили расстояние саккады, а потом в эту же секунду была фиксация (distance1 < saccade),
                            # то мы больше не складываем расстояния для этой саккады, а считаем её скорость
                            # и затем складываем следующие расстояния для следующей саккады за эту секунду, если такие будут
                            if (time_in_sac == 0):  # в теории такого быть не может, т.к. все временные метки имеют разные значения
                                speed_in_sac = 0
                            else:
                                speed_in_sac = distance_in_sac / time_in_sac  # считаем скорость саккады
                                distance_in_sac = 0
                                time_in_sac = 0
                            sac_flag = 0
                            list_speed_in_sac.append(speed_in_sac)  # список всех скоростей саккады
                else:
                    time_line15 += per_time10
                    if (sac_flag == 1):  # это сделано для того, чтобы считать скорость саккад подряд в течении 1 секунды,
                            # если один раз за секунду мы прибавили расстояние саккады, а потом в эту же секунду была фиксация (distance1 < saccade),
                            # то мы больше не складываем расстояния для этой саккады, а считаем её скорость
                            # и затем складываем следующие расстояния для следующей саккады за эту секунду, если такие будут
                        if (time_in_sac == 0):  # в теории такого быть не может, т.к. все временные метки имеют разные значения
                            speed_in_sac = 0
                        else:
                            speed_in_sac = distance_in_sac / time_in_sac  # считаем скорость саккады
                            distance_in_sac = 0
                            time_in_sac = 0
                        sac_flag = 0
                        list_speed_in_sac.append(speed_in_sac)  # список всех скоростей саккады


                # МАКСИМАЛЬНАЯ МГНОВЕННАЯ СКОРОСТЬ
                time_max_velocity = float(real_time2)
                time_max_velocity = time_max_velocity - previous_time_stamp
                new_max_velocity = int(distance1 / time_max_velocity)

                list_velocity.append(new_max_velocity)# список всех мгновенных скоростей


                # КРИВИЗНА (считаем длину пути за 4 секунды и делим на длину расстояния между первой и последней точкой)
                # вычисления происходят внутри 4 -секундного интервала и затем берутся следующие 4 секунды.
                # Возможно надо делать смещение на 1 секунду и снова брать 4-секундный интервал.
                # И возможно надо счиать с первой секунды и брать 2 секунды до и 2 секунды после
                # Тогда получится 5-секундный интервал
                if float(real_time2) < time_line11:
                    length_of_path += distance1
                else:
                    time_line11 += per_time5
                    p_end = p6
                    distance_of_path = int(math.hypot(p_end[0] - p_start[0], p_end[1] - p_start[
                        1]))  # вычисляем длину расстояния между первой и последней точкой
                    if (distance_of_path == 0):
                        distance_of_path = 1
                    curvature = int(length_of_path / distance_of_path)  # вычисление кривизны траектории
                    length_of_path = distance1
                    p_start = p6

                list_curvature.append(curvature)#список значений кривизны траекторий


                #СРЕДНЯЯ СКОРОСТЬ САККАДЫ К ДЛИНЕ САККАДЫ
                if (distance1 > saccade):
                    length_sac=distance1
                    time_sac=float(real_time2)
                    time_sac=time_sac-previous_time_stamp
                    speed_sac=length_sac/time_sac
                    speed_to_length=int(speed_sac/length_sac)


                list_speed_to_length.append(speed_to_length)#список значений средней скорости саккады к длине саккады

            p5 = p6

            previous_time_stamp = float(real_time2)  # предыдущая временная метка


#СОРТИРУЕМ СПИСКИ ПО ВОЗРАСТАНИЮ
list_distance.sort()#сортируем по возрастанию список дистанций
list_time.sort()#сортируем по возрастанию список времени
list_speed.sort()#сортируем по возрастанию список скоростей

#УДАЛЯЕМ 10% МИНИМАЛЬНЫХ И МАКСИМАЛЬНЫХ ЗНАЧЕНИЙ ДИСТАНЦИИ
length_list_distance=len(list_distance)
list_distance_cut=int(length_list_distance/100*proc)#какое число минимальных и максимальных значений дистанции удалить
del list_distance[0:list_distance_cut]#удаляем 10% минимальных значений дистанции
length_list_distance=len(list_distance)#получаем новую длину списка после удаления
del list_distance[(length_list_distance-list_distance_cut):length_list_distance]#удаляем 10% максимальных значений дистанции


#УДАЛЯЕМ 10% МИНИМАЛЬНЫХ И МАКСИМАЛЬНЫХ ЗНАЧЕНИЙ ВРЕМЕНИ
length_list_time=len(list_time)
list_time_cut=int(length_list_time/100*proc)#какое число минимальных и максимальных значений времени удалить
del list_time[0:list_time_cut]#удаляем 10% минимальных значений времени
length_list_time=len(list_time)#получаем новую длину списка после удаления
del list_time[(length_list_time-list_time_cut):length_list_time]#удаляем 10% максимальных значений времени


#УДАЛЯЕМ 10% МИНИМАЛЬНЫХ И МАКСИМАЛЬНЫХ ЗНАЧЕНИЙ СКОРОСТИ
length_list_speed=len(list_speed)
list_speed_cut=int(length_list_speed/100*proc)#какое число минимальных и максимальных значений скорости удалить
del list_speed[0:list_speed_cut]#удаляем 10% минимальных значений скорости
length_list_speed=len(list_speed)#получаем новую длину списка после удаления
del list_speed[(length_list_speed-list_speed_cut):length_list_speed]#удаляем 10% максимальных значений скорости


# МИНИМАЛЬНАЯ И МАКСИМАЛЬНАЯ СКОРОСТЬ РАЗ В СЕКУНДУ
for i in range(len(list_speed)):

    if (list_speed[i] > 0.0) and (init_min == 0):  # нам интересна скорость отличная от нуля. Если учитывать ноль, то надо сделать условие speed4 >= 0.0
        #можно добавить тег присутствует ли ноль
        #init_min используется для задания первого ненулевого значения  min_speed. Сразу написать (min_speed > speed4) нельзя, потому что у нас
        # не задано значение min_speed
        #условие (speed4 > 0.0) и init_min нужны для задания первого значения min_speed отличного от нуля, если дальше условий (>0) нет.
        #Это было добавлено, когда я боялся случайных нулевого значения скорости, так как на тот момент первое значение дистанции было нулевое, хотя
        #оно и сейчас может быть нулевое
        min_speed = int(list_speed[i])
        init_min = 1

    if (list_speed[i] > 0.0) and (min_speed > list_speed[i]):  # нам интересна скорость отличная от нуля. Если учитывать ноль, то надо сделать условие speed4 >= 0.0
        min_speed = int(list_speed[i])

    if max_speed < list_speed[i]:
        max_speed = int(list_speed[i])

    if(list_speed[i]==0):
        speed4_zero_counter+=1#счётчик нулевых значений speed4


# СРЕДНЯЯ СКОРОСТЬ РАЗ В СЕКУНДУ
for i in range(len(list_distance)):
    all_distance+=list_distance[i]#считаем всё пройденное расстояние

for i in range(len(list_time)):
    all_time+=list_time[i]#считаем всё время


#МОДУЛЬ СРЕДНЕГО УСКОРЕНИЯ РАЗ В СЕКУНДУ

list_acceleration.sort()#сортируем по возрастанию список ускорений

#УДАЛЯЕМ 10% МИНИМАЛЬНЫХ И МАКСИМАЛЬНЫХ ЗНАЧЕНИЙ УСКОРЕНИЯ
length_list_acceleration=len(list_acceleration)
list_acceleration_cut=int(length_list_acceleration/100*proc)#какое число минимальных и максимальных значений ускорения удалить
del list_acceleration[0:list_acceleration_cut]#удаляем 10% минимальных значений ускорения
length_list_acceleration=len(list_acceleration)#получаем новую длину списка после удаления
del list_acceleration[(length_list_acceleration-list_acceleration_cut):length_list_acceleration]#удаляем 10% максимальных значений ускорений

for i in range(len(list_acceleration)):
    all_acc+=list_acceleration[i]
    acc_counter+=1

#МОДУЛЬ МИНИМАЛЬНОГО И МАКСИМАЛЬНОГО УСКОРЕНИЯ В СЕКУНДУ
for i in range(len(list_acceleration)):
    if (list_acceleration[i]>0) and (init_min3==0):#нам интересно ускорение отличное от нуля. Если учитывать ноль, то надо сделать условие acceleration2>=0.0
        acc_min=list_acceleration[i]
        init_min3=1

    if (list_acceleration[i]>0) and (acc_min>list_acceleration[i]):#нам интересно ускорение отличное от нуля. Если учитывать ноль,
        # то надо сделать условие list_acceleration[i]>=0.0
        acc_min=list_acceleration[i]

    if acc_max<list_acceleration[i]:
        acc_max=list_acceleration[i]

    if(list_acceleration[i] == 0):
        acceleration2_zero_counter += 1#счётчик нулевых значений list_acceleration[i]


 # СРЕДНЯЯ ДЛИНА САККАДЫ
list_saccade.sort()  # сортируем по возрастанию список длин саккад

# УДАЛЯЕМ 10% МИНИМАЛЬНЫХ И МАКСИМАЛЬНЫХ ЗНАЧЕНИЙ САККАД
length_list_saccade = len(list_saccade)
list_saccade_cut = int(length_list_saccade / 100*proc)  # какое число минимальных и максимальных значений длин саккад удалить
del list_saccade[0:list_saccade_cut]  # удаляем 10% минимальных значений длин саккад
length_list_saccade = len(list_saccade)  # получаем новую длину списка после удаления
del list_saccade[(length_list_saccade - list_saccade_cut):length_list_saccade]  # удаляем 10% максимальных значений длин саккад

for i in range(len(list_saccade)):
    sac_all+=list_saccade[i]
    sac_counter1+=1

# МИНИМАЛЬНАЯ И МАКСИМАЛЬНАЯ ДЛИНА САККАДЫ (ВОЗМОЖНОЕ МИНИМАЛЬНОЕ ЗНАЧЕНИЕ min_sac 100)
for i in range(len(list_saccade)):
    if (list_saccade[i] > saccade) and (init_min4 == 0):
        min_sac = list_saccade[i]
        init_min4 = 1

    if (list_saccade[i] > saccade) and (min_sac > list_saccade[i]):
        min_sac = list_saccade[i]

    if (list_saccade[i] > saccade) and (list_saccade[i] > max_sac):
        max_sac = list_saccade[i]


# СРЕДНЕЕ ЧИСЛО НОВЫХ ОБЛАСТЕЙ ФИКСАЦИИ ЗА 1 СЕКУНДУ
list_fix_freq_1.sort()  # сортируем по возрастанию список числа новых областей фиксации за 1 секунду
# УДАЛЯЕМ 10% МИНИМАЛЬНЫХ И МАКСИМАЛЬНЫХ ЗНАЧЕНИЙ САККАД
length_list_fix_freq_1 = len(list_fix_freq_1)
list_fix_freq_1_cut = int(length_list_fix_freq_1 / 100*proc)  # какое число минимальных и максимальных значений числа новых областей фиксации за 1 секунду удалить
del list_fix_freq_1[0:list_fix_freq_1_cut]  # удаляем 10% минимальных значений числа новых областей фиксации за 1 секунду
length_list_fix_freq_1 = len(list_fix_freq_1)  # получаем новую длину списка после удаления
del list_fix_freq_1[(length_list_fix_freq_1 - list_fix_freq_1_cut):length_list_fix_freq_1]  # удаляем 10% максимальных значений числа новых областей фиксации за 1 секунду

#берем 80% от числа всех фиксаций и числа 1-секундных временных периодов
fixation_counter3=fixation_counter3*((100-proc*2)/100)
time_period_1_counter=time_period_1_counter*((100-proc*2)/100)

# МИНИМАЛЬНАЯ И МАКСИМАЛЬНАЯ ЧАСТОТА ПОЯВЛЕНИЯ НОВОЙ ОБЛАСТИ ФИКСАЦИИ ЗА 1 СЕКУНДУ
for i in range(len(list_fix_freq_1)):
    if(list_fix_freq_1[i] >= 0) and (init_min5 == 0):  # частота может быть нулём. Если не учитывать ноль, то надо сделать условие list_fix_freq_1[i] > 0
        fix_freq_1_min = list_fix_freq_1[i]
        init_min5 = 1

    if (list_fix_freq_1[i] >= 0) and (fix_freq_1_min > list_fix_freq_1[i]):  # частота может быть нулём.
        # Если не учитывать ноль, то надо сделать условие list_fix_freq_1[i] > 0
        fix_freq_1_min = list_fix_freq_1[i]

    if fix_freq_1_max < list_fix_freq_1[i]:
        fix_freq_1_max = list_fix_freq_1[i]

    if (list_fix_freq_1[i] == 0):
        fixation_counter4_zero_counter += 1  # счётчик нулевых значений list_fix_freq_1[i]


# СРЕДНЕЕ ЧИСЛО НОВЫХ ОБЛАСТЕЙ ФИКСАЦИИ ЗА 10 СЕКУНД
list_fix_freq_10.sort()  # сортируем по возрастанию список числа новых областей фиксации за 1 секунду
# УДАЛЯЕМ 10% МИНИМАЛЬНЫХ И МАКСИМАЛЬНЫХ ЗНАЧЕНИЙ САККАД
length_list_fix_freq_10 = len(list_fix_freq_10)
list_fix_freq_10_cut = int(length_list_fix_freq_10 / 100*proc)  # какое число минимальных и максимальных значений числа новых областей фиксации за 10 секунд удалить
del list_fix_freq_10[0:list_fix_freq_10_cut]  # удаляем 10% минимальных значений числа новых областей фиксации за 10 секунд
length_list_fix_freq_10 = len(list_fix_freq_10)  # получаем новую длину списка после удаления
del list_fix_freq_10[(length_list_fix_freq_10 - list_fix_freq_10_cut):length_list_fix_freq_10]  # удаляем 10% максимальных значений
 # числа новых областей фиксации за 10 секунд

# берем 80% от числа всех фиксаций и числа 10-секундных временных периодов
fixation_counter5 = fixation_counter5 * ((100 - proc * 2) / 100)
time_period_10_counter = time_period_10_counter * ((100 - proc * 2) / 100)

# МИНИМАЛЬНАЯ И МАКСИМАЛЬНАЯ ЧАСТОТА ПОЯВЛЕНИЯ НОВОЙ ОБЛАСТИ ФИКСАЦИИ ЗА 10 СЕКУНД
# ПОДУМАТЬ ПРО НУЛИ
for i in range(len(list_fix_freq_10)):
    if (list_fix_freq_10[i] >= 0) and (init_min6 == 0):  # частота может быть нулём. Если не учитывать ноль, то надо сделать условие list_fix_freq_10[i] > 0
        fix_freq_10_min = list_fix_freq_10[i]
        init_min6 = 1

    if (list_fix_freq_10[i] >= 0) and (fix_freq_10_min > list_fix_freq_10[i]):  # частота может быть нулём.
        # Если не учитывать ноль, то надо сделать условие list_fix_freq_10[i] > 0
        fix_freq_10_min = list_fix_freq_10[i]

    if fix_freq_10_max < list_fix_freq_10[i]:
        fix_freq_10_max = list_fix_freq_10[i]

    if (list_fix_freq_10[i] == 0):
        fixation_counter6_zero_counter += 1  # счётчик нулевых значений list_fix_freq_10[i]


# ЧИСЛО ФИКСАЦИЙ КОРОЧЕ 80 МС И ПРОДОЛЖИТЕЛЬНЕЕ 1000 мс
# берем 80% от числа всех фиксаций короче 80 мс и дольше 1000 мс
fix_shorter_80 =fix_shorter_80* ((100 - proc * 2) / 100)
fix_longer_1000 =fix_longer_1000* ((100 - proc * 2) / 100)


#АМПЛИТУДА САККАД МЕНЬШЕ/БОЛЬШЕ 6 УГЛОВЫХ ГРАДУСОВ
# берем 80% от числа всех амплитуд саккад меньше/больше 6 угловых градусов
less_6_FOV_counter =less_6_FOV_counter* ((100 - proc * 2) / 100)#счётчик саккад меньше 6 угловых градусов
more_6_FOV_counter=more_6_FOV_counter* ((100 - proc * 2) / 100)#счётчик саккад больше 6 угловых градусов


#ДЛИТЕЛЬНОСТЬ ФИКСАЦИЙ МЕНЬШЕ/БОЛЬШЕ 180 МИЛИСЕКУНД
# берем 80% от числа всех длительностей фиксаций меньше/больше 180 милисекунд
less_180_ms_counter=less_180_ms_counter* ((100 - proc * 2) / 100)#счётчик фиксаций меньше 180 мс
more_180_ms_counter=more_180_ms_counter* ((100 - proc * 2) / 100)#счётчик фиксаций больше 180 мс


# СРЕДНЯЯ СКОРОСТЬ ВНУТРИ ОБЛАСТИ ФИКСАЦИИ
#СОРТИРУЕМ СПИСКИ ПО ВОЗРАСТАНИЮ
list_all_distance_in_fix.sort()  # сортируем по возрастанию список дистанций внутри области фиксации
list_all_time_in_fix.sort()  # сортируем по возрастанию список всех времен внутри области фиксации
list_speed_in_fix.sort()#сортируем список всех скоростей внутри области фиксации

#УДАЛЯЕМ 10% МИНИМАЛЬНЫХ И МАКСИМАЛЬНЫХ ЗНАЧЕНИЙ ДИСТАНЦИИ ВНУТРИ ОБЛАСТИ ФИКСАЦИИ
length_list_all_distance_in_fix=len(list_all_distance_in_fix)
list_all_distance_in_fix_cut=int(length_list_all_distance_in_fix/100*proc)#какое число минимальных и максимальных значений дистанции удалить
del list_all_distance_in_fix[0:list_all_distance_in_fix_cut]#удаляем 10% минимальных значений дистанции
length_list_all_distance_in_fix=len(list_all_distance_in_fix)#получаем новую длину списка после удаления
del list_all_distance_in_fix[(length_list_all_distance_in_fix-list_all_distance_in_fix_cut):length_list_all_distance_in_fix]#удаляем
# 10% максимальных значений дистанции

#УДАЛЯЕМ 10% МИНИМАЛЬНЫХ И МАКСИМАЛЬНЫХ ЗНАЧЕНИЙ ВРЕМЕНИ ВНУТРИ ОБЛАСТИ ФИКСАЦИИ
length_list_all_time_in_fix=len(list_all_time_in_fix)
list_all_time_in_fix_cut=int(length_list_all_time_in_fix/100*proc)#какое число минимальных и максимальных значений времени внутри области фиксации удалить
del list_all_time_in_fix[0:list_all_time_in_fix_cut]#удаляем 10% минимальных значений времени внутри области фиксации
length_list_all_time_in_fix=len(list_all_time_in_fix)#получаем новую длину списка после удаления
del list_all_time_in_fix[(length_list_all_time_in_fix-list_all_time_in_fix_cut):length_list_all_time_in_fix]#удаляем 10% максимальных
# значений времени внутри области фиксации

#УДАЛЯЕМ 10% МИНИМАЛЬНЫХ И МАКСИМАЛЬНЫХ ЗНАЧЕНИЙ СКОРОСТИ
length_list_speed_in_fix=len(list_speed_in_fix)
list_speed_in_fix_cut=int(length_list_speed_in_fix/100*proc)#какое число минимальных и максимальных значений скорости внутри области фиксации удалить
del list_speed_in_fix[0:list_speed_in_fix_cut]#удаляем 10% минимальных значений скорости внутри области фиксации
length_list_speed_in_fix=len(list_speed_in_fix)#получаем новую длину списка после удаления
del list_speed_in_fix[(length_list_speed_in_fix-list_speed_in_fix_cut):length_list_speed_in_fix]#удаляем 10% максимальных
# значений скорости внутри области фиксации

for i in range(len(list_all_distance_in_fix)):
    all_distance_in_fix += list_all_distance_in_fix[i]  # считает расстояние внутри всех фиксации

for i in range(len(list_all_time_in_fix)):
    all_time_in_fix += list_all_time_in_fix[i]  # считает время внутри всех фиксации

# МИНИМАЛЬНАЯ И МАКСИМАЛЬНАЯ СКОРОСТЬ ВНУТРИ ОБЛАСТИ ФИКСАЦИИ
for i in range(len(list_speed_in_fix)):
    if (list_speed_in_fix[i] > 0) and (init_min7 == 0):  # нам интересна скорость отличная от нуля.
        # Если учитывать ноль, то надо сделать условие list_speed_in_fix[i] >= 0.0
        min_speed_in_fix = list_speed_in_fix[i]
        init_min7 = 1

    if (list_speed_in_fix[i] > 0) and (min_speed_in_fix > list_speed_in_fix[i]):  # нам интересна скорость отличная от нуля.
        # Если учитывать ноль, то надо сделать условие list_speed_in_fix[i] >= 0.0
        min_speed_in_fix = list_speed_in_fix[i]

    if max_speed_in_fix < list_speed_in_fix[i]:
        max_speed_in_fix = list_speed_in_fix[i]

    if (list_speed_in_fix[i] == 0):
        speed_in_fix_zero_counter += 1  # счётчик нулевых значений list_speed_in_fix[i]


# СРЕДНЯЯ СКОРОСТЬ САККАДЫ
#СОРТИРУЕМ СПИСКИ ПО ВОЗРАСТАНИЮ
list_all_distance_in_sac.sort()  # сортируем по возрастанию список дистанций внутри саккады
list_all_time_in_sac.sort()  # сортируем по возрастанию список всех времен внутри саккады
list_speed_in_sac.sort()#сортируем список всех скоростей внутри саккады


#УДАЛЯЕМ 10% МИНИМАЛЬНЫХ И МАКСИМАЛЬНЫХ ЗНАЧЕНИЙ ДИСТАНЦИИ САККАДЫ
length_list_all_distance_in_sac=len(list_all_distance_in_sac)
list_all_distance_in_sac_cut=int(length_list_all_distance_in_sac/100*proc)#какое число минимальных и максимальных значений дистанции удалить
del list_all_distance_in_sac[0:list_all_distance_in_sac_cut]#удаляем 10% минимальных значений дистанции
length_list_all_distance_in_sac=len(list_all_distance_in_sac)#получаем новую длину списка после удаления
del list_all_distance_in_sac[(length_list_all_distance_in_sac-list_all_distance_in_sac_cut):length_list_all_distance_in_sac]#удаляем
# 10% максимальных значений дистанции

#УДАЛЯЕМ 10% МИНИМАЛЬНЫХ И МАКСИМАЛЬНЫХ ЗНАЧЕНИЙ ВРЕМЕНИ САККАДЫ
length_list_all_time_in_sac=len(list_all_time_in_sac)
list_all_time_in_sac_cut=int(length_list_all_time_in_sac/100*proc)#какое число минимальных и максимальных значений времени саккады удалить
del list_all_time_in_sac[0:list_all_time_in_sac_cut]#удаляем 10% минимальных значений времени саккады
length_list_all_time_in_sac=len(list_all_time_in_sac)#получаем новую длину списка после удаления
del list_all_time_in_sac[(length_list_all_time_in_sac-list_all_time_in_sac_cut):length_list_all_time_in_sac]#удаляем 10% максимальных
# значений времени внутри области фиксации

#УДАЛЯЕМ 10% МИНИМАЛЬНЫХ И МАКСИМАЛЬНЫХ ЗНАЧЕНИЙ СКОРОСТИ САККАДЫ
length_list_speed_in_sac=len(list_speed_in_sac)
list_speed_in_sac_cut=int(length_list_speed_in_sac/100*proc)#какое число минимальных и максимальных значений скорости саккады удалить
del list_speed_in_sac[0:list_speed_in_sac_cut]#удаляем 10% минимальных значений скорости саккады
length_list_speed_in_sac=len(list_speed_in_sac)#получаем новую длину списка после удаления
del list_speed_in_sac[(length_list_speed_in_sac-list_speed_in_sac_cut):length_list_speed_in_sac]#удаляем 10% максимальных
# значений скорости саккады

for i in range(len(list_all_distance_in_sac)):
    all_distance_in_sac += list_all_distance_in_sac[i]# считает расстояние всех саккад

for i in range(len(list_all_time_in_sac)):
    all_time_in_sac += list_all_time_in_sac[i]# считает время всех саккад

# МИНИМАЛЬНАЯ И МАКСИМАЛЬНАЯ СКОРОСТЬ САККАДЫ
for i in range(len(list_speed_in_sac)):

    if (list_speed_in_sac[i] > 0) and (init_min8 == 0):  # нам интересна скорость отличная от нуля.
        # Если учитывать ноль, то надо сделать условие list_speed_in_sac[i] >= 0.0
        min_speed_in_sac = list_speed_in_sac[i]
        init_min8 = 1

    if (list_speed_in_sac[i] > 0) and (min_speed_in_sac > list_speed_in_sac[i]):  # нам интересна скорость отличная от нуля.
        # Если учитывать ноль, то надо сделать условие list_speed_in_sac[i] >= 0.0
        min_speed_in_sac = list_speed_in_sac[i]

    if max_speed_in_sac < list_speed_in_sac[i]:
        max_speed_in_sac = list_speed_in_sac[i]

    if (list_speed_in_sac[i] == 0):
        speed_in_sac_zero_counter += 1  # счётчик нулевых значений list_speed_in_sac[i]


#МАКСИМАЛЬНАЯ МГНОВЕННАЯ СКОРОСТЬ
list_velocity.sort()  # сортируем по возрастанию список всех мгновенных скоростей

#УДАЛЯЕМ 10% МИНИМАЛЬНЫХ И МАКСИМАЛЬНЫХ ЗНАЧЕНИЙ МГНОВЕННОЙ СКОРОСТИ
length_list_velocity=len(list_velocity)
list_velocity_cut=int(length_list_velocity/100*proc)#какое число минимальных и максимальных значений значений мгновенной скорости удалить
del list_velocity[0:list_velocity_cut]#удаляем 10% минимальных значений мгновенной скорости
length_list_velocity=len(list_velocity)#получаем новую длину списка после удаления
del list_velocity[(length_list_velocity-list_velocity_cut):length_list_velocity]#удаляем 10% максимальных
# значений мгновенной скорости

for i in range(len(list_velocity)):
    if (max_velocity < list_velocity[i]):
        max_velocity = list_velocity[i]


#СРЕДНЯЯ КРИВИЗНА ТРАЕКТОРИИ
list_curvature.sort()  # сортируем по возрастанию список всех значений кривизны

#УДАЛЯЕМ 10% МИНИМАЛЬНЫХ И МАКСИМАЛЬНЫХ ЗНАЧЕНИЙ КРИВИЗНЫ
length_list_curvature=len(list_curvature)#длина списка значений кривизны
list_curvature_cut=int(length_list_curvature/100*proc)#какое число минимальных и максимальных значений кривизны удалить
del list_curvature[0:list_curvature_cut]#удаляем 10% минимальных значений кривизны
length_list_curvature=len(list_curvature)#получаем новую длину списка после удаления
del list_curvature[(length_list_curvature-list_curvature_cut):length_list_curvature]#удаляем 10% максимальных
# значений мгновенной скорости

for i in range(len(list_curvature)):
    curvature_sum += list_curvature[i]
    curvature_counter += 1

# МИНИМАЛЬНАЯ И МАКСИМАЛЬНАЯ КРИВИЗНА (считаем длину пути за 4 секунды и делим на длину расстояния между первой и последней точкой)
for i in range(len(list_curvature)):

    if (list_curvature[i] > 0.0) and (init_min2 == 0):  # нам интересна кривизна отличная от нуля.
        # Если учитывать ноль, то надо сделать условие list_velocity[i] >= 0.0
        min_curvature = list_curvature[i]
        init_min2 = 1

    if (list_curvature[i] > 0.0) and (min_curvature > list_curvature[i]):  # верхнее условие необходимо для задания первого ненулевого
        # значения для list_curvature[i],
        # если сразу (min_curvature>list_curvature[i]), то мы будем сравнивать min_curvature=0 с ненулевыми значениями list_curvature[i]
        # и это условие никогда не выполнится
        # нам интересна кривизна отличная от нуля. Если учитывать ноль, то надо сделать условие list_curvature[i] >= 0.0
        min_curvature = list_curvature[i]

    if max_curvature < list_curvature[i]:
        max_curvature = list_curvature[i]

    if (list_curvature[i] == 0):
        curvature_zero_counter += 1  # счётчик нулевых значений list_curvature[i]


#СРЕДНЯЯ СКОРОСТЬ САККАДЫ К ДЛИНЕ САККАДЫ
list_speed_to_length.sort()  # сортируем по возрастанию список всех значений кривизны

#УДАЛЯЕМ 10% МИНИМАЛЬНЫХ И МАКСИМАЛЬНЫХ ЗНАЧЕНИЙ СРЕДНЕЙ СКОРОСТИ САККАДЫ К ДЛИНЕ САККАДЫ
length_list_speed_to_length=len(list_speed_to_length)#длина списка значений средней скорости саккады к длине саккады
list_speed_to_length_cut=int(length_list_speed_to_length/100*proc)#какое число минимальных и максимальных значений средней скорости саккады к длине саккады удалить
del list_speed_to_length[0:list_speed_to_length_cut]#удаляем 10% минимальных значений средней скорости саккады к длине саккады
length_list_speed_to_length=len(list_speed_to_length)#получаем новую длину списка после удаления
del list_speed_to_length[(length_list_speed_to_length-list_speed_to_length_cut):length_list_speed_to_length]#удаляем 10% максимальных
# значений средней скорости саккады к длине саккады

for i in range(len(list_speed_to_length)):
    speed_to_length_sum += list_speed_to_length[i]
    speed_to_length_counter += 1

# МИНИМАЛЬНАЯ И МАКСИМАЛЬНАЯ СКОРОСТЬ САККАДЫ К ДЛИНЕ САККАДЫ
for i in range(len(list_speed_to_length)):

    if (list_speed_to_length[i] > 0.0) and (init_min9 == 0):  # нам интересна скорость отличная от нуля. Если учитывать ноль,
        # то надо сделать условие list_speed_to_length[i] >= 0.0
        # можно добавить тег присутствует ли ноль
        min_speed_to_length = list_speed_to_length[i]
        init_min9 = 1

    if (list_speed_to_length[i] > 0.0) and (min_speed_to_length > list_speed_to_length[i]):  # нам интересна скорость отличная от нуля. Если учитывать ноль,
        # то надо сделать условие list_speed_to_length[i] >= 0.0
        min_speed_to_length = list_speed_to_length[i]

    if max_speed_to_length < list_speed_to_length[i]:
        max_speed_to_length = list_speed_to_length[i]

    if (list_speed_to_length[i] == 0):
        speed_to_length_zero_counter += 1  # счётчик нулевых значений list_speed_to_length[i]


#СРЕДНЕЕ ЗНАЧЕНИЕ PPI
with open(ppi_file_path, "r") as f6:
    for string3 in f6.readlines()[2:]:#читает с третьей строки
        string3 = re.findall(r'\d+[.]\d+|\d+', string3)
        ppi = int(string3[1])

        list_ppi.append(ppi)#список значений ppi

#СРЕДНЕЕ ЗНАЧЕНИЕ PPI
list_ppi.sort()  # сортируем по возрастанию список всех значений PPI

#УДАЛЯЕМ 10% МИНИМАЛЬНЫХ И МАКСИМАЛЬНЫХ ЗНАЧЕНИЙ PPI
length_list_ppi=len(list_ppi)#длина списка значений PPI
list_ppi_cut=int(length_list_ppi/100*proc)#какое число минимальных и максимальных значений PPI удалить
del list_ppi[0:list_ppi_cut]#удаляем 10% минимальных значений PPI
length_list_ppi=len(list_ppi)#получаем новую длину списка после удаления
del list_ppi[(length_list_ppi-list_ppi_cut):length_list_ppi]#удаляем 10% максимальных
# значений PPI

for i in range(len(list_ppi)):
    ppi_sum += list_ppi[i]
    ppi_counter += 1

# МИНИМАЛЬНОЕ И МАКСИМАЛЬНОЕ PPI
for i in range(len(list_ppi)):

    if (list_ppi[i] > 0) and (init_min10 == 0):  # нам интересна скорость отличная от нуля. Если учитывать ноль, то надо сделать условие list_ppi[i] >= 0.0
        # можно добавить тег присутствует ли ноль
        ppi_min = list_ppi[i]
        init_min10 = 1

    if (list_ppi[i] > 0) and (ppi_min > list_ppi[i]):  # нам интересна скорость отличная от нуля. Если учитывать ноль, то надо сделать условие list_ppi[i] >= 0.0
        ppi_min= list_ppi[i]

    if ppi_max < list_ppi[i]:
        ppi_max = list_ppi[i]

    if (list_ppi[i] == 0):
        ppi_zero_counter += 1  # счётчик нулевых значений list_ppi[i]


#ПОДСЧЁТ СРЕДНИХ НЕКОТОРЫХ ПАРАМЕТРОВ ЗНАЧЕНИЙ И СИТУАЦИЙ С НУЛЕВЫМИ ЗНАЧЕНИЯМИ
if (all_time == 0):
    average_speed = 0
else:
    average_speed=int(all_distance/all_time)
if (sac_counter1 == 0):
    sac_all_average = 0
else:
    sac_all_average=int(sac_all/sac_counter1)
fix_freq_1=fixation_counter3/time_period_1_counter
fix_freq_1=toFixed(fix_freq_1,2)
fix_shorter_80 =int(fix_shorter_80)
fix_longer_1000 =int(fix_longer_1000)
less_6_FOV_counter =int(less_6_FOV_counter)
more_6_FOV_counter=int(more_6_FOV_counter)
less_180_ms_counter=int(less_180_ms_counter)
more_180_ms_counter=int(more_180_ms_counter)
if (all_time_in_fix == 0):
    average_speed_in_fix = 0
else:
    average_speed_in_fix = int(all_distance_in_fix/all_time_in_fix)
if (all_time_in_sac == 0):
    average_speed_in_sac = 0
else:
    average_speed_in_sac=int(all_distance_in_sac/all_time_in_sac)
if (acc_counter == 0):
    average_acc = 0
else:
    average_acc=int(all_acc/acc_counter)
curvature_aver=int(curvature_sum/curvature_counter)
fix_freq_10=fixation_counter5/time_period_10_counter
fix_freq_10=toFixed(fix_freq_10,1)
min_speed_in_fix=int(min_speed_in_fix)
max_speed_in_fix=int(max_speed_in_fix)
min_speed_in_sac=int(min_speed_in_sac)
max_speed_in_sac=int(max_speed_in_sac)
if (speed_to_length_counter == 0):
    average_speed_to_length = 0
else:
    average_speed_to_length=int(speed_to_length_sum/speed_to_length_counter)
ppi_average=int(ppi_sum/ppi_counter)#среднее значение list_ppi[i]

#РАЗОБРАТЬСЯ С ВЫВОДОМ В ОБЩИЙ ФАЙЛ

f3.write('Static parameters: '+ '\n')
f3.write('\n')

f3.write('Average speed of gaze = ' + str(average_speed) +" px/sec"+ '\n')
f3.write('Minimum speed of gaze = ' + str(min_speed) + " px/sec"+ '\n')
f3.write('Maximum speed of gaze = ' + str(max_speed) + " px/sec"+ '\n')
f3.write('\n')

f3.write('Average speed in fixation area = ' + str(average_speed_in_fix) + " px/sec"+ '\n')
f3.write('Minimum speed in fixation area = ' + str(min_speed_in_fix) + " px/sec"+ '\n')
f3.write('Maximum speed in fixation area = ' + str(max_speed_in_fix) + " px/sec"+ '\n')
f3.write('\n')

f3.write('Average speed of saccade = ' + str(average_speed_in_sac) + " px/sec"+ '\n')
f3.write('Minimum speed of saccade = ' + str(min_speed_in_sac) + " px/sec"+ '\n')
f3.write('Maximum speed of saccade = ' + str(max_speed_in_sac) + " px/sec"+ '\n')
f3.write('\n')

f3.write('Average acceleration module = ' + str(average_acc) + " px/sec2"+ '\n')
f3.write('Minimum acceleration module = ' + str(acc_min) + " px/sec2"+ '\n')
f3.write('Maximum acceleration module = ' + str(acc_max) + " px/sec2"+ '\n')
f3.write('\n')

f3.write('Average length of saccade = ' + str(sac_all_average) + " px"+ '\n')
f3.write('Minimum length of saccade = ' + str(min_sac) + " px"+ '\n')
f3.write('Maximum length of saccade = ' + str(max_sac) + " px"+ '\n')
f3.write('\n')

f3.write('Average frequency of new fixation area = ' + str(fix_freq_1) + " Hz"+ '\n')
f3.write('Minimum frequency of new fixation area = ' + str(fix_freq_1_min) + " Hz"+ '\n')
f3.write('Maximum frequency of new fixation area = ' + str(fix_freq_1_max) + " Hz"+ '\n')
f3.write('\n')

f3.write('Average number of new fixation area per 10 second = ' + str(fix_freq_10) + " times"+ '\n')
f3.write('Minimum number of new fixation area per 10 second = ' + str(fix_freq_10_min) + " times"+ '\n')
f3.write('Maximum number of new fixation area per 10 second = ' + str(fix_freq_10_max) + " times"+ '\n')
f3.write('\n')

f3.write('Average curvature = ' + str(curvature_aver) + '\n')
f3.write('Minimum curvature = ' + str(min_curvature) + '\n')
f3.write('Maximum curvature = ' + str(max_curvature) + '\n')
f3.write('\n')

f3.write('Average velocity of saccade to length of saccade  = ' + str(average_speed_to_length) + '\n')
f3.write('Minimum velocity of saccade to length of saccade  = ' + str(min_speed_to_length) + '\n')
f3.write('Maximum velocity of saccade to length of saccade  = ' + str(max_speed_to_length) + '\n')
f3.write('\n')

f3.write('Number of saccades less 6 degree FOV = ' + str(less_6_FOV_counter) + '\n')
f3.write('Number of saccades more 6 degree FOV = ' + str(more_6_FOV_counter) + '\n')
f3.write('Number of fixations less 180 ms = ' + str(less_180_ms_counter) + '\n')
f3.write('Number of fixations more 180 ms = ' + str(more_180_ms_counter) + '\n')
f3.write('\n')

f3.write('Maximum velocity of gaze = ' + str(max_velocity) + " px/sec"+ '\n')
f3.write('Fixations shorter 80 ms = ' + str(fix_shorter_80)+" times"+ '\n')
f3.write('Fixations longer 1000 ms = ' + str(fix_longer_1000)+" times"+ '\n')
f3.write('\n')

f3.write('Average value of PPI  = ' + str(ppi_average) + '\n')
f3.write('Minimum value of PPI  = ' + str(ppi_min) + '\n')
f3.write('Maximum value of PPI  = ' + str(ppi_max) + '\n')
f3.write('\n')



f3.write('All values in string:'+ '\n')
f3.write(str(average_speed)+";"+str(min_speed)+";"+str(max_speed)+";")
f3.write(str(average_speed_in_fix)+";"+str(min_speed_in_fix)+";"+str(max_speed_in_fix)+";")
f3.write(str(average_speed_in_sac)+";"+str(min_speed_in_sac)+";"+str(max_speed_in_sac)+";")
f3.write(str(average_acc)+";"+str(acc_min)+";"+str(acc_max)+";")
f3.write(str(sac_all_average)+";"+str(min_sac)+";"+str(max_sac)+";")
f3.write(str(fix_freq_1)+";"+str(fix_freq_1_min)+";"+str(fix_freq_1_max)+";")
f3.write(str(fix_freq_10)+";"+str(fix_freq_10_min)+";"+str(fix_freq_10_max)+";")
f3.write(str(curvature_aver)+";"+str(min_curvature)+";"+str(max_curvature)+";")
f3.write(str(average_speed_to_length)+";"+str(min_speed_to_length)+";"+str(max_speed_to_length)+";")
f3.write(str(less_6_FOV_counter)+";"+str(more_6_FOV_counter)+";"+str(less_180_ms_counter)+";"+str(more_180_ms_counter)+";")
f3.write(str(max_velocity)+";"+str(fix_shorter_80)+";"+str(fix_longer_1000)+";"+ '\n')
f3.write(str(ppi_average)+";"+str(ppi_min)+";"+str(ppi_max)+";"+ '\n')
f3.write('\n')


f3.write('Minimum speed of gaze zero counter = ' + str(speed4_zero_counter) + '\n')
f3.write('Minimum speed in fixation area zero counter = ' + str(speed_in_fix_zero_counter) + '\n')
f3.write('Minimum speed in saccade zero counter = ' + str(speed_in_sac_zero_counter) + '\n')
f3.write('Minimum acceleration module zero counter = ' + str(acceleration2_zero_counter) + '\n')
f3.write('Minimum frequency of new fixation area per 1 second zero counter = ' + str(fixation_counter4_zero_counter) + '\n')
f3.write('Minimum frequency of new fixation area per 10 second zero counter = ' + str(fixation_counter6_zero_counter) + '\n')
f3.write('Minimum curvature zero counter = ' + str(curvature_zero_counter) + '\n')
f3.write('Minimum velocity of saccade to length of saccade zero counter = ' + str(speed_to_length_zero_counter) + '\n')
f3.write('Minimum value of PPI zero counter = ' + str(ppi_zero_counter) + '\n')
f3.write('\n')



#выводим статические параметры со всех видео
f5.write(str(average_speed)+";"+str(min_speed)+";"+str(max_speed)+";")
f5.write(str(average_speed_in_fix)+";"+str(min_speed_in_fix)+";"+str(max_speed_in_fix)+";")
f5.write(str(average_speed_in_sac)+";"+str(min_speed_in_sac)+";"+str(max_speed_in_sac)+";")
f5.write(str(average_acc)+";"+str(acc_min)+";"+str(acc_max)+";")
f5.write(str(sac_all_average)+";"+str(min_sac)+";"+str(max_sac)+";")
f5.write(str(fix_freq_1)+";"+str(fix_freq_1_min)+";"+str(fix_freq_1_max)+";")
f5.write(str(fix_freq_10)+";"+str(fix_freq_10_min)+";"+str(fix_freq_10_max)+";")
f5.write(str(curvature_aver)+";"+str(min_curvature)+";"+str(max_curvature)+";")
f5.write(str(average_speed_to_length)+";"+str(min_speed_to_length)+";"+str(max_speed_to_length)+";")
f5.write(str(less_6_FOV_counter)+";"+str(more_6_FOV_counter)+";"+str(less_180_ms_counter)+";"+str(more_180_ms_counter)+";")
f5.write(str(max_velocity)+";"+str(fix_shorter_80)+";"+str(fix_longer_1000)+";")
f5.write(str(ppi_average)+";"+str(ppi_min)+";"+str(ppi_max)+";"+ '\n')

#f3.write('start_time_plus_30 = ' + str(start_time_plus_30) + '\n')
#f3.write('end_time_minus_30 = ' + str(end_time_minus_30) + '\n')
#f3.write('\n')

f3.close()
f5.close()