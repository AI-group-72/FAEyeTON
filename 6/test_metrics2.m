%% 123
function test_metrics2(S)

if nargin < 1
    S = '12ST1';
end

%% Загружаем


rrPath = ['D:\Projects\USC#', S, '.csv=RR.csv'];
featurePath = ['D:\Projects\USC#', S, '_encoded_0000.mp4+mv_features.csv'];
ReultsPathCSV = ['D:\Projects\USC#', S, '-correlation.csv'];

RR = readRR(rrPath);
[allM, allV] = readMV(featurePath);
shift = readCorrelation(ReultsPathCSV);

X = allV;

[SKO, levDist, SKOder, levDistDer] = seriesCorMetrics(RR, X, shift);

if S(1) == '1' 
    Simpostor = ['22ST6', '22ST1', '22ST2', '22ST3'];
else
    Simpostor = ['12ST8', '12ST6', '12ST2', '12ST3'];
end
rrPath = ['D:\Projects\USC#', Simpostor(1), '.csv=RR.csv'];
RR = readRR(rrPath);
[iSKO1, ilevDist1, iSKOder1, ilevDistDer1] = seriesCorMetrics(RR, X, shift);

rrPath = ['D:\Projects\USC#', Simpostor(2), '.csv=RR.csv'];
RR = readRR(rrPath);
[iSKO2, ilevDist2, iSKOder2, ilevDistDer2] = seriesCorMetrics(RR, X, shift);

rrPath = ['D:\Projects\USC#', Simpostor(3), '.csv=RR.csv'];
RR = readRR(rrPath);
[iSKO3, ilevDist3, iSKOder3, ilevDistDer3] = seriesCorMetrics(RR, X, shift);

rrPath = ['D:\Projects\USC#', Simpostor(4), '.csv=RR.csv'];
RR = readRR(rrPath);
[iSKO4, ilevDist4, iSKOder4, ilevDistDer4] = seriesCorMetrics(RR, X, shift);

iSKO = (iSKO4+iSKO3+iSKO2+iSKO1)/4;
ilevDist = (ilevDist4+ilevDist3+ilevDist2+ilevDist1)/4;
iSKOder = (iSKOder4+iSKOder3+iSKOder2+iSKOder1)/4;
ilevDistDer = (ilevDistDer4+ilevDistDer3+ilevDistDer2+ilevDistDer1)/4;

S = [S, ';', num2str(SKO), ';', num2str(levDist), ';', num2str(SKOder), ...
        ';', num2str(levDistDer),'; impostor:;',  num2str(iSKO), ';', ...
             num2str(ilevDist), ';', num2str(iSKOder), ';', num2str(ilevDistDer)];

writeLine(S, 'D:\Projects\CSVs\metricsV.csv');

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
    S = [S, '\n'];       
    fprintf(fid, S);
    fclose(fid);
end