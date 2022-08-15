function writeNewLineLonger(path, NumOfGears, frameNo, eyeX, eyeY, AllGears, frameShiftX, frameShiftY, alpha)
  S = [frameNo, eyeX, eyeY];
  
  for i = 1:NumOfGears
      S = [S, AllGears(i, :)];  %#ok<AGROW>
  end
  
  S = [S, frameShiftX, frameShiftY, alpha];
  writematrix(S, path, 'Delimiter', ';', 'WriteMode', 'append');
end