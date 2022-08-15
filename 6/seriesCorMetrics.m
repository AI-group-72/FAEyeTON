function [SKO, levDist, SKOder, levDistDer] = seriesCorMetrics(RR, X, shift)
% строим корреляцию между данными RR-интервалов и метриками взгляда
% X - метрика.
%% фиксируем RR и X
[~, nn] = size(X);
[~, n] = size(RR);

RR(1:10) = 0;
RR(n-10:n) = 0;
X(1:10) = 0;
X(nn-10:nn) = 0;


%% сдвигаем

if shift > 0 % метрика запаздывает относительно RR
    RR = shiftSignal(RR, shift);
else
    X =  shiftSignal(X, -shift);
end

RR = smoothdata(RR, 'gaussian', 110);
X = smoothdata(X, 'gaussian', 100);

[A, B] = alignsignals(RR+1, X+1, 20);


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
n = kk - ii + 1;

%% находим производные

Ader = A*0;
for i = 1+1:n-1
    Ader(i) = (A(i+1) - A(i-1))/2;
end
Ader(1) = Ader(2);
Ader(n) = Ader(n-1);

Bder = B * 0;
for j = 1+1:n-1
    Bder(j) = (B(j+1) - B(j-1))/2;
end
Bder(1) = Bder(2);
Bder(n) = Bder(n-1);

% подблюриваем их
Ader = smoothdata(Ader, 'gaussian', 30);
Bder = smoothdata(Bder, 'gaussian', 30);

% подравниваем
[Ader2, Bder2] = alignsignals(Ader, Bder, 20);
[~, nn1] = size(Ader2);
[~, nn2] = size(Bder2);
nn = min(nn1, nn2);
Ader2 = Ader2(1:nn);
Bder2 = Bder2(1:nn);

%% вычисляем СКО

A = A - mean(A);
A = A/sqrt(var(A));

B = B - mean(B);
B = B/sqrt(var(B));

Ader2 = Ader2 - mean(Ader2);
Ader2 = Ader2/sqrt(var(Ader2));

Bder2 = Bder2 - mean(Bder2);
Bder2 = Bder2/sqrt(var(Bder2));

SKO = rms(A-B);
SKOder = rms(Ader2 - Bder2); 

% figure;
% plot(Ader2);
% hold on;
% plot(Bder2);

%% Расстояние Левенштейна для оригинальных сигналов
smallA = imresize(A, 0.01);
smallB = imresize(B, 0.01);
sA = toABCString(smallA);   
sB = toABCString(smallB);

vvv = editDistance(sA, sB); 

[~, nn] = size(sB);

levDist = vvv/nn;

%% Расстояние Левенштейна для производных
smallA = imresize(Ader, 0.01);
smallB = imresize(Bder, 0.01);
sA = toABCString(smallA);   
sB = toABCString(smallB);

vvv = editDistance(sA, sB); 

[~, nn] = size(sB);

levDistDer = vvv/nn;

 
end

function sA = toABCString(A)
[~, n] = size(A);
A = A - mean(A);
threshUp = sqrt(var(A))/2;
numPositives = sum((A - threshUp) > 0);
while numPositives > n/3
    threshUp = threshUp+0.07;
    numPositives = sum((A - threshUp) > 0);
end

threshDown = sqrt(var(A))/2;
A = -A;
numNegatives = sum((A - threshDown) > 0);
while numNegatives > n/3
    threshDown = threshDown+0.07;
    numNegatives = sum((A - threshDown) > 0);
end

A = -A;
threshDown = -threshDown;

sA = '';
  for i = 1:n
    if A(i) <= threshDown
        sA = [sA, 'A'];
    elseif A(i) >= threshUp
        sA = [sA, 'C'];
    else
        sA = [sA, 'B'];
    end
  end
end
