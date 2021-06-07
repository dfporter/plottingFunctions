from sklearn.neighbors import NearestNeighbors
import numpy as np

import matplotlib

# Import the following to allow matplotlib to find sans-serif on CentOS.
import matplotlib.font_manager

# Always include the following:
matplotlib.rcParams['pdf.fonttype'] = 42
matplotlib.rcParams['ps.fonttype'] = 42

matplotlib.rcParams['font.family'] = 'sans-serif'
matplotlib.rcParams['font.sans-serif'] = 'Arial'

def label_outliers(
    _x, _y, _val, proximity_cutoff=None, scale_cutoff=1, ax=None, n_points_too_close_cutoff=3, fontsize=5, verbose=False):
    
    if proximity_cutoff is None:  # Estimate from data.
        xspan,yspan = (np.max(_x)-np.min(_x), np.max(_y)-np.min(_y))
        proximity_cutoff = ((xspan*yspan)**0.5)/(20/scale_cutoff)
        verbose and (print(f"Estimating a proximiting cufoff {proximity_cutoff} because proximity_cutoff<0"))

    (ax is None) and print(f"ax was not given - this function does nothing without the ax parameter")
        
    points = np.array([(x,y) for x,y in zip(_x, _y)])
    nbrs = NearestNeighbors(n_neighbors=min([len(points), 10])).fit(points)
    distances, indices = nbrs.kneighbors(points)
    closest_points = distances[:, 1:n_points_too_close_cutoff+2]
    n_points_close = [len(x[x<proximity_cutoff]) for x in closest_points]
    
    for (x, y, val, n_points_close) in zip(_x, _y, _val, n_points_close):
        if n_points_close >= n_points_too_close_cutoff:
            continue  # Don't label.
        if ax is not None:
            ax.text(x, y, val, size=fontsize)

