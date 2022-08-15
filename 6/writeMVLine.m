function writeMVLine(path, frameNo, m, v)
  S = [frameNo, m, v];
   
  writematrix(S, path, 'Delimiter', ';', 'WriteMode', 'append');
end