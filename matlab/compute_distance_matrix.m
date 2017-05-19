function distance_matrix = compute_distance_matrix(train_list)
%         Compute distance matrix for each pair of trains in train_list 
%     :param train_list: list of train in the in the form train[i] = T ith spike occurs at time T
%     :return: a len(train_list) square matrix with distance

ntrains = length(train_list);
distance_matrix = zeros(ntrains, ntrains);
for i=1:ntrains
    for j=(i+1):ntrains
        train1 = train_list{i};
        train2 = train_list{j};
        distance_matrix(i,j) = average_minimum_distance(train1, train2);
        distance_matrix(j,i) = distance_matrix(i,j);
    end
end
