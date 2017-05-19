function surrogate_data_set = update_surrogate_dataset(surrogate_data_set, sigma, merged_train, idx_train1, idx_train2)
nsurrogate = length(surrogate_data_set);
for i=1:nsurrogate     
    surrogate_data_set{i}(idx_train2) =  [];
    surrogate_data_set{i}{idx_train1} =  jitter_spike_train(merged_train, sigma);
end
