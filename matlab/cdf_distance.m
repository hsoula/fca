function cdf_matrix = cdf_distance(train_list, surrogate_data_set)


ntrain = length(train_list);
nsurrogate = length(surrogate_data_set);

cdf_matrix = zeros(nsurrogate, ntrain, ntrain);
for i=1:nsurrogate
    surrogate_distance_matrix = compute_distance_matrix(surrogate_data_set{i});
    cdf_matrix(i, :, :) = surrogate_distance_matrix;
end

for i=1:ntrain
    for j=(i+1):ntrain
        cdf_matrix(:, i, j) = sort(cdf_matrix(:, i, j));
        cdf_matrix(:, j, i) = sort(cdf_matrix(:, j, i));
    end
end
