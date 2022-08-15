function test_metrics_head(S, mode)

if nargin < 1
    S = '12ST2';
    mode = 1;
    SS = ["22ST1", "22ST2", "22ST3", "22ST4", "22ST5", "22ST6", ...
          "12ST1", "12ST2", "12ST3", "12ST4", "12ST5", "12ST6",  "12ST7", "12ST8", ...
          "13ST3", "13ST4", "13ST5", "13ST6", "13ST8"];
end

%% Загружаем


rrPath = strcat('D:\Projects\USC#', S, '.csv=RR.csv');
featurePath = strcat('D:\Projects\USC#', S, '_encoded_0000.mp4+head_mv_features.csv');
ReultsPathCSV = strcat('D:\Projects\USC#', S, '-correlation.csv');

RR = readRR(rrPath);
[allM, allV] = readMV(featurePath);
shift = readCorrelation(ReultsPathCSV);

if mode == 1
    X = allM;
else
    X = allV;
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
    writeLine(S, 'D:\Projects\Results\metrics-Head_M.csv');
else
    writeLine(S, 'D:\Projects\Results\metrics-Head_V.csv');
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

function [allM, allV] = readMV(featurePath)
    csvOpts = delimitedTextImportOptions('Delimiter', ';'); 
    SC = readmatrix(featurePath, csvOpts);
    [nn, ~] = size(SC); 

    allM(nn) = 0.0; allV(nn) = 0.0;
    for i = 2:nn        
        allM(i-1) = str2double(SC(i, 2)); 
        allV(i-1) = str2double(SC(i, 3)); 
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