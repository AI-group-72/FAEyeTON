function [SKO, levDist, xCoeff, shiftCoeff] = seriesCorrelator(RR, X, shift)
% строим корреляцию между данными RR-интервалов и метриками взгляда
% X - метрика.
%% фиксируем RR и X
[~, nn] = size(X);
[~, n] = size(RR);

tempRR = RR; tempX = X;
RR(1:10) = 0;
RR(n-10:n) = 0;
X(1:10) = 0;
X(nn-10:nn) = 0;
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

i = 1;
while RR(i) == 0
    i = i+1;
end
j = n;
while RR(j) == 0
    j = j - 1;
end
RR = RR(i+1:j-1);

[~, nn] = size(X);
[~, n] = size(RR);
%% находим стационарную компоненту и вычитаем её

RRheavyS = smoothdata(RR-mean(RR), 'gaussian', 19000);
XheavyS = smoothdata(X-mean(X), 'gaussian', 19000); 

RR = RR - RRheavyS;
X  = X - XheavyS;

%% масштабируем, подблюриваем



meanRR = mean(RR);
RR = RR  / meanRR - 1;
RR = smoothdata(RR, 'gaussian', 110);
vRR = var(RR);
RR = RR / sqrt( vRR);

meanX = mean(X);
X = X / meanX - 1;
X = smoothdata(X, 'gaussian', 100);
vX = var(X);
X = X /sqrt(vX);

% tempRR = tempRR - smoothdata(tempRR-mean(tempRR), 'gaussian', 19000);
% tempRR = tempRR/meanRR - 1;
% tempRR = smoothdata(tempRR, 'gaussian', 110);
% tempRR = tempRR/sqrt(vRR);
% figure;
% plot(RR);
% hold on
% plot(tempRR);
% legend('RR', 'tempRR');
  


%% находим сдвиг через анализ производных

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

% добавим вторую производную

Rdif2 = Rdif*0;
Xdif2 = Xdif*0;

for i = 1+1:n-1
    Rdif2(i) = (Rdif(i+1) - Rdif(i-1))/2;
end
Rdif2(1) = Rdif2(2);
Rdif2(n) = Rdif2(n-1);

for j = 1+1:nn-1
    Xdif2(j) = (Xdif(j+1) - Xdif(j-1))/2;
end
Xdif2(1) = Xdif2(2);
Xdif2(nn) = Xdif2(nn-1);

% Xdif = Xdif2;
% Rdif = Rdif2;
% пробуем полусумму производных
Xdif = Xdif/sqrt(var(Xdif));
Xdif2 = Xdif2/sqrt(var(Xdif2));

Rdif = Rdif/sqrt(var(Rdif));
Rdif2 = Rdif2/sqrt(var(Rdif2));

Xdif = Xdif + Xdif2;
Rdif = Rdif + Rdif2;
%


i = 1;
while Rdif(i) == 0
    i = i+1;
end
j = 1;
while Xdif(j) == 0
    j = j+1;
end
ii = max(i, j);

k = n;
while Rdif(k) == 0
    k = k - 1;
end

l = nn;
while Xdif(l) == 0
    l = l - 1;
end

kk = min(k ,l);

Rdif = Rdif(ii:kk);
Xdif = Xdif(ii:kk);

Rdif = Rdif  /  mean(Rdif) - 1;
Rdif = smoothdata(Rdif, 'gaussian', 300);

Rdif = Rdif / sqrt( var(Rdif));
Rdif = Rdif + 1;

Xdif = Xdif / mean(Xdif) - 1;
Xdif = smoothdata(Xdif, 'gaussian', 300);
Xdif = Xdif /sqrt(var(Xdif));
Xdif = Xdif + 1;

maxSC = 38;
shiftCoeff = finddelay(Rdif, Xdif, maxSC );
%  shiftCoeff = finddelay(RR, X, maxSC );
[tempRdif, tempXdif] = alignsignals(Rdif, Xdif, maxSC );
figure;
plot(tempRdif);
hold on;
plot(tempXdif);

%% сдвигаем
if nargin == 2    
    shift = shiftCoeff;
end

if shift > 0 % метрика запаздывает относительно RR
    RR = shiftSignal(RR, shift);
%     disp('shift+');
else
    X =  shiftSignal(X, -shift);
%     disp('shift-');
end
A = RR; B = X; 

%% выравнивание размерности
[~,  n] = size(A);
[~, nn] = size(B);

i = 1;
while A(i) == 0
    i = i+1;
end
j = 1;
while B(j) == 0
    j = j+1;
end
ii = max(i, j);

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

SKO = rms(A-B);
% C = shiftSignal(A, 300);
% [~, tn] = size(C);
% C = C(1:tn-300);
% SKO2 = rms(C-B)
 
%% Расстояние Левенштейна 
smallA = imresize(A, 0.01);
smallB = imresize(B, 0.01);
sA = toABCString(smallA);   
sB = toABCString(smallB);

vvv = editDistance(sA, sB); 

[~, nn] = size(sB);

levDist = vvv/nn;

%% находим степень кросс-корреляции, чтобы потом хотя бы её знак знать

[c,lags] = xcorr(A, B);
[~, nnn] = size(lags);
xCoeff = c(round(nnn/2)); 

%% коэффициент сдвига находим через корреляцию с исходными данными


% tempRR = tempRR - smoothdata(tempRR-mean(tempRR), 'gaussian', 19000);



% tempRR = tempRR  / meanRR - 1;
% tempRR = smoothdata(tempRR, 'gaussian', 110);
% tempRR = tempRR / sqrt(vRR);

% tempRR = tempRR - smoothdata(tempRR-mean(tempRR), 'gaussian', 19000);
% tempRR = tempRR/meanRR - 1;
% tempRR = smoothdata(tempRR, 'gaussian', 110);
% tempRR = tempRR/sqrt(vRR);
% 
% 
% % aX = tempX;
% tempX = tempX - smoothdata(tempX-mean(tempX), 'gaussian', 19000);
% tempX = tempX / mean(tempX) - 1;
% tempX = smoothdata(tempX, 'gaussian', 100);
% tempX = tempX /sqrt(vX);
% 
% tRR = finddelay(tempRR, RR);
% tX =  finddelay(tempX,  X);
% 
% % shiftCoeff = tX - tRR;
% 
% figure;
% plot(X);
% hold on
% plot(circshift(tempX, tX));
% legend('X', 'shifted aX');

% figure;
% plot(RR);
% hold on
% plot(circshift(tempRR, tRR));
% legend('RR', 'shifted tempRR');
end

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
