%% функция вычисления интеграла (3)
function result = dmn(m, n, X, Y, T) 
  result = 0;
  if m == n
      return
  end
  if m > n
      k = m;
      m = n;
      n = k;
  end
  
  tsum = 0;
  for i = m+1:n
      tsum = tsum + T(i);
  end
  xsum = X(n) - X(m);
  ysum = Y(n) - Y(m);
  
  if (X(n) < 1) || (X(m) < 1) || isnan(X(n)) || isnan(X(m))
      xsum = 0;
  end
  if (Y(n) < 1) || (Y(m) < 1) || isnan(Y(n)) || isnan(Y(m))
      ysum = 0;
  end
  result = sqrt(xsum^2 + ysum^2 + tsum^2);
end