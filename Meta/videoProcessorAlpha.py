import os
import numpy as np
import cv2
import glob
from sys import argv
from math import pi
import datetime
import os.path


def HashString(s):
    result = ''
    for i in range(len(s)):
        if ord('0') <= ord(s[i]) <= ord('9'):
            result = result + s[i]
    return result


def DoLog(line):
    # запись лога
    path = os.curdir + '\\log-' + HashString(argv[1]) + '.txt'
    file1 = open(path, 'a')
    line = str(datetime.datetime.now()) + ' ' + line + '\n'
    file1.write(line)
    file1.close()


def LastLine(path):
    with open(path) as f:
        for line in f:
            pass
    return line
    f.close()


def DoProcessing(inputVideo):
    # на вход получает путь к видеофайлу.
    # вычисляется относительное (!) смещение головы в градусах и наклон в градусах.
    # результат записывается в текстовый файл и в массив transforms.
    EyetrackerFOV = 82 # указание угла обзора камеры сцены окулографа, в угловых градусах
    EyetrackerPixels = 1084 # указание расширения окулографа, в пикселях
    EyetrackerPixToFOV = EyetrackerFOV/EyetrackerPixels  # для перевода смещения из пикселей в градусы для камеры сцены 

    outputTxt = inputVideo + '+alpha.csv'
    DoLog('start processing of ' + inputVideo)
    cap = cv2.VideoCapture(inputVideo)
    num_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

    if os.path.isfile(outputTxt):
        # проверяем, вдруг мы этот файл уже обработали, полностью или частично
        line = LastLine(outputTxt)
        prevFrameNo = int(line.split(';')[0]) - 1

        if (num_frames - prevFrameNo) < 10:
            # сброс хвоста видео
            DoLog('already processed ' + inputVideo)
            print('already processed ' + inputVideo)
            return
        print('Skiping frames. Start processing from frame No ' + str(prevFrameNo))
        for i in range(0, prevFrameNo):
            _, prev_frame = cap.read()
            if i/1000 == round(i/1000):
                print(i)
        fileTxt = open(outputTxt, 'a')
        prevFrameNo = prevFrameNo
    else:
        # файл ни разу не обрабатывался ранее
        prevFrameNo = 0
        fileTxt = open(outputTxt, 'w')
        fileTxt.write('FrameNo;eye_X;eye_Y;FlightInstr1_X;FlightInstr1_Y;FlightInstr1_W;FlightInstr1_H;FlightInstr2_X;FlightInstr2_Y;FlightInstr2_W;FlightInstr2_H;FlightInstr3_X;FlightInstr3_Y;FlightInstr3_W;FlightInstr3_H;FlightInstr4_X;FlightInstr4_Y;FlightInstr4_W;FlightInstr4_H;FrameShift_X;frameShift_Y;frameRotation_deg\n')
        fileTxt.write('1;-0;-0;-1;-1;-1;-1;-1;-1;-1;-1;-1;-1;-1;-1;-1;-1;-1;-1;0;0;0;\n')

    _, prev_frame = cap.read()
    prev_gray = cv2.cvtColor(prev_frame, cv2.COLOR_BGR2GRAY)
    transforms = np.zeros((num_frames - 1, 3), np.float32)

    for i in range(prevFrameNo, num_frames - 1):
        if i == round(num_frames * 0.01):
            print(inputVideo + ":  1% of processing done")
        if i == round(num_frames * 0.33):
            print(inputVideo + ": 33% of processing done")
        if i == round(num_frames * 0.66):
            print(inputVideo + ": 66% of processing done")

        # Расчёт оптического потока между кадрами / Calculate optical flow between consecutive frames
        translation_x = 0
        translation_y = 0
        rotation_angle = 0

        prev_points = cv2.goodFeaturesToTrack(
            prev_gray,
            maxCorners=200,
            qualityLevel=0.1,
            minDistance=20,
            blockSize=4
        )
        success, curr_frame = cap.read()
        if not success:
            DoLog('Error reading file '+inputVideo + ' |frame ' + str(i))
            break

        curr_gray = cv2.cvtColor(curr_frame, cv2.COLOR_BGR2GRAY)
        try:
            # вычисляем оптический поток при помощи Канаде-Лукаса
            curr_points, status, err = cv2.calcOpticalFlowPyrLK(
                prev_gray,
                curr_gray,
                prev_points,
                None,
                2
            )
        except:
            # обработка битых частей видео, где кадр представляет собой, например, серый прямоугольник
            DoLog('another bad frame ' + str(i+2) + ' in ' + inputVideo)
            line = str(i+2) + ';-0;-0;-1;-1;-1;-1;-1;-1;-1;-1;-1;-1;-1;-1;-1;-1;-1;-1;' + str(translation_x) + ';' + str(translation_y) + ';' + str(rotation_angle) + ';\n'
            fileTxt.write(line)
            # prev_gray = curr_gray
            continue

        assert prev_points.shape == curr_points.shape
        idx = np.where(status == 1)[0]
        prev_points = prev_points[idx]
        curr_points = curr_points[idx]

        if len(curr_points) > 0:
            # Оценка аффинных преобразований (включая поворот) между точками / Estimate affine transformation between the points
            try:
                matrix, _ = cv2.estimateAffine2D(prev_points, curr_points)
                translation_x = matrix[0, 2]
                translation_y = matrix[1, 2]
                rotation_angle = (180/pi) * np.arctan2(matrix[1, 0], matrix[0, 0])

                # переводим из пикселей в градусы
                translation_x = translation_x * EyetrackerPixToFOV
                translation_y = translation_y * EyetrackerPixToFOV
            except:
                DoLog('bad frame ' + str(i+2) + ' in ' + inputVideo)

        if abs(rotation_angle) > 15:
            # отбрасываем невозможно резкие наклоны головы, явный артефакт записи
            translation_x = 0
            translation_y = 0
            rotation_angle = 0

        transforms[i] = [translation_x, translation_y, rotation_angle]

        translation_x = round(translation_x, 3)
        translation_y = round(translation_y, 3)
        rotation_angle = round(rotation_angle, 3)
        line = str(translation_x) + ';' + str(translation_y) + ';' + str(rotation_angle) + ';\n'
        line = str(i+2) + ';-0;-0;-1;-1;-1;-1;-1;-1;-1;-1;-1;-1;-1;-1;-1;-1;-1;-1;' + line
        fileTxt.write(line)
        prev_gray = curr_gray

    fileTxt.close()
    cap.release()
    DoLog('finished processing of ' + inputVideo)
    # return transforms


if __name__ == '__main__':
    # скрипт принимает 1 аргумент командной строки - маску для поиска видеофайлов.
    # например:
    # c:\Folder\Experiments\Participant_5\*\Eyes\*\*.mp4
    # обработает все файлы по удовлетворяющем маску путям.

    print('mask: ', argv[1])
    mask = argv[1]
    mp4list = glob.glob(mask, recursive=True)
    print('\nfiles found:\n')
    print(*mp4list, sep='\n')
    print('Starting to process ' + str(len(mp4list)) + ' files')
    for i in range(len(mp4list)):
        print('processing ' + mp4list[i])
        DoProcessing(mp4list[i])
        print('File is 100% processed.\n')
