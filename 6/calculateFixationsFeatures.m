function calculateFixationsFeatures(alphaDataPath)
% вычисляем время между фиксациями и длины отрезков перевода взгляда.
% Покамест только для взгляда. Значения выводим для каждого кадра,
% распространяя их на всю последующую фиксацию.

if nargin ~= 1      
  % для целей дебага
  vidPath = 'G:\Projects\temp\+alpha\USC#07ST3';
  alphaDataPath = 'G:\Projects\temp\+alpha\USC#07ST3.mp4+alpha.csv'; 
  disp('no file selected');
end

%% Читаем файл csv  
csvPath = strcat(alphaDataPath, '+alpha.csv');  % устаревший вариант
csvPath = alphaDataPath;                        % теперь передаём целиком имя файла с +alpha
alphaDataPath = char(alphaDataPath);
idx = strfind(alphaDataPath, '+alpha');  
outPath = strcat(alphaDataPath(1:idx(end)-5), '+fixsac_features.csv'); % путь для сохранения результирующего файла

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
    if XX(i) + YY(i) < 2
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
afN = 0;

for i = 1:n-2
    if (Fixations(i) == 0) && (Fixations(i+1) == 1)
        afN = afN + 1;
        allFixs(afN, 1) = i+1; %#ok<AGROW>
        for j = i+1:n-1
            if (Fixations(j) == 1)  && (Fixations(j+1) == 0)
                allFixs(afN, 2) = j;
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

%% Строим фича-векторы
 

% время между фиксациями
fTime = XX * 0;
for i = 1 : afN-1
    timeBetw = allFixs(i+1, 1) - allFixs(i, 2); % время между двумя фиксациями
    fTime(allFixs(i, 1):allFixs(i+1, 1)+1) = timeBetw; % заполняем
end
fTime(allFixs(afN, 1):n) = fTime(allFixs(afN, 1)-1);

% длины саккад
sLengths = Fixations * 0;
for i = 1 : afN-1
    timeStart = allFixs(i, 2);
    timeEnd = allFixs(i+1, 1);
    slen = hypot(XX(timeEnd)-XX(timeStart), YY(timeEnd)-YY(timeStart));
    timeS1 = allFixs(i, 1);
    sLengths(timeS1:timeEnd) = slen;
end
sLengths(allFixs(afN, 1):n) = sLengths(allFixs(afN, 1)-1);

% теперь у нас два фича-вектора: sLengths и fTime
%% Всякие графики фиксаций
% figure;
% plot(Fixations);
% xlim([0 35000]);  
% ylim([0 2]);
% xlabel('Frames (30 per second)');

% B = smoothdata(Fixations, 'gaussian', 120);
% figure;
% plot(B);
% xlim([0 45000]);  
% ylim([0 2]);
% xlabel('Frames (30 per second)');

% figure;
% 
% A = smoothdata(sLengths, 'gaussian', 320);
% B = smoothdata(fTime, 'gaussian', 320);
% plot(A, 'LineWidth', 2); % , 'Color', 'k'
% hold on
% plot(B, 'LineWidth', 2); 
% xlim([0 45000]);  
% % ylim([0.1 2.5]);
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
% figure;
% spectrogram(B,256,250,[],fs,'yaxis')



%% Сохранение результатов  sLengths и fTime

fprintf('writing results to %s\n',  outPath);

writeHeader(outPath);
S = [];
for i = 1:n
    S(i, 1) = frameNo(i);
    S(i, 2) = fTime(i); 
    S(i, 3) = sLengths(i);   
end 
   
writematrix(S, outPath, 'Delimiter', ';', 'WriteMode', 'append');
end

function writeHeader(path)
  S = ["FrameNo", "inter_fixation_time", "saccade_length"];
  writematrix(S, path, 'Delimiter', ';');
end
