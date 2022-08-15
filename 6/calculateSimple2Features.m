function calculateSimple2Features(vidPath)
% фичи из метрики Журавлёва для движений головы

if nargin < 1      
    vidPath = 'D:\Projects\USC#13ST3_encoded_0000.mp4'; 
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

%% Переводим значения из относительных в абсолютные
headX = fX * 0;
headY = fY * 0;

for i = 2:n
    headX(i) = headX(i-1) + fX(i);
    headY(i) = headY(i-1) + fY(i);
end    

%% Выделяем фиксации

Fixations = headX*0;
for i = 1:n-1
    distance = hypot(headX(i+1) - headX(i), headY(i+1) - headY(i));
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

T = headX*0;
for i = 1:n
    T(i) = tau(i, allFixs, afN);
end

%% Пример построения карты расстояний

% D = ones(120, 120)*0;
%  
% for i = 2500:2620
%     for j = 2500:2620
%         k = i + 1 - 2500;
%         l = j + 1 - 2500;
%         D(k, l) = dmn(i, j, headX, headY, T);
%     end
% end
% 
% figure; imshow(D, []);
% return;
 
%% Строим все возможные карты расстояний размером 120 х 120
% tic
% sumD = ones(120, 120)*0;
% k = 0;
% for t = 61 : n-62     
%     k = k + 1;
%     sumD = sumD + dMap(t, headX, headY, T) / 27000;
% end 
% 
% avgHeadD = sumD * 0.5 + flip(flip(sumD, 2)) * 0.5;
% avgHeadD = avgHeadD * (27000/k);
% save('allHeadD.mat', 'avgHeadD');
% toc
%% Построение фича-вектора файла

load('allHeadD.mat', 'avgHeadD');
avgHeadD = avgHeadD + diag(diag(ones(120)))*200;  % чтобы можно было поэлементно делить

allV = headX*0;
allM = headX*0;

for t = 61 : n-62       
    [v, m] = featureVect(t, headX, headY, T, avgHeadD);
    allV(t) = v;
    allM(t) = m;
end 

allV = (allV*1000*1.4/8);  % примерно нормируем

% теперь у нас два фича-вектора: allV и allM

%% Сохранение результатов

outPath = strcat(vidPath, '+head_mv_features.csv'); 
fprintf('writing results to %s\n',  outPath);

writeMVFile(outPath);
S = [];
for i = 1:n
    S(i, 1) = frameNo(i);
    S(i, 2) = allM(i); 
    S(i, 3) = allV(i); 
end 
   
writematrix(S, outPath, 'Delimiter', ';', 'WriteMode', 'append');

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
function result = dMap(t, headX, headY, T)
  result = ones(120, 120)*0;
  for i = -59:60  % 60 = 2 секунды
      for j = -59:60
          result(i+60, j+60) = dmn(t + i, t + j, headX, headY, T);
      end
  end
end

%% сжимание карты расстояний до дисперсии и матожидания
function [v, m] = featureVect(t, headX, headY, T, avgD)
  curD = dMap(t, headX, headY, T)./avgD;
  curD = interpolateDiag(curD);
  m = mean(mean(curD));
  v = var(reshape(curD, [], 1));
end

  