function surrogate_trains = create_surrogate_dataset(train_list, nsurrogate, sigma)
surrogate_trains = {};
for i=1:nsurrogate
    surrogate_trains{i} = jitter_dataset(train_list, sigma);
end


