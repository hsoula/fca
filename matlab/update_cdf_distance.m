function cdf_matrix =  update_cdf_distance(cdf_matrix, surrogate_data_set, train_list, idx_train1, idx_train2)

ntrain = length(train_list);
nsurrogate = length(surrogate_data_set);
cdf_matrix(:,idx_train2, :) = [];
cdf_matrix(:,:, idx_train2) = [];
for i=1:nsurrogate    
    update_distance_data_set(cdf_matrix(i, :, :), surrogate_data_set{i}, idx_train1);
  %  cdf_matrix(i, :, : ) =  cm
end
for i=1:ntrain
    for j=(i+1):ntrain
        cdf_matrix(:, i, j) = sort(cdf_matrix(:, i, j));
        cdf_matrix(:, j, i) = sort(cdf_matrix(:, j, i));
    end
end