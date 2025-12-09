from sklearn.neighbors import NearestNeighbors
import numpy as np
import matplotlib
import adjustText

# Import the following to allow matplotlib to find sans-serif on CentOS.
import matplotlib.font_manager

# Always include the following:
matplotlib.rcParams['pdf.fonttype'] = 42
matplotlib.rcParams['ps.fonttype'] = 42

#matplotlib.rcParams['font.family'] = 'sans-serif'
#matplotlib.rcParams['font.sans-serif'] = 'Arial'


def label_outliers(
    _x, _y, _val, proximity_cutoff=None, scale_cutoff=1, ax=None, n_points_too_close_to_label=4, 
    n_points_too_close_to_need_arrow=1, no_adjust=False, dodge=0,
    arrowprops={'arrowstyle':'-', 'color':'gray', 'alpha':.5}, fontsize=5, 
    always_plot=[], verbose=False, **adjust_text_kwargs):
    """Label points on a graph. Identifies points with few neighbors and points without an arrow.
    If arrowprops is not False (default), label with an arrow. adjustText is used to plot the text labels.
    Extra keyword arguments are passed to adjustText.adjust_text.
    A higher scale_cutoff is a higher proximity cutoff (fewer labels).
    For faster plotting of huge numbers of datapoints, use no_adjust=True.
    The dodge option should only be used if no_adjust=True.
    Pass always_plot a list of labels to always plot those labels."""
    
    if proximity_cutoff is None:  # Estimate from data.
        xspan,yspan = (np.max(_x)-np.min(_x), np.max(_y)-np.min(_y))
        proximity_cutoff = ((xspan*yspan)**0.5)/(20/scale_cutoff)
        verbose and (print(f"Estimating a proximiting cufoff {proximity_cutoff} because proximity_cutoff<0"))

    (ax is None) and print(f"ax was not given - this function does nothing without the ax parameter")
        
    points = np.array([(x,y) for x,y in zip(_x, _y)])
    
    # Get rid of nan and infinite.
    filt = np.isnan(points).any(axis=1)
    filt2 = ~np.isfinite(points).all(axis=1)
    filt = np.array([(a | b) for a,b in zip(filt, filt2)])
    if np.any(filt):
        _x = np.array(_x[~filt])
        _y = np.array(_y)[~filt]
        _val = np.array(_val)[~filt]
        points = np.array([(x,y) for x,y in zip(_x, _y)])

    nbrs = NearestNeighbors(n_neighbors=min([len(points), n_points_too_close_to_label + 1])).fit(points)
    distances, indices = nbrs.kneighbors(points)
          
    closest_points = distances[:, 1:n_points_too_close_to_label+2]
    n_points_close = [len(x[x<proximity_cutoff]) for x in closest_points]
    
    if not no_adjust:
        dodge = 0

    textsNoArrow, textsWithArrow = [], []
    for (x, y, val, n_points_close_to_this_dot) in zip(_x, _y, _val, n_points_close):
        
        if np.any(~np.isfinite([x, y])):
            continue

        if n_points_close_to_this_dot < n_points_too_close_to_need_arrow:
            t = ax.text(x + dodge, y + dodge, val, size=fontsize)
            textsNoArrow.append(t)
            
        elif (n_points_close_to_this_dot < n_points_too_close_to_label) or (val in always_plot):
            t = ax.text(x + dodge, y + dodge, val, size=fontsize)
            textsWithArrow.append(t)
    
    if not no_adjust:
        if len(textsNoArrow):
            adjustText.adjust_text(textsNoArrow, ax=ax, **adjust_text_kwargs)
        if len(textsWithArrow):
            adjustText.adjust_text(textsWithArrow, ax=ax, arrowprops=arrowprops, **adjust_text_kwargs)
    
