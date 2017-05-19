function distance_matrix = update_distance_data_set(distance_matrix, train_list, idx_train)
%   
%         update the distance matrix for a pair a train assuming the train list contains new (with the merged train)
%         at position idx_train1 - we remove row and column idx_train2
%     :param train_list: list of train in the in the form train[i] = T ith spike occurs at time T
%     :return: a len(train_list) square matrix with distance


ntrain = length(train_list);
merged_train  = train_list{idx_train};
for ix=1:ntrain    
    train2 = train_list{ix};
    d = average_minimum_distance(merged_train, train2);
    distance_matrix(ix, idx_train) = d;
    distance_matrix(idx_train, ix) = d;
end




