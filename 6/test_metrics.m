%% Выводим выровненные графики и RR-интервалы
close all


%% Загружаем

S = '22ST1';
S_fileName = S;
rrPath = ['D:\Projects\USC#', S, '.csv=RR.csv'];
featurePath = ['D:\Projects\USC#', S, '_encoded_0000.mp4+mv_features.csv'];
ReultsPathCSV = ['D:\Projects\USC#', S, '-correlation.csv'];

RR = readRR(rrPath);
[allM, allV] = readMV(featurePath);

[SKO, levDist, xCoeff, shiftCoeff] = seriesCorrelator(RR, allM);
shiftCoeff = readCorrelation(ReultsPathCSV);

S = [S, ';', num2str(SKO), ';', num2str(levDist), ';', num2str(xCoeff), ';', num2str(shiftCoeff)]

figure;
X = allV;
if shiftCoeff > 0 
    RRshift = shiftSignal(RR, shiftCoeff);
    Xshift = X;
else
    RRshift = RR;
    Xshift = shiftSignal(X, -shiftCoeff);
end    

RRshift = smoothdata(RRshift, 'gaussian', 150);
Xshift = smoothdata(Xshift,  'gaussian', 700);
plot(RRshift*2.4-1, 'LineWidth', 2);
hold on
plot(Xshift, 'LineWidth', 2); 
title(S_fileName);

legend('RR', 'Обобщённое ускорение');
ylim([0 1.6]);
xlim([0 44000]);


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

function writeLine(S, path)
    fid = fopen(path, 'wt');
    S = [S, '\n'];       
    fprintf(fid, S);
    fclose(fid);
end

function shift = readCorrelation(path)
    csvOpts = delimitedTextImportOptions('Delimiter', ';'); 
    SC = readmatrix(path, csvOpts);   
    
    shift = str2double(SC(5));
%     disp(SC); 
end