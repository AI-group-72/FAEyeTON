function writeMVFile(path)
  S = ["FrameNo", "Featuremap_Mean", "Featuremap_Variance"];
  writematrix(S, path, 'Delimiter', ';');
end