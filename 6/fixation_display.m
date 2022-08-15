% ПЕРЕПРОВЕРИТЬ заполнение фича-векторов во всех
% calculateFixationsFeatures

% Эта штука читает видеофайл, который предварительно обработан. Затем
% просто демонстрирует все фиксации, так чтобы соседние фиксации
% отображались разным цветом.

% Здесь реализован правильный алгоритм выделения фиксаций.


disp('press CTRL + C to interrupt'); 

            
vidPath = 'G:\Projects\Vids\USC#01ST7.mp4';
% vidPath = 'G:\Projects\temp2\scene-test.mp4';
alphaPath = strcat(vidPath, '+alpha.csv');


[XX, YY, fX, fY] = read_alpha(alphaPath);
% fixTimeline = Fixations_Timeline(XX, YY);
fixTimeline = Fixations_Timeline_PlusHead(XX, YY, fX, fY);
v = VideoReader(vidPath);
figure;

% for kk = 1:20
%     videoFrame = readFrame(v);
% end
arrColors = {'cyan','yellow', 'blue', 'green', 'red', 'magenta', 'white'};  
bboxes(3) = 64;
bboxes(4) = 64;
frameNo = 20;


for kk = 1:frameNo
    videoFrame = readFrame(v);
end

while hasFrame(v)
    videoFrame = readFrame(v);
    frameNo = frameNo + 1;
    I = videoFrame;

    bboxes(1) = XX(frameNo)-32;
    bboxes(2) = YY(frameNo)-32;
    
    position = bboxes;
    
    if fixTimeline(frameNo) > 0
      col = arrColors(mod(fixTimeline(frameNo), 7) + 1);   
      I = insertObjectAnnotation(I, 'rectangle', position(1:size(position, 1), :),...
                                 strcat('fixation_ ', string(fixTimeline(frameNo))),...
                                 'TextBoxOpacity', 0.8, 'FontSize', 12, 'Color', col);
    end
 
    imshow(I);
    pause(1/15);
end



function [eye_X, eye_Y, head_X, head_Y] = read_alpha(path)
    csvPath = path;

    csvOpts = delimitedTextImportOptions('Delimiter', ';'); 

    S = readmatrix(csvPath, csvOpts);
    [n, ~] = size(S);
    eye_X(n-1) = 0.0; eye_Y(n-1) = 0.0; head_X(n-1) = 0.0; head_Y(n-1) = 0.0; frameNo(n-1) = 1;
    for i = 2:n
        frameNo(i-1) = round(str2double(S(i, 1))); 
        eye_X(i-1) = str2double(S(i, 2)); % координаты зрачка
        eye_Y(i-1) = str2double(S(i, 3));
        head_X(i-1) = str2double(S(i, 20)); % смещение головы. Внимание: относительная величина!
        head_Y(i-1) = str2double(S(i, 21));
    end
 
end


function [fixTimeline] = Fixations_Timeline_PlusHead(XX, YY, fX, fY)
  Fixations = XX*0;
  headX = fX * 0;
  headY = fY * 0;
  n = length(XX);
  
  for i = 2:n
    headX(i) = headX(i-1) + fX(i)*2;
    headY(i) = headY(i-1) + fY(i)*0.58;
  end
  
  dists = Fixations*0;
  
  for i = 1:n-1
      if XX(i) + YY(i) < 2
          Fixations(i) = 0;
          continue;
      end
      
      x = XX(i) - headX(i);
      y = YY(i) - headY(i);
      x_next = XX(i+1) - headX(i+1);
      y_next = YY(i+1) - headY(i+1); 
      
      
%       distance = hypot(XX(i+1) - XX(i), YY(i+1) - YY(i));
      distance = hypot(x_next - x, y_next - y);
      
      dists(i) = distance;
      if distance < 13 %%%%%%%%%%%%%%%%%%%%% 13
          Fixations(i) = 1;
          Fixations(i+1) = 1;
      end
  end
  
  for i = 2:n-1  % заполняем короткие разрывы фиксаций
      if (Fixations(i) == 0)&&(Fixations(i-1) == 1)&&(Fixations(i+1) == 1)
        Fixations(i) = 1;
      end
  end

  for i = 2:n-2
      if (Fixations(i) == 0) && (Fixations(i+1) == 0) &&(Fixations(i-1) == 1)&&(Fixations(i+2) == 1)
        Fixations(i)   = 1;
        Fixations(i+1) = 1;
      end
  end

  for i = 2:n-1  % удаляем слишком короткие фиксации
      if (Fixations(i) == 1)&&(Fixations(i-1) == 0)&&(Fixations(i+1) == 0)
        Fixations(i) = 0;
      end
  end

  allFixs = [];  % структура, хранящая начало и конец фиксации
  afN = 0;

  Fixations(1) = 0;
  Fixations(n) = 0;
  
  for i = 1:n-2
      if (Fixations(i) == 0) && (Fixations(i+1) == 1)
          afN = afN + 1;
          allFixs(afN, 1) = i+1; %#ok<AGROW>
          for j = i+1:n-1
              if (Fixations(j) == 1)  && (Fixations(j+1) == 0)
                  allFixs(afN, 2) = j;
                  break
              end

              if j == n
                  allFixs(afN, 2) = j;
              end
          end
      end
  end
  % теперь у нас afN фиксаций, каждая из которых начинается в allFixs(i, 1) и
  % заканчивается в allFixs(i, 2).


  % время между фиксациями
  fixTimeline = XX * 0;
  
  for i = 1 : afN-1       
      fixTimeline(allFixs(i, 1) : allFixs(i, 2)) = i; % заполняем
  end
  
  n = min(n, allFixs(afN, 2));
  fixTimeline(allFixs(afN, 1):n) = afN;
  
%    disp(sum(dists(1:45)));
end

function [fixTimeline] = Fixations_Timeline(XX, YY)
  Fixations = XX*0;
  n = length(XX);
  for i = 1:n-1
      if XX(i) + YY(i) < 2
          Fixations(i) = 0;
          continue;
      end
      distance = hypot(XX(i+1) - XX(i), YY(i+1) - YY(i));
      if distance < 3 
          Fixations(i) = 1;
          Fixations(i+1) = 1;
      end
  end

  for i = 2:n-1  % заполняем короткие разрывы фиксаций
      if (Fixations(i) == 0)&&(Fixations(i-1) == 1)&&(Fixations(i+1) == 1)
        Fixations(i) = 1;
      end
  end

  for i = 2:n-2
      if (Fixations(i) == 0) && (Fixations(i+1) == 0) &&(Fixations(i-1) == 1)&&(Fixations(i+2) == 1)
        Fixations(i)   = 1;
        Fixations(i+1) = 1;
      end
  end

  for i = 2:n-1  % удаляем слишком короткие фиксации
      if (Fixations(i) == 1)&&(Fixations(i-1) == 0)&&(Fixations(i+1) == 0)
        Fixations(i) = 0;
      end
  end

  allFixs = [];  % структура, хранящая начало и конец фиксации
  afN = 0;
  
  Fixations(1) = 0;
  Fixations(n) = 0;
  
  for i = 1:n-2
      if (Fixations(i) == 0) && (Fixations(i+1) == 1)
          afN = afN + 1;
          allFixs(afN, 1) = i+1; %#ok<AGROW>
          for j = i+1:n-1
              if (Fixations(j) == 1)  && (Fixations(j+1) == 0)
                  allFixs(afN, 2) = j;
                  break
              end

              if j == n
                  allFixs(afN, 2) = j;
              end
          end
      end
  end
  % теперь у нас afN фиксаций, каждая из которых начинается в allFixs(i, 1) и
  % заканчивается в allFixs(i, 2).


  % время между фиксациями
  fixTimeline = XX * 0;
  
  for i = 1 : afN-1       
      fixTimeline(allFixs(i, 1) : allFixs(i, 2)) = i; % заполняем
  end
  
  n = min(n, allFixs(afN, 2));
  fixTimeline(allFixs(afN, 1):n) = afN;
end