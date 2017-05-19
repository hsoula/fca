function p = scaled_value(cdf, v, ci)

n = length(cdf);
n2 = n/2.0;
nci = n * ci;  
nv = length(find(cdf<v));
p = max(0, (n2- nv)/(n2 - nci));

end
