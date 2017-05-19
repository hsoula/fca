% test functional clustering 

s = RandStream('mcg16807','Seed',1);
RandStream.setGlobalStream(s);

ntrains = 20;
freq = 0.5;
ngroup  =  6;
low_sigma = 0.10;

train_list = create_uncorrelated_spike_trains(ntrains- ngroup, freq, 100);
for i=1:ngroup
    train_list{ntrains-ngroup +i} = jitter_spike_train(train_list{1}, low_sigma);
end
data_plot = [];
for i=1:ntrains
    tr = train_list{i};
    nr = length(tr);
    data_plot = [data_plot; [i * ones(nr,1), tr']];
end
figure(1);  plot(data_plot(:,2), data_plot(:,1), 'k+', 'MarkerSize', 14); drawnow;


distance_matrix = compute_distance_matrix(train_list);

figure(2); imagesc(distance_matrix); drawnow;


n_surrogate = 1000;
sigma = 1.0; 
early_stop = 0;
%[merge_history, current_cluster] = fca(train_list, n_surrogate, sigma, early_stop)

ci  = 0.05;
n_train = length(train_list);
current_train_list = train_list(:);
current_cluster = {};
for c=1:n_train
    current_cluster{c} = c;
end

merge_history = {};
nstep  = 1;

disp('creating surrogate data set');
surrogate_data_set = create_surrogate_dataset(train_list, n_surrogate, sigma);
disp('creating cdf matrix');
cdf_matrix = cdf_distance(train_list, surrogate_data_set);
disp('creating initial distance matrix')
distance_matrix = compute_distance_matrix(train_list);
done = 0;

disp('starting clustering')
while ~done
   
    disp('computing scale matrix');
    scale_matrix = scaled_significance_matrix (current_train_list, cdf_matrix, distance_matrix, ci);
    [max_scale, imax] = max(scale_matrix(:))
    if early_stop == 1 &  max_scale < 1.0
        done = 1;
    else
        [i,j] =  ind2sub(size(scale_matrix), imax);
        if i > j 
            a = i;
            i = j;
            j = a;
        end
        disp('merging')
        merge_history{nstep} =  [current_cluster(i), current_cluster(j), max_scale];
        fprintf('%d %d %d\n', nstep, i, j);
        new_train = merge_train(current_train_list{i}, current_train_list{j});
        current_cluster{i} = [current_cluster{i}, current_cluster{j}];
        current_cluster(j)= [];
        current_train_list{i} = new_train;
        current_train_list(j) =  [];
        if length(current_train_list) == 1
            done = 1
        else
            surrogate_data_set = update_surrogate_dataset(surrogate_data_set, sigma, new_train, i, j);            
            cdf_matrix = update_cdf_distance(cdf_matrix, surrogate_data_set, current_train_list, i, j);
            distance_matrix = update_distance_data_set(distance_matrix, current_train_list, i);
        end
                            
        nstep = nstep + 1;    
    end
end
