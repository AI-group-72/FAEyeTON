% clc
% close all

vids = ["G:\Projects\RR\USC#11ST1.csv=RR.csv",  ...
        "G:\Projects\RR\USC#11ST2.csv=RR.csv",   ...
    	"G:\Projects\RR\USC#11ST3.csv=RR.csv",  ...
    	"G:\Projects\RR\USC#11ST4.csv=RR.csv", ...
        "G:\Projects\RR\USC#11ST5.csv=RR.csv", ...
        "G:\Projects\RR\USC#11ST6.csv=RR.csv"];
    
AN1 = readRR(vids(1));
AN2 = readRR(vids(2));
AN3 = readRR(vids(3));
AN4 = readRR(vids(4));
AN5 = readRR(vids(5));
AN6 = readRR(vids(6));

[~, n1] = size(AN1);
[~, n2] = size(AN2);
[~, n3] = size(AN3);
[~, n4] = size(AN4);
[~, n5] = size(AN5);
[~, n6] = size(AN6);

ns = [n1, n2, n3, n4, n5, n6];

nN = max(ns);

clear Data
Data(1:nN, 1:6) = NaN;

j = 1;
AN = AN1;
n = n1;
for i = 1:n
    Data(i, j) = AN(i);
end

j = 2;
AN = AN2;
n = n2;
for i = 1:n
    Data(i, j) = AN(i);
end

j = 3;
AN = AN3;
n = n3;
for i = 1:n
    Data(i, j) = AN(i);
end

j = 4;
AN = AN4;
n = n4;
for i = 1:n
    Data(i, j) = AN(i);
end

j = 5;
AN = AN5;
n = n5;
for i = 1:n
    Data(i, j) = AN(i);
end

j    = 6;
AN = AN6;
n   = n6;
for i = 1:n
    Data(i, j) = AN(i);
end

for i = 1:nN
    for j = 1:6
        if Data(i, j) == 0
            Data(i, j) = NaN;
        end
    end
end

[p,tbl,stats] = anova1(Data, {'11ST1', '11ST2', '11ST3', '11ST4', '11ST5', '11ST6'});

%%

% clc
% close all

vids = ["G:\Projects\USC#11ST1.mp4+mv_features.csv",  ...
        "G:\Projects\USC#11ST2.mp4+mv_features.csv",   ...
    	"G:\Projects\USC#11ST3.mp4+mv_features.csv",  ...
    	"G:\Projects\USC#11ST4.mp4+mv_features.csv", ...
        "G:\Projects\USC#11ST5.mp4+mv_features.csv", ...
        "G:\Projects\USC#11ST6.mp4+mv_features.csv"];
    
[AN1M, AN1V] = readMV(vids(1));
[AN2M, AN2V] = readMV(vids(2));
[AN3M, AN3V] = readMV(vids(3));
[AN4M, AN4V] = readMV(vids(4));
[AN5M, AN5V] = readMV(vids(5));
[AN6M, AN6V] = readMV(vids(6));

[~, n1] = size(AN1M);
[~, n2] = size(AN2M);
[~, n3] = size(AN3M);
[~, n4] = size(AN4M);
[~, n5] = size(AN5M);
[~, n6] = size(AN6M);

ns = [n1, n2, n3, n4, n5, n6];

nN = max(ns);

Data(1:nN, 1:6) = NaN;

j = 1;
AN = AN1M;
n = n1;
for i = 1:n
    Data(i, j) = AN(i);
end

j = 2;
AN = AN2M;
n = n2;
for i = 1:n
    Data(i, j) = AN(i);
end

j = 3;
AN = AN3M;
n = n3;
for i = 1:n
    Data(i, j) = AN(i);
end

j = 4;
AN = AN4M;
n = n4;
for i = 1:n
    Data(i, j) = AN(i);
end

j    = 5;
AN = AN5M;
n   = n5;
for i = 1:n
    Data(i, j) = AN(i);
end

j    = 6;
AN = AN6M;
n   = n6;
for i = 1:n
    Data(i, j) = AN(i);
end

for i = 1:nN
    for j = 1:6
        if Data(i, j) == 0
            Data(i, j) = NaN;
        end
    end
end

[p,tbl,stats] = anova1(Data, {'11ST1', '11ST2', '11ST3', '11ST4', '11ST5', '11ST6'});


%%

function  [allM, allV] = head_mv_features(path)
  [allM, allV] = readMV(path);
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

function RR = readRR(rrPath)
    csvOpts = delimitedTextImportOptions('Delimiter', ';'); 
    S = readmatrix(rrPath, csvOpts);
    [n, ~] = size(S); 

    RR(n) = 0.0; 
    for i = 2:n        
        RR(i-1) = str2double(S(i, 2));  
    end
end
