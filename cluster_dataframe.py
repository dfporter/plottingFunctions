# The seaborn clustering algorithm.
from scipy.cluster import hierarchy
import numpy as np
import fastcluster

def calculate_dendrogram(linkage):
    """Calculates a dendrogram based on the linkage matrix
    Made a separate function, not a property because don't want to
    recalculate the dendrogram every time it is accessed.
    Returns
    -------
    dendrogram : dict
        Dendrogram dictionary as returned by scipy.cluster.hierarchy
        .dendrogram. The important key-value pairing is
        "reordered_ind" which indicates the re-ordering of the matrix
    """
    return hierarchy.dendrogram(linkage, no_plot=True,
                                color_threshold=-np.inf)

def _calculate_linkage_fastcluster(array, metric='euclidean', method='single'):
    # Fastcluster has a memory-saving vectorized version, but only
    # with certain linkage methods, and mostly with euclidean metric
    # vector_methods = ('single', 'centroid', 'median', 'ward')
    euclidean_methods = ('centroid', 'median', 'ward')
    euclidean = metric == 'euclidean' and method in \
        euclidean_methods
    if euclidean or method == 'single':
        return fastcluster.linkage_vector(array,
                                          method=method,
                                          metric=metric)
    else:
        linkage = fastcluster.linkage(array, method=method,
                                      metric=metric)
        return linkage

def _index_to_ticklabels(index):
    """Convert a pandas index or multiindex into ticklabels."""
    if isinstance(index, pandas.MultiIndex):
        return ["-".join(map(to_utf8, i)) for i in index.values]
    else:
        return index.values
    
def cluster_rows_of_dataframe(sub: pandas.DataFrame):
    linkage = _calculate_linkage_fastcluster(sub.values)
    dendrogram = calculate_dendrogram(linkage)
    ticklabels = _index_to_ticklabels(sub.index)
    ticklabels = [ticklabels[i] for i in dendrogram['leaves']]
    sub = sub.loc[ticklabels,:]
    return sub