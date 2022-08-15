function calculateFixationsFeatures2(alphaDataPath)
%% Считаем количество фиксаций в секунду

if nargin ~= 1      
  % для целей дебага
  alphaDataPath = 'G:\Projects\USC#07ST3.mp4'; 
  disp('no file selected');
end

%% Читаем файл csv  
csvPath = strcat(alphaDataPath, '+alpha.csv');  % устаревший вариант
csvPath = alphaDataPath;                        % теперь передаём целиком имя файла с +alpha

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

%% Поправка на кадры, где пропущен зрачок

for i = 2:n
    if (XX(i) < 0) || (YY(i) < 0)  % не смогли распознать зрачок
        XX(i) = XX(i-1); % заменяем на значение предыдущего кадра. Можно добавить поправку на скорость
        YY(i) = YY(i-1);
    end    
end

%% Выделяем фиксации

Fixations = XX*0;
for i = 1:n-1
    if XX(i) + YY(i) < 2  %% зрачок имеет координаты (0, 0) или где-то там
        Fixations(i) = 0;
        continue;
    end
    distance = hypot(XX(i+1) - XX(i), YY(i+1) - YY(i));
    if distance < 3 
        Fixations(i) = 1;
        Fixations(i+1) = 1;
    end
end

for i = 2:n-1  % заполняем короткие разрывы фиксаций
    if (Fixations(i) == 0)&&(Fixations(i-1) == 1)&&(Fixations(i+1) == 1)
      Fixations(i) = 1;
    end
end

for i = 2:n-2
    if (Fixations(i) == 0) && (Fixations(i+1) == 0) &&(Fixations(i-1) == 1)&&(Fixations(i+2) == 1)
      Fixations(i)   = 1;
      Fixations(i+1) = 1;
    end
end

for i = 2:n-1  % удаляем слишком короткие фиксации
    if (Fixations(i) == 1)&&(Fixations(i-1) == 0)&&(Fixations(i+1) == 0)
      Fixations(i) = 0;
    end
end

allFixs = [];  % структура, хранящая начало и конец фиксации
fixsStarts = XX * 0; % структура, соответствующая кадрам, в которой каждое начало и каждый конец фиксации отмечается единицей
afN = 0;

for i = 1:n-2
    if (Fixations(i) == 0) && (Fixations(i+1) == 1)
        fixsStarts(i+1) = 1;
        
        afN = afN + 1;
        allFixs(afN, 1) = i+1; %#ok<AGROW>
        for j = i+1:n-1
            if (Fixations(j) == 1)  && (Fixations(j+1) == 0)
                allFixs(afN, 2) = j;
                
                fixsStarts(j) = 1;
                break
            end
            
            if j == n
                allFixs(afN, 2) = j;
            end
        end
    end
end
% теперь у нас afN фиксаций, каждая из которых начинается в allFixs(i, 1) и
% заканчивается в allFixs(i, 2).

%% Строим фича-вектор
% фильтруем гауссианой

A = smoothdata(fixsStarts, 'gaussian', 120);  % 120 подобрано на глазок



% теперь у нас есть фича-вектор A. 
%% Всякие графики фиксаций
% 
% figure;
% plot(A, 'LineWidth', 2); % , 'Color', 'k'
% hold on
% % plot(fixsStarts, 'LineWidth', 2); 
% xlim([0 45000]);  
% 
% 
% xlabel('Frames (30 per second)');
% ylabel('Time between fixations (seconds)');
% [ ~ , name , ~ ] = fileparts( vidPath );
% legend(name(5:9));
% 
% 
% figure;
% fs = 30;
% spectrogram(A,256,250,[],fs,'yaxis')
% 
% return



%% Сохранение результатов  sLengths и fTime
outPath = strcat(alphaDataPath, '+fixsac2_features.csv'); 
fprintf('writing results to %s\n',  outPath);

writeHeader(outPath);
S = [];
for i = 1:n
    S(i, 1) = frameNo(i);
    S(i, 2) = A(i);    
end 
   
writematrix(S, outPath, 'Delimiter', ';', 'WriteMode', 'append');
end

function writeHeader(path)
  S = ["FrameNo", "fixation_time"];
  writematrix(S, path, 'Delimiter', ';');
end
