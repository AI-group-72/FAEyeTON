% ПЕРЕПРОВЕРИТЬ заполнение фича-векторов во всех
% calculateFixationsFeatures!!

% По группе из 7 фиксаций
% Считаем между началами фиксаций время.
% Среднее и СКО. 
% Для этого же отрезка считаем, скажем, кривизну.
% Выводим на плоскость.
 
clear all
            
vidPath = 'G:\Projects\Vids\USC#01ST8.mp4';
stageName = vidPath(24:26);
alphaPath = strcat(vidPath, '+alpha.csv');
curvaPath = strcat(alphaPath, '+curva_features.csv');


[XX, YY, fX, fY] = read_alpha(alphaPath);
[curv_Features] = read_curvature_features(curvaPath);

[AllFixations, afN] = Fixations_Timeline(XX, YY);
n = length(XX);


parseA(7) = 0; diffs(6) = 0;
for i = 1 : afN-6
  for j = 1 : 7  % заполняем массив для обработки
    parseA(j) = AllFixations(i+j-1, 1);
  end
  
  for j = 1 : 6
    diffs(j) = parseA(j+1) - parseA(j);
  end
  
  m_freq = mean(diffs);
  sko_freq = std(diffs);
  
  curvFragment = curv_Features(parseA(1) : parseA(7));
  m_curv = mean(curvFragment);
  
  result_pairs(i, 1) = m_freq;
  result_pairs(i, 2) = sko_freq;
  result_pairs(i, 3) = m_curv;
end 

I(1:2560, 1:3840) = 0;

for i = 1 : afN-6
  X = round(result_pairs(i, 1) * 3); % короткая сторона - частота
  Y = round(result_pairs(i, 3) * 1500); % длинная сторона - кривизна
  
  X = max(1, X); X = min(X, 2560);
  Y = max(1, Y); Y = min(Y, 3840);
  
  I(X, Y) = I(X, Y) + 9;
end

h = fspecial('disk', 12);
I = imfilter(I, h);
I = imgaussfilt(I, 7);

figure;
imshow(I, []);

xlabel('кривизна →') 
ylabel('← частота смены фиксаций') 
title(stageName);


return


%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

function [eye_X, eye_Y, head_X, head_Y] = read_alpha(path)
    csvPath = path;

    csvOpts = delimitedTextImportOptions('Delimiter', ';'); 

    S = readmatrix(csvPath, csvOpts);
    [n, ~] = size(S);
    eye_X(n-1) = 0.0; eye_Y(n-1) = 0.0; head_X(n-1) = 0.0; head_Y(n-1) = 0.0; frameNo(n-1) = 1;
    for i = 2:n
        frameNo(i-1) = round(str2double(S(i, 1))); 
        eye_X(i-1) = str2double(S(i, 2)); % координаты зрачка
        eye_Y(i-1) = str2double(S(i, 3));
        head_X(i-1) = str2double(S(i, 20)); % смещение головы. Внимание: относительная величина!
        head_Y(i-1) = str2double(S(i, 21));
    end
 
end

function [allFixs, afN] = Fixations_Timeline(XX, YY)
  Fixations = XX*0;
  n = length(XX);
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

 
end


function [allF] = read_curvature_features(featurePath)
  allF = read_fixation2_features(featurePath);
end

function [allF] = read_fixation2_features(featurePath)
    csvOpts = delimitedTextImportOptions('Delimiter', ';'); 
    SC = readmatrix(featurePath, csvOpts);
    [nn, ~] = size(SC); 

    allF(nn-1) = 0.0;  
    for i = 2:nn        
        allF(i-1) = str2double(SC(i, 2)); 
      
    end    
    
    for i = 2:nn-1 % в паре файлов нашлись NaN, прямо на этапе чтения их затираем
      if isnan(allF(i))
        allF(i) = allF(i-1);
      end 
    end
end