""" Utilities for detecting outliers

These functions take a vector of values, and return a boolean vector of the
same length as the input, where True indicates the corresponding value is an
outlier.

The outlier detection routines will likely be adapted to the specific measure
that is being worked on.  So, some detector functions will work on values > 0,
other on normally distributed values etc.  The routines should check that their
requirements are met and raise an error otherwise.
"""

import numpy as np
# This should be later removed as "compute_metric()" will be moved to "metrics.py"
import findoutlie.metrics as metrics

def compute_metric(img, metric_name = 'dvars', **kwargs):
    """ Compute the metric value of a 4D image for a specified metric name.

    Parameters
    ----------
    img : nibabel image
        Functional 4D image
    metric_name : str, optional
        Name of the metric to compute, by default 'dvars'

    Returns
    -------
    numpy array
        Metric values at each timepoints (usually of size n_timepoints but could be less)
    """

    metric_func = getattr(metrics, metric_name)
    metric_tf = metric_func(img, **kwargs)

    return metric_tf

def compute_outliers(metric_values, n_timepoints, detector_name = 'iqr_detector', **kwargs):
    """ Compute the outlier mask timeframe of a metric array for a specified detector.

    Parameters
    ----------
    metric_values : numpy array
        Metric value at each timepoint
    n_timepoints : int
        Number of timepoints in the functional data
    detector_name : str
        Name of the detector to use in the outlier detection

    Returns
    -------
    numpy array (n_timepoints)
        Outlier mask timeframe with 1 if the frame is considered as an outlier and 0 otherwise.
    """

    detector_func = globals()[detector_name]
    outlier_tf = detector_func(metric_values, **kwargs)

    while len(outlier_tf) < n_timepoints:
        outlier_tf = np.insert(outlier_tf, 0, 0)

    return outlier_tf

def consensus_outliers(outlier_tfs, decision = 'all'):
    """ Decide if a frame is to be considered as outlier or not based on the outcome of all metrics.

    Parameters
    ----------
    outlier_tfs : numpy array (n_metrxi x n_timepoints)
        Array with the outlier mask timeframe for each metric
    decision : str, optional
        Type of the decisions for the final mask vector ('all', 'any', etc), by default 'all'

    Returns
    -------
    numpy array
        Outlier mask timeserie with the final decision on outlier detection
    """

    if type(outlier_tfs) != np.array:
        outlier_tfs = np.array(outlier_tfs)

    if decision == 'all':
        outlier_decision_tf = (outlier_tfs.sum(axis = 0) == outlier_tfs.shape[0])
    elif decision == 'any':
        outlier_decision_tf = (outlier_tfs.sum(axis = 0)  > 0)

    return outlier_decision_tf

def iqr_detector(measures, iqr_proportion=1.5):
    """Detect outliers in `measures` using interquartile range.

    Returns a boolean vector of same length as `measures`, where True means the
    corresponding value in `measures` is an outlier.

    Call Q1, Q2 and Q3 the 25th, 50th and 75th percentiles of `measures`.

    The interquartile range (IQR) is Q3 - Q1.

    An outlier is any value in `measures` that is either:

    * > Q3 + IQR * `iqr_proportion` or
    * < Q1 - IQR * `iqr_proportion`.

    See: https://en.wikipedia.org/wiki/Interquartile_range

    Parameters
    ----------
    measures : 1D array
        Values for which we will detect outliers
    iqr_proportion : float, optional
        Scalar to multiply the IQR to form upper and lower threshold (see
        above).  Default is 1.5.

    Returns
    -------
    outlier_tf : 1D boolean array
        A boolean vector of same length as `measures`, where True means the
        corresponding value in `measures` is an outlier.
    """
    Q1 = np.percentile(measures, 25)
    Q3 = np.percentile(measures, 75)
    IQR = Q3 - Q1
    outlier_tf = np.logical_or(
        measures > Q3 + iqr_proportion * IQR, measures < Q1 - iqr_proportion * IQR
    )

    return outlier_tf
