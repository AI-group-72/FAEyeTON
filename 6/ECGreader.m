%% Читает формат ЭКГ и сохраняет с разбиением по времени кадра

ecgPath = 'D:\Projects\ECG_base\RAW_HRV_CSV\USC#07\';

ecgFile = 'USC#07ST1.csv';
ECG_Reader(ecgPath, ecgFile);

ecgFile = 'USC#07ST2.csv';
ECG_Reader(ecgPath, ecgFile);

ecgFile = 'USC#07ST3.csv';
ECG_Reader(ecgPath, ecgFile);

ecgFile = 'USC#07ST4.csv';
ECG_Reader(ecgPath, ecgFile);

ecgFile = 'USC#07ST5.csv';
ECG_Reader(ecgPath, ecgFile);

ecgFile = 'USC#07ST6.csv';
ECG_Reader(ecgPath, ecgFile);

ecgFile = 'USC#07ST7.csv';
ECG_Reader(ecgPath, ecgFile);

ecgFile = 'USC#07ST8.csv';
ECG_Reader(ecgPath, ecgFile);
 

function ECG_Reader(ecgPath, ecgFile)
csvPath = strcat(ecgPath, ecgFile);

csvOpts = delimitedTextImportOptions('Delimiter', ','); 

S = readmatrix(csvPath, csvOpts);
[n, ~] = size(S);
 

frameNo(n) = 0; realTm(n) = 0.0; realRR(n) = 0.0;

for i = 1:n    
    realTm(i) = str2double(S(i, 1))*1000;  
    realRR(i) = str2double(S(i, 2));  
end


tAccum = 0;
frameRR = [];
jRR = 1;

for i = 1:n-1
    tAccum = tAccum + realTm(i+1)-realTm(i);    
    while tAccum > 100/3
        tAccum = tAccum - 100/3;
        frameRR(jRR) = realRR(i);   %#ok<SAGROW>
        jRR = jRR + 1;
    end
end
frameRR(jRR) = realRR(n);

outFolder = 'D:\Projects\';
outPath = strcat(outFolder, ecgFile, '=RR.csv');

S = ["FrameNo", "RR_sec"];
writematrix(S, outPath, 'Delimiter', ';');
S = [];

for i = 1:jRR
    S(i, 1) = i;
    S(i, 2) = frameRR(i); 
end 
   
writematrix(S, outPath, 'Delimiter', ';', 'WriteMode', 'append');
end