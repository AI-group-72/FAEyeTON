function res = interpolateDiag(A)
  [n, ~] = size(A);
  res = A;
  for i = 2:n-1
      res(i, i) = (res(i-1, i) + res(i, i+1))/2;
  end
  res(1,1) = res(1,2);
  res(n,n) = res(n,n-1);
end