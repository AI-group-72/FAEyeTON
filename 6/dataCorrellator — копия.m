% строим корреляцию между данными РР-интервалов и метриками взгляда

%% Загружаем
rrPath = 'D:\Projects\USC#12ST3.csv=RR.csv';
featurePath = 'D:\Projects\USC#12ST3_encoded_0000.mp4+mv_features.csv';

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
X = X(i+1:j-1);
%% фильтруем

RRheavyS = smoothdata(RR-mean(RR), 'gaussian', 19000);
XheavyS = smoothdata(X-mean(X), 'gaussian', 19000); 

% figure;
% plot(RRheavyS, 'LineWidth', 3);
% hold on
% plot(XheavyS, 'LineWidth', 3);
% hold off;
% legend('RR','метрикасд');


%% масштабируем
RR = RR - RRheavyS;
X  = X - XheavyS;

meanRR = mean(RR);

RR = RR  / meanRR - 1;
RR = smoothdata(RR, 'gaussian', 300);
vRR = var(RR);
RR = RR / sqrt( vRR);

meanX = mean(X);
X = X / meanX - 1;
vX = var(X);
X = X /sqrt(vX);



[A, B] = alignsignals(RRsm, X, 3333);

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
smallA = imresize(RRsm, 0.01);
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

return


X = X  / meanX - 1;



t21 = finddelay(RR, X, 3000)
hold off

figure
[c,lags] = xcorr(RR, X);
stem(lags,c)

function sA = toABCString(A)
[~, n] = size(A);
sA = '';
  for i = 1:n
    if A(i) < -0.667
        sA = [sA, 'A'];
    elseif (-0.667 <= A(i)) && (A(i) <0.667)
        sA = [sA, 'B'];
    else
        sA = [sA, 'C'];
    end
  end
end
