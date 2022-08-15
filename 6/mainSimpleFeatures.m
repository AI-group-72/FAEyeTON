function mainSimpleFeatures(vidPath)
% Детектим только зрачок и поворот головы
    if nargin < 1
        vidPath = 'D:\Projects\USC#21ST1.mp4';
        close all;
    end

%     disp(vidPath);    
%     n1 = strfind(vidPath, 'USC');
    experimentName = vidPath; % substr(vidPath,n1,8);
    fprintf('\n'); disp("Start processing of " + experimentName);

    numClasses = 4;
    circleColor = [255 23 1];          

    csvPath = strcat(vidPath, '+alpha.csv');
    writeNewFileLonger(csvPath, numClasses);

    frameNo = 1;
    v = VideoReader(vidPath); 


    AllGears = -ones(numClasses, 4);    

    videoFrame = readFrame(v);
    scale = 599/1280;   
    
    I = videoFrame;
    Igray = rgb2gray(imresize(videoFrame, [449 599])); 
    ptsI = detectSURFFeatures(Igray);        
    [featuresI, validPtsI] = extractFeatures(Igray, ptsI);
    
%     figure;
    
    while hasFrame(v)
        %% ищем в текущем кадре   
        predI = I;      
        featuresPred = featuresI; 
        validPtsPred = validPtsI;
        
        videoFrame = readFrame(v);
        I = videoFrame ;
        frameNo = frameNo + 1;    
        
        if frameNo == round(v.NumFrames*0.33)
            disp(experimentName + ": preprocessing: 33% done");
        elseif frameNo == round(v.NumFrames*0.66)
            disp(experimentName + ": preprocessing: 66% done");
        end

        [eyeX, eyeY] = findMyCircles(I, circleColor);  % зрачок

        Igray = rgb2gray(imresize(I, [449 599]));    % примерно  

        %% вычисляем сдвиг относительно предыдущего кадра      

        ptsI = detectSURFFeatures(Igray);        
        [featuresI, validPtsI] = extractFeatures(Igray, ptsI);
        
        warning('off','all');
        [ii, jj, angle] = coordsByCorrelation4(featuresPred, validPtsPred, featuresI, validPtsI, scale);  % коррелируем предыдущий кадр с текущим
        warning('on','all');
        %% Сохраняем координаты в файле

        writeNewLineLonger(csvPath, numClasses, frameNo, eyeX, eyeY, AllGears, ii, jj, angle); 

%         disp(frameNo);

        %% Выводим на экран
%         J = imtranslate(I,[-ii, -jj]); 
%         
%         subplot(1,2,1);
%         imshow(predI);  
%         subplot(1,2,2);
%         imshow(J);
 
    end
    
    disp(experimentName + ": preprocessing: 100% done");
    

end