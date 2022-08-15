% строим корреляцию между данными РР-интервалов и метриками взгляда
close all
%% Загружаем
rrPath = 'D:\Projects\USC#22ST1.csv=RR.csv';
featurePath = 'D:\Projects\USC#22ST1_encoded_0000.mp4+mv_features.csv';

csvOpts = delimitedTextImportOptions('Delimiter', ';'); 
S = readmatrix(rrPath, csvOpts);
[n, ~] = size(S); 

RR(n) = 0.0; 
for i = 2:n        
    RR(i-1) = str2double(S(i, 2));  
end
n = n-1;

SC = readmatrix(featurePath, csvOpts);
[nn, ~] = size(SC); 

allM(nn) = 0.0; allV(nn) = 0.0;
for i = 2:nn        
    allM(i-1) = str2double(SC(i, 2)); 
    allV(i-1) = str2double(SC(i, 3)); 
end

nn = nn-1;

%% коррелировать будем только с одним каналом
X = allM;

%% срезаем стартовые и финальные нули
i = 1;
while X(i) == 0
    i = i+1;
end
j = nn;
while X(j) == 0
    j = j - 1;
end
RR = RR(10:n-10); [~, n] = size(RR);
X = X(i+10:j-10);
%% фильтруем

RRheavyS = smoothdata(RR-mean(RR), 'gaussian', 19000);
XheavyS = smoothdata(X-mean(X), 'gaussian', 19000); 

RR = RR - RRheavyS;
X  = X - XheavyS;

RR = smoothdata(RR, 'gaussian', 150);

% figure;
% plot(RRheavyS, 'LineWidth', 3);
% hold on
% plot(XheavyS, 'LineWidth', 3);
% hold off;
% legend('RR','метрикасд');

%% строим производную

Rdif = RR*0;
for i = 1+1:n-1
    Rdif(i) = (RR(i+1) - RR(i-1))/2;
end
Rdif(1) = Rdif(2);
Rdif(n) = Rdif(n-1);

[~, nn] = size(X);

Xdif = X * 0;
for j = 1+1:nn-1
    Xdif(j) = (X(j+1) - X(j-1))/2;
end
Xdif(1) = Xdif(2);
Xdif(nn) = Xdif(nn-1);

RR = Rdif;
X = Xdif;


%% масштабируем


meanRR = mean(RR);

RR = RR  / meanRR - 1;
RR = RR  / meanRR ;
RR = smoothdata(RR, 'gaussian', 110);
vRR = var(RR);
RR = RR / sqrt( vRR);
RR = RR + 1;

meanX = mean(X);
X = X / meanX - 1;
X = X / meanX ;
X = smoothdata(X, 'gaussian', 100);
vX = var(X);
X = X /sqrt(vX);
X = X + 1;

[A, B] = alignsignals(RR+1, X+1, 840);
t21 = finddelay(RR+1, X+1, 840);
A = A-1;
B = B-1;

figure
plot(A,'LineWidth', 2); 
hold on
% plot(X, 'LineWidth', 2);  % plot(X, 'LineWidth', 2); 
plot(B, 'LineWidth', 2); 
legend('RR','матожидание расстояния Журавлёва');

%% выравнивание размерности
i = 1;
while A(i) == 0
    i = i+1;
end
j = 1;
while B(j) == 0
    j = j+1;
end

ii = max(i, j);



[~, n] = size(A);
[~, nn] = size(B);

k = n;
while A(k) == 0
    k = k - 1;
end

l = nn;
while B(l) == 0
    l = l - 1;
end

kk = min(k ,l);

A = A(ii:kk);
B = B(ii:kk);

%% вычисляем СКО

vvv = rms(A-B)


 
%% Расстояние Левенштейна
smallA = imresize(RR, 0.01);
smallB = imresize(X, 0.01);
sA = toABCString(smallA);
sB = toABCString(smallB);


tic
vvv = editDistance(sA, sB);
toc
[~, n] = size(sA);
[~, nn] = size(sB);
2*vvv/(n+nn)


randomX = (rand(1, nn) - 0.5)*2;
sR = toABCString(randomX);
vvv = editDistance(sA, sR);
2*vvv/(n+nn)



t21 = finddelay(RR, X, 3000);
hold off

figure
[c,lags] = xcorr(A, B);
[~, nnn] = size(lags);
ccoeff = c(round(nnn/2))

stem(lags,c)

function sA = toABCString(A)
[~, n] = size(A);
sA = '';
  for i = 1:n
    Ai = A(i) - 1;
    if Ai < -0.667
        sA = [sA, 'A'];
    elseif (-0.667 <= Ai) && (Ai <0.667)
        sA = [sA, 'B'];
    else
        sA = [sA, 'C'];
    end
  end
end
