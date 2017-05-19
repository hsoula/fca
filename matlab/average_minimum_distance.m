function d = average_minimum_distance(train1, train2)
d1 = 0.0;
for s=train1;
    d1 = d1 + min(abs(s - train2));
end
d2 = 0.0;
for s=train2
    d2 = d2 + min(abs(s - train1));
end
d = 0.5 * (d1 + d2);
