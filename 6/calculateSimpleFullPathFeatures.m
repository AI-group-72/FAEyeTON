% function calculateSimpleFullPathFeatures(vidPath)
% if nargin < 1
    disp('no file specified')
    vidPath = 'D:\Projects\USC#13ST3.mp4'; 
% end

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

%% Готовимся к вычисленниям расстояния Журавлёва 

T = XX*0;
for i = 1:n
    T(i) = tau(i, allFixs, afN);
end

%% Пример построения карты расстояний

% D = ones(30, 30)*0;
%  
% for i = 500:530
%     for j = 500:530
%         D(i-500, j-500) = dmn(i, j, XX, YY, T);
%     end
% end
% 
% figure; imshow(D, []);
% return;
 
%% Строим все возможные карты расстояний размером 120 х 120

% sumD = ones(120, 120)*0;
% for t = 61 : n-62     
%     sumD = sumD + dMap(t, XX, YY, T) / 27309;
% end 
% 
% avgD = sumD * 0.5 + flip(flip(sumD, 2)) * 0.5;
% save('allD.mat', 'avgD');

%% Построение фича-вектора файла



load('allD.mat', 'avgD');
avgD = interpolateDiag(avgD);
% figure;
% imshow(avgD, []);

n = floor(n/4)*4;
n_interp = 1:4:n; %linspace(1, n, newn);
n_orig = 1:n; % linspace(1, n, n);

XX = XX(1:n);
YY = YY(1:n);
T = T(1:n);

tic
XXi = interp1(n_orig, XX, n_interp, 'pchip');
YYi = interp1(n_orig, YY, n_interp, 'pchip');
TTi = interp1(n_orig, T, n_interp, 'pchip');

n = floor(n/4);
result = ones(n, n)*0;
for i = 1:n  
  for j = i:n
      result(i, j) = dmn(i, j, XXi, YYi, TTi);
      result(j, i) =  result(i, j);
  end
end  

% avgD = imresize(avgD, [n n]);

result = interpolateDiag(result);  
% result = result./avgD;

toc

figure;
imshow(result, []);

%% Сохранение результатов

% outPath2 = strcat(vidPath, '+fullGaze_features.mat'); 
outPath2 = 'C:\Projects\MatTall\result.mat'; 
disp('writing results to ');
disp(outPath2);

save(outPath2, 'result');
% writematrix(result, outPath, 'Delimiter', ';');
% end <<<<<<<<<<<<<<<<<<<<<<<<<
return

%% функция вычисления того самого члена в интеграле (3)
function result = tau(t, allFixs, afN) 
  alpha = 8;
  beta = 0.0005;
  result = 0;
  for i = 1:afN
      tj1 = allFixs(i, 1);
      tj2 = allFixs(i, 2);
      tmid = (tj1 + tj2)/2;
      tdif = tj2 - tj1;
      result = result + exp(- beta * (t - tmid)^2/tdif^2);
  end
  result = alpha * result;
end

%% построение карты расстояний размером 120 х 120
function result = dMap(t, XX, YY, T)
  result = ones(120, 120)*0;
  for i = -59:60  % 60 = 2 секунды
      for j = -59:60
          result(i+60, j+60) = dmn(t + i, t + j, XX, YY, T);
      end
  end
end

%% сжимание карты расстояний до дисперсии и матожидания
function [v, m] = featureVect(t, XX, YY, T, avgD)
  curD = dMap(t, XX, YY, T)./avgD;
  curD = interpolateDiag(curD);
  m = mean(mean(curD));
  v = var(reshape(curD, [], 1));
end

  