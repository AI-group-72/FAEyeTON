% 
% 
% function rearranger
% 
% inFileName = 'G:\Projects\temp\Fix2-features-file.csv';
% outFileName = 'G:\Projects\temp\Fix2-features-rearranged.csv';
% csvOpts = delimitedTextImportOptions('Delimiter', ';'); 
% SC = readmatrix(inFileName, csvOpts);
% [nn, ~] = size(SC); 
% 
% allPts(1:23) = 0;
% allData(1:23, 1:8, 1:3) = -100;
% for i = 2:nn      
%   charStr = char(SC(i, 1));
%   pilot = str2num(string(charStr(37:38)));
%   stage = str2num(string(charStr(41)));
%   allPts(pilot) = allPts(pilot) + stage; 
%   allData(pilot, stage, 1) = str2num(string(SC(i, 4)))*30/2;
%   allData(pilot, stage, 2) = str2num(string(SC(i, 5)))*30/2;
%   allData(pilot, stage, 3) = str2num(string(SC(i, 6)))*30/2;  
% end    
% 
% S = ["Filename", "ST1-1", "ST1-2", "ST1-3", "ST2-1", "ST2-2", "ST2-3", "ST3-1", "ST3-2", "ST3-3", "ST4-1", "ST4-2", "ST4-3", "ST5-1", "ST5-2", "ST5-3", "ST6-1", "ST6-2", "ST6-3", "ST7-1", "ST7-2", "ST7-3", "ST8-1", "ST8-2", "ST8-3"];
% 
% writematrix(S, outFileName, 'Delimiter', ';', 'WriteMode', 'overwrite');
% 
% for i = 1:23
%   if allPts(i) == 0 
%     continue
%   end
%   
%   fileN = strcat('USC#', string(i))
%   S = [fileN];
%   for j = 1:8
%     for k = 1:3
%       subs = string(allData(i, j, k));
%       S = [S, subs];
%     end
%   end
%   
%   writematrix(S, outFileName, 'Delimiter', ';', 'WriteMode', 'append');
% end
% 
% 
% end
% 
% 
% function meaner
%   folderName = "G:\Projects\temp\+alpha\";
%   list = ls(folderName);
%   list = list(3:end, :);
%    
%   
%   outFileName = 'G:\Projects\M-features-file.csv';
%   writeResultsHeader(outFileName);  
%   parfor j = 1:length(list)
%     filename = strcat(folderName, list(j,:));
%     [allM, allV] = readMV(filename);
%     X = allM;
%     [~, n] = size(X);
%     n1 = floor(n*1/3);
%     n2 = floor(n*2/3);
% %     results(1) = mean(X(   1:n1));
% %     results(2) = mean(X(n1+1:n2));
% %     results(3) = mean(X(n2+1:end));
%     results = [mean(X(   1:n1)), mean(X(n1+1:n2)), mean(X(n2+1:end))];
%     writeResultsLine(outFileName, filename, results);
%     
%     disp(floor(j*50/length(list)));
%   end
%   
%   
%   outFileName = 'G:\Projects\V-features-file.csv';
%   writeResultsHeader(outFileName);  
%   parfor j = 1:length(list) 
%     filename = strcat(folderName, list(j,:));
%     [allM, allV] = readMV(filename);
%     X = allV;
%     [~, n] = size(X);
%     n1 = floor(n*1/3);
%     n2 = floor(n*2/3);
% %     results(1) = mean(X(   1:n1));
% %     results(2) = mean(X(n1+1:n2));
% %     results(3) = mean(X(n2+1:end));
%     results = [mean(X(   1:n1)), mean(X(n1+1:n2)), mean(X(n2+1:end))];
%     writeResultsLine(outFileName, filename, results);
%     
%     disp(50 + floor(j*50/length(list)));
%   end  
% end
% 
% function featuresCalculate
% % сначала обрабатываем и сохраняем фичи,
%   folderName = "G:\Projects\temp\+alpha\";
%   list = ls(folderName);
%   list = list(3:end, :);
%   
%   parfor j = 1:length(list)
%     filename = strcat(folderName, list(j,:));
%     calculateFixationsFeatures2(filename);
%     disp(strcat(list(j,:), ' processed'));
%   end
%   
%   disp('end');
% end
% 
% function meaner2
%   % делим каждый файл на
%   % три части и усредняем по каждой трети.
%   folderName = "G:\Projects\Fixations2-Features\";
%   list = ls(folderName);
%   list = list(3:end, :);
%    
%   
%   outFileName = 'G:\Projects\Fix2-features-file.csv';
%   writeResultsHeader(outFileName);  
%   
%   lenList = length(list);
%   parfor j = 1:lenList
%     filename = strcat(folderName, list(j,:));
%     [X] = read_fixation2_features(filename);
%     
%     [~, n] = size(X);
%     n1 = floor(n*1/3);
%     n2 = floor(n*2/3);
% %     results(1) = mean(X(   1:n1));
% %     results(2) = mean(X(n1+1:n2));
% %     results(3) = mean(X(n2+1:end));
%     results = [mean(X(   1:n1)), mean(X(n1+1:n2)), mean(X(n2+1:end))];
%     writeResultsLine(outFileName, filename, results);
%     
%     disp(floor(j*100/lenList));
%   end 
% end

function writeResultsHeader(path)
  S = ["Full Filename", "Pilot Num", "Stage Num", "mean 1", "mean 2", "mean 3"];

  writematrix(S, path, 'Delimiter', ';', 'WriteMode', 'overwrite');
end

function writeResultsLine(path, MVFileName, results)  
  charStr = char(MVFileName);
  PilotNo = string(charStr(29:30));
  StageNo = string(charStr(33));
  S = [MVFileName, PilotNo, StageNo];
  
  [~, n] = size(results);
  for i = 1:n
      S = [S, results(i)];  %#ok<AGROW>
  end 
  
  writematrix(S, path, 'Delimiter', ';', 'WriteMode', 'append');
end

function [all1, all2, all3, all4] = read_speed_features(path)
  [all1, all2, all3, all4] = readMV2(path);
end

function [all1, all2] = read_fixsac_features(path)
  [all1, all2] = readMV(path);
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

function [allF] = read_curvature_features(featurePath)
  allF = read_fixation2_features(featurePath);
end

function  [allM, allV] = head_mv_features(path)
  [allM, allV] = readMV(path);
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

function [all1, all2, all3, all4] = readMV2(featurePath)
    csvOpts = delimitedTextImportOptions('Delimiter', ';'); 
    SC = readmatrix(featurePath, csvOpts);
    [nn, ~] = size(SC); 

    all1(nn) = 0.0; all2(nn) = 0.0;
    all3(nn) = 0.0; all4(nn) = 0.0;
    for i = 2:nn        
        all1(i-1) = str2double(SC(i, 2)); 
        all2(i-1) = str2double(SC(i, 3)); 
        all3(i-1) = str2double(SC(i, 4)); 
        all4(i-1) = str2double(SC(i, 5));         
    end
end

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

    n = n-1; % поправка на заголовок файла 
end



function RR = readRR(rrPath)
    csvOpts = delimitedTextImportOptions('Delimiter', ';'); 
    S = readmatrix(rrPath, csvOpts);
    [n, ~] = size(S); 

    RR(n) = 0.0; 
    for i = 2:n        
        RR(i-1) = str2double(S(i, 2));  
    end
end

function shift = readCorrelation(path)
    csvOpts = delimitedTextImportOptions('Delimiter', ';'); 
    SC = readmatrix(path, csvOpts);   
    
    shift = str2double(SC(5)); 
end

