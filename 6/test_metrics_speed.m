function test_metrics_speed(S, mode)

if nargin < 1
    S = '12ST2';
    mode = 1; 
end

%% Загружаем


rrPath = strcat('D:\Projects\USC#', S, '.csv=RR.csv');
featurePath = strcat('D:\Projects\USC#', S, '_encoded_0000.mp4+speed_features.csv');
ReultsPathCSV = strcat('D:\Projects\USC#', S, '-correlation.csv');

RR = readRR(rrPath);
[all1, all2, all3, all4] = readMV(featurePath);
shift = readCorrelation(ReultsPathCSV);

if mode == 1
    X = all1;
elseif mode == 2
    X = all2;
elseif mode == 3
    X = all3;
elseif mode == 4
    X = all4;
end

[SKO, levDist, SKOder, levDistDer] = seriesCorMetrics(RR, X, shift);

Simpostor = ["10ST1", "10ST2", "10ST3", "10ST4", ...
    "10ST5", "10ST6", "10ST7", "10ST8", "10ST9", ...
    "11ST1", "11ST2", "11ST3", "11ST4", "11ST5", ...
    "11ST6", "11ST7", "11ST8", "11ST9", ...
    "14ST1", "14ST2"];
for j = 1:18 
    rrPath = strcat('D:\Projects\USC#', Simpostor(j), '.csv=RR.csv');
    
    RR = readRR(rrPath);
    [iSKO(j), ilevDist(j), iSKOder(j), ilevDistDer(j)] = seriesCorMetrics(RR, X, shift);
end

count_iSKO = sum(iSKO < SKO);
count_iLevDist = sum(ilevDist < levDist);
count_iSKOder = sum(iSKOder < SKOder);
count_levDistDer = sum(ilevDistDer < levDistDer); 

S = [S, ';', num2str(SKO), ';', num2str(levDist),  ';', num2str(SKOder),  ';', num2str(levDistDer),'; impostor:;', ...
            num2str(count_iSKO), ';', num2str(count_iLevDist), ';', num2str(count_iSKOder), ';', num2str(count_levDistDer)];

if mode == 1
    writeLine(S, 'D:\Projects\Results\metrics-Speed_GazeX.csv');
elseif mode == 2
    writeLine(S, 'D:\Projects\Results\metrics-Speed_GazeY.csv');
elseif mode == 3    
    writeLine(S, 'D:\Projects\Results\metrics-Speed_HeadX.csv');
elseif mode == 4
    writeLine(S, 'D:\Projects\Results\metrics-Speed_HeadY.csv');    
end

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

function [all1, all2, all3, all4] = readMV(featurePath)
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

function shift = readCorrelation(path)
    csvOpts = delimitedTextImportOptions('Delimiter', ';'); 
    SC = readmatrix(path, csvOpts);   
    
    shift = str2double(SC(5));
%     disp(SC); 
end

function writeLine(S, path)
    fid = fopen(path, 'at');
    S = strjoin(S, '');     
    fprintf(fid, S);
    fprintf(fid, '\n');
    fclose(fid);
end