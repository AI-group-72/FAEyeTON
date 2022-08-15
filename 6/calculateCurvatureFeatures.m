function calculateCurvatureFeatures(alphaDataPath)
% Это метрика, равная отношению длины трека за некоторое время 
% к расстоянию между начальной и конечной точками трека. Этакая обобщённая
% кривизна.

if nargin ~= 1      
  % для целей дебага
  alphaDataPath = 'G:\Projects\temp\+alpha\USC#01ST1.mp4+alpha.csv'; 
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

%% Рассчитываем путь взгляда между двумя кадрами
dPath = XX * 0;
for i = 1:n-1 
  dPath(i) = hypot(XX(i+1) - XX(i), YY(i+1) - YY(i));
end
dPath(n) = dPath(n-1);

% окно положим в 120 отсчётов
t = 120;

fullPath_t = dPath*0;
for i = 1:n-t
  fullPath_t(i+t/2) = hypot(XX(i+t) - XX(i), YY(i+t) - YY(i));
end

% экстраполируем первые и последние t/2 отсчётов
Bshort = smoothdata(fullPath_t(t/2:n-t/2), 'gaussian', 120);
NCap = 1:t;
bat1 = t/2+1:t;
Bstart = interp1(bat1, Bshort(1:t/2), NCap, 'linear', 'extrap');
Bstart = max(Bstart, 0); 

Bshort = fliplr(Bshort);
Bend = interp1(bat1, Bshort(1:t/2), NCap, 'linear', 'extrap');
Bend = max(Bend, 0);
Bend = fliplr(Bend);
Bshort = fliplr(Bshort);

fullPath_t(1:t/2) = Bstart(1:t/2);
fullPath_t(n-t/2+1:n) = Bend(1:t/2);
   

%% Строим фича-вектор
% фильтруем гауссианой

A = smoothdata(dPath, 'gaussian', 22);
B = smoothdata(fullPath_t, 'gaussian', 22);  % 22 подобрано на глазок

for i = 1:n 
  A(i) = (A(i) + 0.01)/(B(i) + 0.01);
end

% теперь у нас есть фича-вектор A. 
%% Всякие графики  
% 
% 
% figure(1);
% plot(NCap, Bend, '--r')
% hold on
% plot(bat1, Bshort(1:60))
% hold off
% grid
% return

% A = smoothdata(dPath/mean(dPath),           'gaussian', 15);
% B = smoothdata(fullPath_t/mean(fullPath_t), 'gaussian', 15);
% figure
% plot(A);
% hold on
% plot(B);
% legend('dPath', 'fullPath_t');
% return;

% figure
% plot(A);
% 
% figure;
% fs = 30;
% spectrogram(A,256,250,[],fs,'yaxis')
% 
% return



%% Сохранение результатов  фича-вектора
outPath = strcat(alphaDataPath, '+curva_features.csv'); 
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
  S = ["FrameNo", "curvature_approx"];
  writematrix(S, path, 'Delimiter', ';');
end

