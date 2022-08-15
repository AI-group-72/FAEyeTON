% Детектим только зрачок и поворот головы

close all

numClasses = 4;
circleColor = [254 25 2];          
vidPath = 'D:\Projects\USC#12ST2_encoded_0000.mp4';
csvPath = strcat(vidPath, '+alpha.csv');
writeNewFileLonger(csvPath, numClasses);

frameNo = 1;
v = VideoReader(vidPath); 

  
AllGears = -ones(numClasses, 4);    

% for kk = 1:7837 % этот цикл закомментить, а две строчки раскомментить.
%     videoFrame = readFrame(v);  
%     frameNo = frameNo + 1;
% end

videoFrame = readFrame(v);
I = imresize(videoFrame, [449 599]); 
scale = 599/1280;
 
% figure;
% for kkk = 1:100
while hasFrame(v)
    %% ищем в текущем кадре   
 
    predI = I;
    videoFrame = readFrame(v);
    I = videoFrame ;
    frameNo = frameNo + 1;    
    
    [eyeX, eyeY] = findMyCircles(I, circleColor);  % зрачок

    I = imresize(I, [449 599]);    % примерно  
 
    %% вычисляем сдвиг относительно предыдущего кадра
     
     [ii, jj, angle] = coordsByCorrelation3(predI, I, scale);  % коррелируем предыдущий кадр с текущим
        
    %% Сохраняем координаты в файле
 
    writeNewLineLonger(csvPath, numClasses, frameNo, eyeX, eyeY, AllGears, ii, jj, angle); 
    
    disp(frameNo);
    
    %% Выводим на экран
    
%     IAnnotated = videoFrame;
%     
%     IAnnotated = insertShape(IAnnotated, 'circle', [eyeX eyeY 13]);
%     
%     IAnnotated = imresize(IAnnotated, 2);
% 
%     imshow(IAnnotated);   
end
