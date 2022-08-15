function [i, j, angle] = coordsByCorrelation3(Imain, Ipart, scale)
  original = rgb2gray(Imain);
  distorted = rgb2gray(Ipart);
  
  ptsOriginal  = detectSURFFeatures(original);
  ptsDistorted = detectSURFFeatures(distorted);
  [featuresOriginal,validPtsOriginal] = extractFeatures(original,ptsOriginal);
  [featuresDistorted,validPtsDistorted] = extractFeatures(distorted,ptsDistorted);
  
  index_pairs = matchFeatures(featuresOriginal,featuresDistorted);
  matchedPtsOriginal  = validPtsOriginal(index_pairs(:,1));
  matchedPtsDistorted = validPtsDistorted(index_pairs(:,2));
  
  if (matchedPtsOriginal.Count < 3) || (matchedPtsDistorted.Count < 3)
    disp('None matched');
    i = 4242;
    j = -666;
    angle = 0;
    return
  end
  
  try
    [tform, ~] = estimateGeometricTransform2D(matchedPtsDistorted,matchedPtsOriginal,'affine');
  catch
    disp('None matched again');
    i = 4242;
    j = -666;
    angle = 0;
    return
  end  
  
  i = round(tform.T(3, 2)/scale, 1);
  j = round(tform.T(3, 1)/scale, 1);
  
  u = [0 1]; 
  v = [0 0]; 
  [x, y] = transformPointsForward(tform, u, v); 
  dx = x(2) - x(1); 
  dy = y(2) - y(1); 
  angle = (180/pi) * atan2(dy, dx); % в градусах
  angle = round(angle, 1);
end