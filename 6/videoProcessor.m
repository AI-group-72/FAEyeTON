% Детектим элементы кокпита.
% Детектор предварительно обучается в Net_test

close all

% numClasses = 4;
% 
% vidPath = 'C:\Projects\DBs\007+.avi';
% csvPath = strcat(vidPath, '2.csv');
% 
% csvOpts = delimitedTextImportOptions('Delimiter', ';'); 
% tic
% S = readmatrix(csvPath, csvOpts);
% [n, ~] = size(S);
% frameNums(1:n-1) = 0; eyesX(1:n-1) = 0; eyesY(1:n-1) = 0; headShiftX(1:n-1) = 0; headShiftY(1:n-1) = 0; 
% BllGears = [];
% toc
% for i = 2:n
%     frameNums(i-1) = round(str2double(S(i, 1))); 
%     eyesX(i-1) = str2double(S(i, 2)); % координаты зрачка
%     eyesY(i-1) = str2double(S(i, 3));
%     for j = 1:16
%         BllGears(i-1, j) = str2double(S(i, j+3));
%     end
%     headShiftX(i-1) = str2double(S(i, 20)); % смещение головы. Внимание: относительная величина!
%     headShiftY(i-1) = str2double(S(i, 21));
% end
% 
% n = n-1; % поправка на заголовок файла 
% save('vid_processor_all.mat');
% return

return

load('vid_processor_all.mat');

frameNo = 1;
v = VideoReader(vidPath);
vidResultPatch = strcat(vidPath, '_big_out.avi');
w = VideoWriter(vidResultPatch, 'MPEG-4');
w.Quality = 65;
open(w);

videoFrame = readFrame(v); 
I = imresize(videoFrame, [450 600]); 
writeVideo(w, I);

figure;
  
while hasFrame(v)
    %% загружаем лейблы 
    
    videoFrame = readFrame(v); 
    frameNo = frameNo + 1;
    
    I = imresize(videoFrame, [450 600]);    % примерно     
    
    for vvv = 1: numClasses
        for zzz = 1:4
            AllGears(vvv, zzz) = BllGears(frameNo, vvv * 4 + zzz - 4);
        end
    end     
    
    %% Выводим найденное на экран
    
    arrColors = {'cyan','yellow', 'blue', 'green', 'red', 'magenta'};  
    IAnnotated = I;
    
    for k = 1:numClasses        
        position = AllGears(k,:);   %  AllGearsFileCur  
        if position(1) < 0
            continue
        end  
        
        llabel = strcat('gear ', int2str(k));        

        col = arrColors(mod(k, 6) + 1);         
       
        IAnnotated = insertObjectAnnotation(IAnnotated, 'rectangle', position(1:size(position, 1), :), llabel,...
                                                'TextBoxOpacity', 0.6, 'FontSize', 12, 'Color', col); 
    end     
    
    IAnnotated = insertShape(IAnnotated, 'circle', [eyesX(frameNo) eyesY(frameNo) 13]);
    
    imshow(IAnnotated);   
    
    writeVideo(w,IAnnotated);
end
close(w);