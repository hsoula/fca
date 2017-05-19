function train_list = create_uncorrelated_spike_trains(ntrains, lambda, tmax)
train_list = {};
for i=1:ntrains;
    train = cumsum(-log(rand(1,round(tmax/lambda)))/lambda);
    train(train> tmax) = [];
    train_list{i} = train;
end
