function showSimpleFeatures(vidPath, mode)
if nargin < 1
    vidPath = 'D:\Projects\USC#12ST3_encoded_0000.mp4';   
    mode = 1;
end
%% Читаем файл csv 

if mode == 1
    csvPath = strcat(vidPath, '+mv_features.csv'); 
    disp('gaze mode');
elseif mode == 2
    csvPath = strcat(vidPath, '+head_mv_features.csv'); 
    disp('head mode');
else
    disp('mode not specified');
    return
end

csvOpts = delimitedTextImportOptions('Delimiter', ';'); 

S = readmatrix(csvPath, csvOpts);
[n, ~] = size(S);

frameNo(n-1) = 0; allM(n-1) = 0.0; allV(n-1) = 0.0;

for i = 2:n
    frameNo(i-1) = round(str2double(S(i, 1))); 
    allM(i-1) = str2double(S(i, 2)); %  матожидание и дисперсия расстояния Журавлёва
    allV(i-1) = str2double(S(i, 3));  
end

%% Масштабируем
if mode == 2
    allV = allV * 2.4;
end

%% Выводим
figure;
plot(allM, 'LineWidth', 2); 

hold on
plot(allV, 'LineWidth', 2); 
hold off

xlim([0 45000]);  % до 43591 у двадцать второго
ylim([0 2]);
xlabel('Frames (30 per second)')

[ ~ , name , ~ ] = fileparts( vidPath );
legend(name(5:9));

figure;

fs = 30;
pwelch(allM, fs)
legend(name(5:9));

ylim([-50 10]);

% fs = 30;
% spectrogram(allV,256,250,[],fs,'yaxis')


end