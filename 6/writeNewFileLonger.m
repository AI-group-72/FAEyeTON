function writeNewFileLonger(path, NumOfGears)
  S = ["FrameNo", "eye_X", "eye_Y"];
  
  for i = 1:NumOfGears
      S1 = "FlightInstr" + string(i) + "_X";
      S2 = "FlightInstr" + string(i) + "_Y";
      S3 = "FlightInstr" + string(i) + "_W";
      S4 = "FlightInstr" + string(i) + "_H";
      
      S = [S, S1, S2, S3, S4]; %#ok<AGROW>
  end
  
  S = [S, "FrameShift_X", "frameShift_Y", "frameRotation_deg"];
  writematrix(S, path, 'Delimiter', ';');
end