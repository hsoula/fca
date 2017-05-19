function train = jitter_spike_train(original_train, sigma)
%  Compute new spike trains jitterd by gaussian (centered) noise with sd  sigma
%         train should be in the form train[i] = T ith spike occurs at time T
%     :param train:
%     :param sigma:
%     :return: new spike trains - with same number of spike len = len(train)

nspikes = length(original_train);
train = sort(original_train  +  sigma * randn(1, nspikes));

