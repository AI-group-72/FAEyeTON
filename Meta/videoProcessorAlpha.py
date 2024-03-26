import os
import numpy as np
import cv2 
from math import pi
import datetime
import os.path
import statistics as st
from scipy import ndimage as ndi


class SceneProcessor:
    EyetrackerHorizontalFOV = 82
    EyetrackerFrameWidth = -1
    EyetrackerFrameHeight = -1
    EyetrackerFPS = 30
    _trajectory_x = []  # координаты по x и
    _trajectory_y = []  # y
    _trajectory_r = []  # Наклон головы
    _confidence = []    # Если 0 - данные x, y, r не получилось достоверно расчитать.
    _length = 0  # в кадрах

    def __init__(self, doLogging = False):
        self.doLogging = doLogging

    def LoadVideo(self, path):
        self.inputPath = path
        vcap = cv2.VideoCapture(path)
        if vcap.isOpened():
            width = vcap.get(cv2.CAP_PROP_FRAME_WIDTH)
            height = vcap.get(cv2.CAP_PROP_FRAME_HEIGHT)
            self.EyetrackerFrameWidth = int(width)
            self.EyetrackerFrameHeight = int(height)
            self.EyetrackerFPS = vcap.get(cv2.CAP_PROP_FPS)
            self._length = int(vcap.get(cv2.CAP_PROP_FRAME_COUNT))
##            print('width, height, fps, total frames:', width, height, self.EyetrackerFPS, self._length)  # debug only
        vcap.release()

    def _DoLog(self, line):
        # запись лога
        if self.doLogging:
            path = os.curdir + '\\log_videoprocessor.txt'
            file1 = open(path, 'a')
            line = str(datetime.datetime.now()) + ' ' + line + '\n'
            file1.write(line)
            file1.close()

    def _bilateralFtr1D(self, y, sSpatial = 0.2, sIntensity = 1):
        """
        version: 1.0
        author: akshay
        date: 10/03/2016

        The equation of the bilateral filter is

                (       dx ^ 2       )       (         dI ^2        )
        F = exp (- ----------------- ) * exp (- ------------------- )
                (  sigma_spatial ^ 2 )       (  sigma_Intensity ^ 2 )
            ~~~~~~~~~~~~~~~~~~~~~~~~~~
            This is a guassian filter!
            dx - The 'geometric' distance between the 'center pixel' and the pixel
             to sample
        dI - The difference between the intensity of the 'center pixel' and
             the pixel to sample
        sigma_spatial and sigma_Intesity are constants. Higher values mean
        that we 'tolerate more' higher value of the distances dx and dI.

        Dependencies: numpy, scipy.ndimage.gaussian_filter1d

        calc gaussian kernel size as: filterSize = (2 * radius) + 1; radius = floor (2 * sigma_spatial)
        y - input data
        """
        # gaussian filter and parameters
        radius = np.floor (2 * sSpatial)
        filterSize = int((2 * radius) + 1)
        ftrArray = np.zeros(filterSize)
        ftrArray[int(radius)] = 1

        # Compute the Gaussian filter part of the Bilateral filter
        gauss = ndi.gaussian_filter1d(ftrArray, sSpatial)

        # 1d data dimensions
        width = y.size

        # 1d resulting data
        ret = np.zeros (width)

        for i in range(width):

            ## To prevent accessing values outside of the array
            # The left part of the lookup area, clamped to the boundary
            xmin = int(max (i - radius, 1));
            # How many columns were outside the image, on the left?
            dxmin = int(xmin - (i - radius));

            # The right part of the lookup area, clamped to the boundary
            xmax = int(min (i + radius, width));
            # How many columns were outside the image, on the right?
            dxmax = int((i + radius) - xmax);

            # The actual range of the array we will look at
            area = y [xmin:xmax]

            # The center position
            center = y [i]

            # The left expression in the bilateral filter equation
            # We take only the relevant parts of the matrix of the
            # Gaussian weights - we use dxmin, dxmax, dymin, dymax to
            # ignore the parts that are outside the image
            expS = gauss[(1+dxmin):(filterSize-dxmax)]

            # The right expression in the bilateral filter equation
            dy = y [xmin:xmax] - y [i]
            dIsquare = (dy * dy)
            expI = np.exp (- dIsquare / (sIntensity * sIntensity))

            # The bilater filter (weights matrix)
            F = expI * expS

            # Normalized bilateral filter
            Fnormalized = F / sum(F)

            # Multiply the area by the filter
            tempY = y [xmin:xmax] * Fnormalized

            # The resulting pixel is the sum of all the pixels in
            # the area, according to the weights of the filter
            # ret(i,j,R) = sum (tempR(:))
            ret[i] = sum (tempY)
        return ret


    def DoProcessing(self, videoprocessing_fastener = 1):
        # основной метод обработки.
        # videoprocessing_fastener - параметр для ускорения обработки ценой качества. Чем выше - тем быстрее.
        # Для повышения скорости снижается разрешение картинки и количество отслеживаемых особых точек.
        if self.EyetrackerFrameWidth == -1:
            self._DoLog('Couldn''t open ' + self.inputPath)
            print('Couldn''t open ' + self.inputPath)  # debug only
            return

        doSpeedup = videoprocessing_fastener != 1
        new_height = int(self.EyetrackerFrameHeight/videoprocessing_fastener)
        new_width = int(self.EyetrackerFrameWidth/videoprocessing_fastener)
        new_dimensions = (new_width, new_height)

        EyetrackerPixToFOV = self.EyetrackerHorizontalFOV/self.EyetrackerFrameWidth
        self._DoLog('start processing of ' + self.inputPath)
        cap = cv2.VideoCapture(self.inputPath)
        num_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

        # если раскомментировать, то можно будет проверить,
        # вдруг мы этот файл уже обработали, полностью или частично, и продолжить обработку
        # if os.path.isfile(outputTxt):
        #     line = LastLine(outputTxt)
        #     prevFrameNo = int(line.split(';')[0]) - 1
        #     if (num_frames - prevFrameNo) < 10:  # на последние 10 кадров плевать
        #         self._DoLog('already processed ' + self.inputPath)
        #         return
        #     print('Skiping frames. Start processing from frame No ' + str(prevFrameNo))
        #     for i in range(0, prevFrameNo):
        #         _, prev_frame = cap.read()
        #         if i/1000 == round(i/1000):
        #             print(i)
        #     fileTxt = open(outputTxt, 'a')
        #     prevFrameNo = prevFrameNo
        # else:
        #     # файл ни разу не обрабатывался ранее
        #     prevFrameNo = 0
        #     fileTxt = open(outputTxt, 'w')
        #     fileTxt.write('FrameNo;eye_X;eye_Y;FlightInstr1_X;FlightInstr1_Y;FlightInstr1_W;FlightInstr1_H;FlightInstr2_X;FlightInstr2_Y;FlightInstr2_W;FlightInstr2_H;FlightInstr3_X;FlightInstr3_Y;FlightInstr3_W;FlightInstr3_H;FlightInstr4_X;FlightInstr4_Y;FlightInstr4_W;FlightInstr4_H;FrameShift_X;frameShift_Y;frameRotation_deg\n')
        #     fileTxt.write('1;-0;-0;-1;-1;-1;-1;-1;-1;-1;-1;-1;-1;-1;-1;-1;-1;-1;-1;0;0;0;\n')

        self._trajectory_x = [0] * self._length
        self._trajectory_y = [0] * self._length
        self._trajectory_r = [0] * self._length
        self._confidence = [0] * self._length
        self._confidence[0] = 1
        self._length = num_frames
        prevFrameNo = 0
        _, prev_frame = cap.read()  # читаем первый кадр
        prev_gray = cv2.cvtColor(prev_frame, cv2.COLOR_BGR2GRAY)

        if doSpeedup:  # тут даунсайз изображения
            prev_gray = cv2.resize(prev_gray, new_dimensions)

        for i in range(prevFrameNo+1, num_frames):
            """ # debug only
            if i == round(num_frames * 0.01):
                print(self.inputPath + ":  1% of processing done")
            if i == round(num_frames * 0.33):
                print(self.inputPath + ": 33% of processing done")
            if i == round(num_frames * 0.66):
                print(self.inputPath + ": 66% of processing done")
            """

            # Вычисляем оптический поток
            translation_x = 0
            translation_y = 0
            rotation_angle = 0
            confidence_est = 0
            tmpMaxCorners = int(200 / videoprocessing_fastener)

            prev_points = cv2.goodFeaturesToTrack(
                prev_gray,
                maxCorners=tmpMaxCorners,
                qualityLevel=0.1,
                minDistance=20,
                blockSize=4
            )

            success, curr_frame = cap.read()  # читаем очередной кадр
            if not success:
                self._DoLog('Error reading file ' + self.inputPath + ' |frame ' + str(i))
                break

            curr_gray = cv2.cvtColor(curr_frame, cv2.COLOR_BGR2GRAY)
            if doSpeedup:  # тут даунсайз изображения
                curr_gray = cv2.resize(curr_gray, new_dimensions)

            try:
                # вычисляем оптический поток
                curr_points, status, err = cv2.calcOpticalFlowPyrLK(
                    prev_gray,
                    curr_gray,
                    prev_points,
                    None,
                    2
                )
            except:
                # сюда попадаем в основном когда видео битое, и кадр представляет собой серый прямоугольник
                self._DoLog('another bad frame ' + str(i+2) + ' in ' + self.inputPath)
                self._trajectory_x[i] = self._trajectory_x[i-1]  # вставляем предыдущие значения
                self._trajectory_y[i] = self._trajectory_y[i-1]
                self._trajectory_r[i] = self._trajectory_r[i-1]
                self._confidence[i]   = 0  # в этом кадре мы совершенно не уверены
                continue

            assert prev_points.shape == curr_points.shape
            idx = np.where(status == 1)[0]
            prev_points = prev_points[idx]
            curr_points = curr_points[idx]

            if len(curr_points) > 0:
                # Оцениваем параметры аффинного преобразования между точками
                try:
                    matrix, _ = cv2.estimateAffine2D(prev_points, curr_points)
                    translation_x = matrix[0, 2]
                    translation_y = matrix[1, 2]
                    rotation_angle = (180/pi) * np.arctan2(matrix[1, 0], matrix[0, 0])
                    confidence_est = 1

                    # переводим из пикселей в градусы
                    translation_x = translation_x * EyetrackerPixToFOV
                    translation_y = translation_y * EyetrackerPixToFOV
                except:
                    self._DoLog('bad frame ' + str(i+2) + ' in ' + self.inputPath)

            if abs(rotation_angle) > 15:
                # слишком резким наклон головы быть не может, 450 градусов/сек - за гранью
                translation_x = 0
                translation_y = 0
                rotation_angle = 0
                confidence_est = 0

            if doSpeedup:
                translation_x  = translation_x * videoprocessing_fastener
                translation_y  = translation_y * videoprocessing_fastener
                rotation_angle = rotation_angle * videoprocessing_fastener

            self._trajectory_x[i] = translation_x + self._trajectory_x[i-1]  # записываем в массив, попутно переводя из относительных
            self._trajectory_y[i] = translation_y + self._trajectory_y[i-1]  # координат в абсолютные
            self._trajectory_r[i] = rotation_angle + self._trajectory_r[i-1]
            self._confidence[i] = confidence_est

            prev_gray = curr_gray

        cap.release()
        self._DoLog('finished processing of ' + self.inputPath)


    def DoPostprocessing(self, FilteringPower = 1):
        # FilteringPower характеризует силу постпроцессинга.
        # Значение 0 - это отсутствие фильтрации вообще.
        # Значение 1 означает, что будут вычислены медианные значения за первые
        # 60 секунд, и их вычтут из остальных величин.
        # Значение более 1 означает применение ещё и билатеральной фильтрации к
        # величинам x, y и r. Чем выше величина - тем сильнее фильтрация.
        if FilteringPower == 0:
          return

        if FilteringPower >= 1:
          time_sec = 60
          amount_of_frames = int(time_sec * self.EyetrackerFPS)
          n = min(self._length, amount_of_frames)
          tx = self._trajectory_x[1:n]
          ty = self._trajectory_y[1:n]
          tr = self._trajectory_r[1:n]

          med_x = st.median(tx)
          med_y = st.median(ty)
          med_r = st.median(tr)

          self._trajectory_x = [x - med_x for x in self._trajectory_x]
          self._trajectory_y = [y - med_y for y in self._trajectory_y]
          self._trajectory_r = [r - med_r for r in self._trajectory_r]

          if FilteringPower == 1:
            return

          # применяем билатеральную фильтрацию
          sigma_r = FilteringPower / 5
          sigma_i = FilteringPower - 1
          np_trajectory_x = self._bilateralFtr1D(np.asarray(self._trajectory_x), sigma_r, sigma_i)
          self._trajectory_x = np_trajectory_x.tolist()

          np_trajectory_y = self._bilateralFtr1D(np.asarray(self._trajectory_y), sigma_r, sigma_i)
          self._trajectory_y = np_trajectory_y.tolist()

          sigma_i = sigma_i/2
          np_trajectory_r = self._bilateralFtr1D(np.asarray(self._trajectory_r), sigma_r, sigma_i)
          self._trajectory_r = np_trajectory_r.tolist()


    def SaveToCSV(self, path):
        gaze_timestamp = 0
        fileTxt = open(path, 'w')
        fileTxt.write('gaze_timestamp,world_index,confidence,head_pos_x,head_pos_y,head_rotation,gaze_point_3d_x,gaze_point_3d_y,gaze_point_3d_z,eye_center0_3d_x,eye_center0_3d_y,eye_center0_3d_z,gaze_normal0_x,gaze_normal0_y,gaze_normal0_z,eye_center1_3d_x,eye_center1_3d_y,eye_center1_3d_z,gaze_normal1_x,gaze_normal1_y,gaze_normal1_z\n')
        for i in range(0, self._length):
           translation_x  = round(self._trajectory_x[i], 3)
           translation_y  = round(self._trajectory_y[i], 3)
           rotation_angle = round(self._trajectory_r[i], 3)
           confidence = self._confidence[i]

           gz_time = round(gaze_timestamp, 3)

           line = str(gz_time) + ',' + str(i+1) + ',' +  str(confidence) + ',' + str(translation_x) + ',' + str(translation_y) + ',' + str(rotation_angle) + ',\n'
           fileTxt.write(line)
           gaze_timestamp = gaze_timestamp + 1/self.EyetrackerFPS

        fileTxt.close()

if __name__ == '__main__':
    # Пример использования
    inputVideoPath = "video_test.avi"
    outputPath = inputVideoPath + '+alpha.csv'

    v = SceneProcessor(doLogging=True)
    v.EyetrackerHorizontalFOV = 82  # угол обзора камеры сцены айтрекера. Обычно есть в паспорте модели.
    v.LoadVideo(inputVideoPath)
    v.DoProcessing(5)  # рекомендуемое значение 1
    v.DoPostprocessing(5)  # рекомендуемое значение 1. Выше - для сильно зашумлённых данных.
    v.SaveToCSV(outputPath)

    print("Done!")
