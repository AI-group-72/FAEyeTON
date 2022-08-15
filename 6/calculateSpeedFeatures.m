function calculateSpeedFeatures(vidPath)
% фича-вектор для скорости зрачка и головы

if nargin < 1      
    vidPath = 'D:\Projects\USC#12ST3_encoded_0000.mp4'; 
end

%% Читаем файл csv 
 
csvPath = strcat(vidPath, '+alpha.csv');

csvOpts = delimitedTextImportOptions('Delimiter', ';'); 

S = readmatrix(csvPath, csvOpts);
[n, ~] = size(S);
XX(n-1) = 0.0; YY(n-1) = 0.0; fX(n-1) = 0.0; fY(n-1) = 0.0; frameNo(n-1) = 1;
for i = 2:n
    frameNo(i-1) = round(str2double(S(i, 1))); 
    XX(i-1) = str2double(S(i, 2)); % координаты зрачка
    YY(i-1) = str2double(S(i, 3));
    fX(i-1) = str2double(S(i, 20)); % смещение головы. Внимание: относительная величина!
    fY(i-1) = str2double(S(i, 21));
end

n = n-1; % поправка на заголовок файла 

%% Поправка на пропуск кадров сдвига головы

for i = 2:n
    if fX(i) == 4242  % не смогли распознать смещение кадра
        fX(i) = fX(i-1);
        fY(i) = fY(i-1);
    end    
end

% причёсываем выбросы

k = 0;
while max(fX) > 1152
    [~, i] = max(fX);
    if (i > 0 ) && (i < n)
        xx = (fX(i-1) + fX(i+1))/2;
        yy = (fY(i-1) + fY(i+1))/2;
        fX(i) = xx;
        fY(i) = yy;
    end
    
    [~, i] = max(fY);
    if (i > 0 ) && (i < n)
        xx = (fX(i-1) + fX(i+1))/2;
        yy = (fY(i-1) + fY(i+1))/2;
        fX(i) = xx;
        fY(i) = yy;
    end
    
    [~, i] = min(fX);
    if (i > 0 ) && (i < n)
        xx = (fX(i-1) + fX(i+1))/2;
        yy = (fY(i-1) + fY(i+1))/2;
        fX(i) = xx;
        fY(i) = yy;
    end
    
    [~, i] = min(fY);
    if (i > 0 ) && (i < n)
        xx = (fX(i-1) + fX(i+1))/2;
        yy = (fY(i-1) + fY(i+1))/2;
        fX(i) = xx;
        fY(i) = yy;   
    end
    
    k = k + 1;
    if k > 100
        break
    end
end

for i = 2:n-1
    xx = (fX(i-1) + fX(i+1))/2;
    yy = (fY(i-1) + fY(i+1))/2;
    
    if (abs(fX(i) - xx) > 170) || (abs(fY(i) - yy) > 170) 
%         fprintf('[%f] [%f] [%f] \n', fX(i-1), fX(i), fX(i+1));
        fX(i) = xx;
        fY(i) = yy;
    end     
end 
% 
% [v, i] = max(fX);
% fprintf('max = %f fNo = %f  \n', v, frameNo(i));

%% Переводим значения головы из относительных в абсолютные
headX = fX * 0;
headY = fY * 0;

for i = 2:n
    headX(i) = headX(i-1) + fX(i);
    headY(i) = headY(i-1) + fY(i);
end    

%% фильтруем движения глаза: поправка на кадры, где пропущен зрачок

for i = 3:n
    if (XX(i) < 0) || (YY(i) < 0)  % не смогли распознать зрачок
        XX(i) = XX(i-1) + (XX(i-1) - XX(i-2)); % заменяем на значение предыдущего кадра. И делаем поправку на скорость.
        YY(i) = YY(i-1) + (YY(i-1) - YY(i-2)); 
    end    
end

%% считаем горизонтальную скорость и вертикальную скорость того и другого

eyeVX = XX * 0;
eyeVY = XX * 0;
headVX = XX * 0;
headVY = XX * 0;

for i = 2:n 
    eyeVX(i) = abs(XX(i) - XX(i-1)) * 30;
    eyeVY(i) = abs(YY(i) - YY(i-1)) * 30;
    headVX(i) = abs(fX(i)) * 30;
    headVY(i) = abs(fY(i)) * 30;
end

%% фильтруем результаты медианой

eyeVX = medfilt1(eyeVX, 5);
eyeVY = medfilt1(eyeVY, 5);
headVX = medfilt1(headVX, 5);
headVY = medfilt1(headVY, 5);

%% Сохранение результатов

outPath = strcat(vidPath, '+speed_features.csv'); 
fprintf('writing results to %s\n',  outPath);

writeHeader(outPath);
S = [];
for i = 1:n
    S(i, 1) = frameNo(i);
    S(i, 2) = eyeVX(i); 
    S(i, 3) = eyeVY(i); 
    S(i, 4) = headVX(i); 
    S(i, 5) = headVY(i);     
end 
   
writematrix(S, outPath, 'Delimiter', ';', 'WriteMode', 'append');
end

function writeHeader(path)
  S = ["FrameNo", "eye_SpeedX", "eye_SpeedY", "head_SpeedX", "head_SpeedY"];
  writematrix(S, path, 'Delimiter', ';');
end

% function B = medianFilterWithWindow(A, windowSize)
% % windowSize считаем нечётным
% B = A;
% n = size(A);
% wHalf = floor(windowSize/2)+1;
% for i = wHalf:n-wHalf
%     C = A(i-wHalf, i+wHalf);
%     B(i) = medfilt1
% 
% end