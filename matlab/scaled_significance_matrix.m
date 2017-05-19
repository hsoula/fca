function scale_matrix = scaled_significance_matrix (current_train_list, cdf_matrix, distance_matrix, ci)

[nsurrogate, ntrain, ~] = size(cdf_matrix);
scale_matrix = zeros(ntrain, ntrain);

for i=1:ntrain
    for j=(i+1):ntrain
        scale_matrix(i, j) = scaled_value(cdf_matrix(:, i, j), distance_matrix(i, j), ci);
    end
end

