"""
    : test_fca.py
    Created: 10/04/17
    Description:
        Simple script to test FCA algorithm
"""

import numpy as np
import numpy.random as rnd
from fca import functional_clustering_algorithm


def test_functional_clustering():
    rnd.seed(2)
    n_trains = 10

    # create two group - one periodical with noise and one random

    n_group1 = 3
    n_group2 = n_trains - n_group1

    train_list = []
    tmax = 1000.0
    freq1 = 1.0
    period = 3.5

    print "creating spikes train"
    for i in range(n_group1):
        train = np.arange(1.0 * rnd.random(), tmax, period)
        train_list.append(train)
    for i in range(n_group2):
        train = np.cumsum([-np.log(rnd.random())/freq1 for i in range(int(tmax*freq1))])
        train = train[train < tmax]
        train_list.append(train)
    for i in range(n_group1):
        train = np.arange(0.0 * rnd.random(), tmax, period)
        train_list.append(train)
    print "starting clustering"
    merge_history, current_cluster = functional_clustering_algorithm(train_list, 300, .10)
    return train_list, merge_history, current_cluster
