% какие у нас есть фичи? Расстояние Журавлёва V и M, скорости по Х и Y,
% Фиксации-в-секунду, время между фиксациями, длины саккад, кривизна
% тракетории, карта расстояний для всего ролика. И каждое из этого в двух
% вариантах: для головы и взгляда.
% На данный момент обсчитаны для взгляда: расст. Журавлёва,
% фиксации-в-секунду, fixation_features и кривизна траектории. Осталось: 
% speed_features, full_path_Features, расстояние от центра кадра,
% средняя продолжительность фиксаций (а также её ст. отклонение)


featuresCalculate;

% перекидываем результаты в другую папку, а затем...

return
meaner2;


function rearranger

inFileName = 'G:\Projects\InterFixTime-features-file.csv';
outFileName = 'G:\Projects\InterFixTime-features-rearranged.csv';
csvOpts = delimitedTextImportOptions('Delimiter', ';'); 
SC = readmatrix(inFileName, csvOpts);
[nn, ~] = size(SC); 

allPts(1:23) = 0;
allData(1:23, 1:8, 1:3) = -100;
for i = 2:nn      
  charStr = char(SC(i, 1));
  pilot = str2num(string(charStr(37:38)));
  stage = str2num(string(charStr(41)));
  allPts(pilot) = allPts(pilot) + stage; 
  allData(pilot, stage, 1) = str2num(string(SC(i, 4)))*30;
  allData(pilot, stage, 2) = str2num(string(SC(i, 5)))*30;
  allData(pilot, stage, 3) = str2num(string(SC(i, 6)))*30;  
end    

S = ["Filename", "ST1-1", "ST1-2", "ST1-3", "ST2-1", "ST2-2", "ST2-3", "ST3-1", "ST3-2", "ST3-3", "ST4-1", "ST4-2", "ST4-3", "ST5-1", "ST5-2", "ST5-3", "ST6-1", "ST6-2", "ST6-3", "ST7-1", "ST7-2", "ST7-3", "ST8-1", "ST8-2", "ST8-3"];

writematrix(S, outFileName, 'Delimiter', ';', 'WriteMode', 'overwrite');

for i = 1:23
  if allPts(i) == 0 
    continue
  end
  
  fileN = strcat('USC#', string(i))
  S = [fileN];
  for j = 1:8
    for k = 1:3
      subs = string(allData(i, j, k));
      S = [S, subs];
    end
  end
  
  writematrix(S, outFileName, 'Delimiter', ';', 'WriteMode', 'append');
end

 
end


function featuresCalculate
% сначала обрабатываем и сохраняем фичи
% 1 расстояние Журавлёва V и M (обобщённое ускорение и обобщённая скорость), 
% 2 количество фиксаций в секунду, 
% 3 "кривизна" траектории,
% 4 скорости по вертикали и горизонтали,
% 5 время между фиксациями, 
% 6 длина отрезка перевода взгляда, 
% 7 карта расстояний для всего испытания (почти готова).
% 8 Расстояние от центра кадра до точки фиксации — это только для взгляда.

  folderName = "G:\Projects\temp\+alpha\";
  list = ls(folderName);
  list = list(3:end, :);
  
  parfor j = 1:length(list)
%   for j = 1:1
    filename = strcat(folderName, list(j,:));
%     calculateCurvatureFeatures(filename); % 3g
%    calculateFixationsFeatures(filename); % 5g 6g
    calculateFixationsFeatures1(filename); % 5g-1 6g-1    - исправленный
    disp(strcat(list(j,:), ' processed'));
  end
  
  disp('end');
end

function meaner2
  % делим каждый файл на
  % три части и усредняем по каждой трети.
%   folderName = "G:\Projects\CurvaturAp-Features\"; % 3g
  folderName = "G:\Projects\FixatiSac1-Features\";  
  outFileName = 'G:\Projects\Fix_SaccadesLength1-features-file.csv';  
  
  list = ls(folderName);
  list = list(3:end, :);     
  lenList = length(list);

  writeResultsHeader(outFileName);   
  
  parfor j = 1:lenList
    filename = strcat(folderName, list(j,:));
%     [X] = read_curvature_features(filename); % 3g
    
    [InterFixT, SacLen] = read_fixsac_features(filename);
    X = SacLen;
    
    [~, n] = size(X);
    n1 = floor(n*1/3);
    n2 = floor(n*2/3);
%     results(1) = mean(X(   1:n1));
%     results(2) = mean(X(n1+1:n2));
%     results(3) = mean(X(n2+1:end));
    results = [mean(X(   1:n1)), mean(X(n1+1:n2)), mean(X(n2+1:end))];
    writeResultsLine(outFileName, filename, results);
    
    disp(floor(j*100/lenList));
  end 
  
  inFileName1 = outFileName;
  outFileName2 = strcat(inFileName1, '-rearranged.csv');
%   'G:\Projects\InterFixTime-features-rearranged.csv';
  csvOpts = delimitedTextImportOptions('Delimiter', ';'); 
  SC = readmatrix(inFileName1, csvOpts);
  [nn, ~] = size(SC); 

  allPts(1:23) = 0;
  allData(1:23, 1:8, 1:3) = -100;
  for i = 2:nn      
    charStr = char(SC(i, 1));
    pilot = str2num(string(charStr(37:38)));
    stage = str2num(string(charStr(41)));
    allPts(pilot) = allPts(pilot) + stage; 
    allData(pilot, stage, 1) = str2num(string(SC(i, 4)));
    allData(pilot, stage, 2) = str2num(string(SC(i, 5)));
    allData(pilot, stage, 3) = str2num(string(SC(i, 6)));  
  end    

  S = ["Filename", "ST1-1", "ST1-2", "ST1-3", "ST2-1", "ST2-2", "ST2-3", "ST3-1", "ST3-2", "ST3-3", "ST4-1", "ST4-2", "ST4-3", "ST5-1", "ST5-2", "ST5-3", "ST6-1", "ST6-2", "ST6-3", "ST7-1", "ST7-2", "ST7-3", "ST8-1", "ST8-2", "ST8-3"];

  writematrix(S, outFileName2, 'Delimiter', ';', 'WriteMode', 'overwrite');

  for i = 1:23
    if allPts(i) == 0 
      continue
    end

    fileN = strcat('USC#', string(i))
    S = [fileN];
    for j = 1:8
      for k = 1:3
        subs = string(allData(i, j, k));
        S = [S, subs];
      end
    end

    writematrix(S, outFileName2, 'Delimiter', ';', 'WriteMode', 'append');
  end
end

function writeResultsHeader(path)
  S = ["Full Filename", "Pilot Num", "Stage Num", "mean 1", "mean 2", "mean 3"];

  writematrix(S, path, 'Delimiter', ';', 'WriteMode', 'overwrite');
end

function writeResultsLine(path, MVFileName, results)  
  charStr = char(MVFileName);
  PilotNo = string(charStr(37:38));
  StageNo = string(charStr(41));
  S = [MVFileName, PilotNo, StageNo];
  
  [~, n] = size(results);
  for i = 1:n
      S = [S, results(i)];  %#ok<AGROW>
  end 
  
  writematrix(S, path, 'Delimiter', ';', 'WriteMode', 'append');
end

function [allF] = read_curvature_features(featurePath)
  allF = read_fixation2_features(featurePath);
end

function [all1, all2] = read_fixsac_features(path)
  [all1, all2] = readMV(path);
end

function [allM, allV] = readMV(featurePath)
    csvOpts = delimitedTextImportOptions('Delimiter', ';'); 
    SC = readmatrix(featurePath, csvOpts);
    [nn, ~] = size(SC); 

    allM(nn-1) = 0.0; allV(nn-1) = 0.0;
    for i = 2:nn        
        allM(i-1) = str2double(SC(i, 2)); 
        allV(i-1) = str2double(SC(i, 3));  
    end    
    
    for i = 2:nn-1 % в паре файлов нашлись NaN, прямо на этапе чтения их затираем
      if isnan(allM(i))
        allM(i) = allM(i-1);
      end
      if isnan(allV(i))
        allV(i) = allV(i-1);
      end
    end
      
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