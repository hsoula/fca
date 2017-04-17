# Functional Clustering Algorithm 

This python code implemente the functional clustering algorithm (FCA) for spike trains hierarchical clustering. 


The algorithm is described in _Feldt S, Waddell J, Hetrick VL, Berke JD, Zochowski M (2009) Functional clustering algorithm for the analysis of dynamic network data. Phys Rev E Stat Nonlin Soft Matter Phys 79(5 Pt 2):056104_


It works as follows:
1. starts with n_trains spike trains to cluster
2. create surrogate data by jittering spike train (n_surrogate of n_trains spike trains) 
3. compute the distance matrix - here a distance is given but any distance should work 
4. use the surrogate to create an empirical noise distribution 
5. compute the probability to obtain this distance according to the surrogate 
6. take the most significant pair of spike trains 
7. merge them and recompute the new surrogate data with the new spike trains set
8. repeat 5 to 7 until either 5% threshold is reached 

This code is in pure python and should work without dependency (except numpy). It therefore portable but very slow. 


A simple example is given with obvious clustering (and of course the algorithm yields the expected result).

HAS 


