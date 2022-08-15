%% Читаем файл csv 

vidPath = 'C:\Projects\DBs\007+.avi';
csvPath = strcat(vidPath, '+alpha.csv');

csvOpts = delimitedTextImportOptions('Delimiter', ';'); 

S = readmatrix(csvPath, csvOpts);
[n, ~] = size(S);
XX = []; YY = []; fX = []; fY = []; frameNo = [];
for i = 2:n
    frameNo(i) = round(str2double(S(i, 1))); 
    XX(i) = str2double(S(i, 2)); % координаты зрачка
    YY(i) = str2double(S(i, 3));
    fX(i) = str2double(S(i, 20)); % смещение головы. Внимание: относительная величина!
    fY(i) = str2double(S(i, 21));
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

for i = 1:n-1
    if (Fixations(i) == 0) && (Fixations(i+1) == 1)
        afN = afN + 1;
        allFixs(afN, 1) = i+1;
        for j = i+1:n
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
% for i = 1:30
%     for j = 1:30
%         D(i, j) = dmn(i, j, XX, YY, T);
%     end
% end
 
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
avgD = avgD + diag(diag(ones(120)))*200;  % чтобы можно было поэлементно делить

allV = XX*0;
allM = XX*0;

for t = 61 : n-62       
    [v, m] = featureVect(t, XX, YY, T, avgD);
    allV(t) = v;
    allM(t) = m;
end 

allV = allV*1000*1.4/8;  % примерно нормируем

% теперь у нас два фича-вектора: allV и allM

%% Сохранение результатов

outPath = strcat(vidPath, '+mv_features.csv'); 
writeMVFile(outPath);
for i = 1:n
    writeMVLine(outPath, frameNo(i), allM(i), allV(i));    
end




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

  