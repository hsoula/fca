"""
    : fca.py
    Created: 10/04/17
    Description: own interpretation of functional clustering

"""

import numpy as np
import numpy.random as rnd


def average_minimum_distance(train1, train2):
    """
        Compute the average minimum distance between spike trains train 1 and train 2
        trains should be in the form train[i] = T ith spike occurs at time T
    :param train1: first train to be compared
    :param train2: second train
    :return: distance positive float

    """
    dist1 = 0
    for spike_t in train1:
        diff_spike = train2 - spike_t
        delta = np.min(np.abs(diff_spike))
        dist1 += delta
    dist2 = 0
    for spike_t in train2:
        diff_spike = train1 - spike_t
        delta = np.min(np.abs(diff_spike))
        dist2 += delta

    return 0.5 * (dist1 + dist2)


def jitter_spike_train(train, sigma):
    """
        Compute new spike trains jitterd by gaussian (centered) noise with sd  sigma
        train should be in the form train[i] = T ith spike occurs at time T
    :param train:
    :param sigma:
    :return: new spike trains - with same number of spike len = len(train)

    """

    n = len(train)
    new_train = train.copy()
    new_train += sigma * rnd.randn(n)
    return new_train


def jitter_data_set(train_list, sigma):
    """
        create new train list with jittered spike trains
    :param train_list: the spike train list to be jittered
    :param sigma: noise of jittering
    :return: new jittered train list

    """
    jittered_list = []
    for train in train_list:
        new_train = jitter_spike_train(train, sigma)
        jittered_list.append(new_train)
    return jittered_list


def distance_data_set(train_list):
    """
        Compute distance matrix for each pair of trains
    :param train_list: list of train in the in the form train[i] = T ith spike occurs at time T
    :return: a len(train_list) square matrix with distance
    """
    ntrains = len(train_list)
    distance_matrix = np.zeros((ntrains, ntrains))
    for i in range(ntrains):
        for j in range(i+1, ntrains):
            train1 = train_list[i]
            train2 = train_list[j]
            d = average_minimum_distance(train1, train2)
            distance_matrix[i, j] = d
            distance_matrix[j, i] = d
    return distance_matrix


def update_distance_data_set(distance_matrix, train_list, idx_train1, surrogate_train):
    """
        update the distance matrix for a pair a train assuming the train list contains new (with the merged train)
        at position idx_train1 - we remove row and column idx_train2
    :param train_list: list of train in the in the form train[i] = T ith spike occurs at time T
    :return: a len(train_list) square matrix with distance
    """
    ntrains = len(train_list)

    for j in range(ntrains):
        train2 = train_list[j]
        d = average_minimum_distance(surrogate_train, train2)
        distance_matrix[idx_train1, j] = d
        distance_matrix[j, idx_train1] = d
    return distance_matrix


def scaled_value(cdf, v, ci=0.05):
    """
        From cdf value compute the distance to the 95% interval (low so 5%)
    :param cdf: the sorted vector of values
    :param v: the value to find the significance level
    :param ci: confidence interval - default 5%
    :return: a float os scaled value
    """
    n = len(cdf)
    n2 = n/2.0
    n5 = n * ci
    nv = len(cdf[cdf < v])
    return max(0, (n2-nv)/(n2-n5))


def scaled_significance_matrix(train_list, cdf_matrix):

    n_surrogate, nx, ny = cdf_matrix.shape
    distance_matrix = distance_data_set(train_list)
    scaled_matrix = np.zeros((nx, nx))
    for i in range(nx):
        for j in range(i+1, nx):
            scaled_matrix[i, j] = scaled_value(cdf_matrix[:, i, j], distance_matrix[i, j])
    return scaled_matrix


def merge_trains(train1, train2):
    """
        Merge spike train in the form train[i] = T ith spike occurs at time T
    :param train1:
    :param train2:
    :return: a merged spike train in the form train[i] = T ith spike occurs at time T
    """
    x = np.concatenate((train1, train2))
    x.sort()
    return x


def create_surrogate_dataset(train_list, nsurrogate, sigma):
    surrogate_data_set = []
    for i in range(nsurrogate):
        surrogate_data_set.append(jitter_data_set(train_list, sigma))
    return surrogate_data_set


def update_surrogate_dataset(surrogate_data_set, sigma, merged_train, idx_train1, idx_train2):
    nsurrogate = len(surrogate_data_set)
    for i in range(nsurrogate):
        train_list = surrogate_data_set[i]
        train_list.pop(idx_train2)
        train_list[idx_train1] = jitter_spike_train(merged_train, sigma)
    return surrogate_data_set


def cdf_distance(train_list, surrogate_data_set):
    """
        create for each pair of train a cumulative distance function for distance based on the surrogate
        data set
        - first nsurrogate surrogate data sets are created
        - the for each surrogate data set a distance matrix is created
        - for each pair - entry in the matrix - a cdf if computed
    :param train_list:
    :param sigma:
    :param nsurrogate:
    :return:
    """
    ntrains = len(train_list)
    nsurrogate = len(surrogate_data_set)

    cdf_matrix = np.zeros((nsurrogate, ntrains, ntrains))
    for i in range(nsurrogate):
        print "surrogate", i
        surrogate_distance_matrix = distance_data_set(surrogate_data_set[i])
        cdf_matrix[i, :, :] = surrogate_distance_matrix

    # sort each entry to create the cdf
    for i in range(ntrains):
        for j in range(i+1, ntrains):
            cdf_matrix[:, i, j].sort()
            cdf_matrix[:, j, i].sort()
    return cdf_matrix


def update_cdf_distance(cdf_matrix, surrogate_data_set, train_list, idx_train1, idx_train2):
    """
       update  cumulative distance function for distance based on the surrogate
        data set by removing idx_train2 and usinf idx_train1 as placeholder for merged
    """
    ntrains = len(train_list)
    nsurrogate = cdf_matrix.shape[0]
    cdf_matrix = np.delete(cdf_matrix, idx_train2, 1)
    cdf_matrix = np.delete(cdf_matrix, idx_train2, 2)
    for i in range(nsurrogate):
        surrogate_train = surrogate_data_set[i][idx_train1]
        cdf_matrix[i, :, :] = update_distance_data_set(cdf_matrix[i, :, :], train_list, idx_train1, surrogate_train)
    # sort each entry to create the cdf
    for i in range(ntrains):
        for j in range(i+1, ntrains):
            cdf_matrix[:, i, j].sort()
            cdf_matrix[:, j, i].sort()
    return cdf_matrix


def functional_clustering_algorithm(train_list, nsurrogate, sigma, early_stop=False):
    """
        Main clustering algorithm
    :param train_list:
    :param nsurrogate:
    :param sigma:
    :return:
    """
    print "starting clustering"
    done = False
    ntrain = len(train_list)
    current_train_list = train_list[:]
    current_cluster = range(ntrain)
    merge_history = []
    nstep = 0
    surrogate_data_set = create_surrogate_dataset(train_list, nsurrogate, sigma)
    cdf_matrix = cdf_distance(current_train_list, surrogate_data_set)

    while not done:
        print "doing step", nstep
        print "computing cdf"
        scale_matrix = scaled_significance_matrix(current_train_list, cdf_matrix)
        maximum_scale = np.max(scale_matrix)
        print "max scale", maximum_scale
        if early_stop and maximum_scale < 1.0:
            done = True
        else:
            i, j = np.unravel_index(np.argmax(scale_matrix), scale_matrix.shape)
            print "max index", i, j
            if i > j:
                i, j = j, i

            merge_history.append([current_cluster[i], current_cluster[j], maximum_scale])
            new_train = merge_trains(current_train_list[i], current_train_list[j])
            current_cluster[i] = [current_cluster[i], current_cluster[j]]
            current_cluster.pop(j)
            new_list = []
            current_train = len(current_train_list)
            for ix in range(current_train):
                if ix == i:
                    new_list.append(new_train)
                elif ix == j:
                    pass
                else:
                    new_list.append(current_train_list[ix])
            current_train_list = new_list[:]
            if len(current_train_list) == 1 :
                done = True
            else:
                surrogate_data_set = update_surrogate_dataset(surrogate_data_set, sigma, new_train, i, j)
                cdf_matrix = update_cdf_distance(cdf_matrix,  surrogate_data_set, current_train_list, i, j)
        nstep += 1
    return merge_history, current_cluster


def create_linkage(n_nodes, merge_history):
    """
        Create the Z matrix for dendrogram plotting
    :param merge_history: the merge history as list of lists
    :return: a (n-1) * 4 matrix as coded in sklearn.clustering.linkage function
    """
    Z = []
    cluster_list = range(n_nodes)
    cluster_size = [1] * n_nodes

    for merge in merge_history:
        cluster1 = merge[0]
        cluster2 = merge[1]
        if cluster1 not in cluster_list:
            cluster_list.append(cluster1)
            cl1, cl2 = cluster1
            id1 = cluster_size[cluster_list.index(cl1)]
            id2 = cluster_size[cluster_list.index(cl2)]
            cluster1_size = cluster_size[id1] + cluster_size[id2]
            cluster_size.append(cluster1_size)

        if cluster2 not in cluster_list:
            cluster_list.append(cluster2)
            cl1, cl2 = cluster2
            id1 = cluster_size[cluster_list.index(cl1)]
            id2 = cluster_size[cluster_list.index(cl2)]
            cluster2_size = cluster_size[id1] + cluster_size[id2]
            cluster_size.append(cluster2_size)
        print len(cluster_size)
        ix1 = cluster_list.index(cluster1)
        ix2 = cluster_list.index(cluster2)
        Z.append([ix1, ix2, 1.0, 1])
    return Z

