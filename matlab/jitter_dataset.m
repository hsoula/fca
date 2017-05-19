function new_set = jitter_dataset(train_list, sigma)
n_train = length(train_list);
new_set = {};
for i=1:n_train
    new_set{i} = jitter_spike_train(train_list{i}, sigma);
end
