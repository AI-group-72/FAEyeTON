function showGazeFeatures(csvPath, channels)
if nargin < 1
    csvPath = 'D:\Projects\USC#12ST3_encoded_0000.mp4+speed_features.csv';  
    channels = 1;
end
%% Читаем файл csv 

csvOpts = delimitedTextImportOptions('Delimiter', ';'); 

S = readmatrix(csvPath, csvOpts);
[n, ~] = size(S);

frameNo(n-1) = 0; allChannels(1:channels, n-1) = 0.0; 

for i = 2:n
    frameNo(i-1) = round(str2double(S(i, 1))); 
    for j = 1:channels
        allChannels(j, i-1) = str2double(S(i, j+1));
    end
end

%% Масштабируем
% if mode == 2
%     allV = allV * 2.4;
% end

%% Выводим
figure;
hold on
for j = 1:channels
    plot(allChannels(j,:), 'LineWidth', 2); 
end
hold off

xlim([0 45000]);  % до 43591 у двадцать второго
xlabel('Frames (30 per second)')

[ ~ , name , ~ ] = fileparts( csvPath );
legend(name(5:9));

% figure
% fs = 30;
% spectrogram(allChannels(1,:),256,250,[],fs,'yaxis')


end