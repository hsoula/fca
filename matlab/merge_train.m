function train = merge_train(train1, train2) 
% create a merged train from the two spike trains

train = [train1, train2];
train = sort(train);
