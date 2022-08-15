function B = shiftSignal(A, shift)
  [~, n] = size(A);
  newN = n + shift;
  B(1:newN) = 0;
 
  B(shift+1:newN) = A(:);
end