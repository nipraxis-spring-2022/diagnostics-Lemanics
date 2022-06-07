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

def iqr_detector(measures, iqr_proportion=1.5, pos_only = True, neg_only = False):
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
        above).  Default is 2.
    pos_only : bool, optional
        Condition to filter only values above the upper threshold.  Default is True.
    neg_only : bool, optional
        Condition to filter only values above the lower threshold.  Default is False.

    Returns
    -------
    outlier_tf : 1D boolean array
        A boolean vector of same length as `measures`, where True means the
        corresponding value in `measures` is an outlier.
    """
    Q1 = np.percentile(measures, 25)
    Q3 = np.percentile(measures, 75)
    IQR = Q3 - Q1
    outlier_tf = np.logical_or((not neg_only)*( measures > Q3 + iqr_proportion * IQR),
                                (not pos_only)*(measures < Q1 - iqr_proportion * IQR))

    return outlier_tf

def median_detector(measures, scale = 5, pos_only = True, neg_only = False):
    """Detect outliers in `measures` from the scaled Means Absolute Deviation.
    
    An outlier is any value in `measures` that is either:

    * > median(measures) + scaled_MAD * `scale`
    * < median(measures) - scaled_MAD * `scale`

    where scaled_MAD is defined as `c * median(abs(measures - median(measures)))` and
    c is `-1/sqrt(2)*erfcinv(3/2)` whichi is approxcimately equal to 1.4826

    Frames with metric value that is more then three scaled MAD from the median are labeled as outliers.

    See: https://en.wikipedia.org/wiki/Median_absolute_deviation

    Parameters
    ----------
    metric : numpy array
        Metric to detect outlier on
    scale : int, float, optional
        Scalar to multiply the scaled MAD to form upper and lower threshold (see
        above).  Default is 4.
    pos_only : bool, optional
        Condition to filter only values above the upper threshold.  Default is True.
    neg_only : bool, optional
        Condition to filter only values above the lower threshold.  Default is False.

    Returns
    -------
    numpy array (bool)
        Outlier mask timeframe with a 1 if a frame is labeled as an outlier and 0 otherwise.
    """
    # Corresponding to erfcinv(3/2), to avoid importing "scipy.special" only for this
    ERFCINV_CST = -0.4769362762044699

    c = -1/(np.sqrt(2)*ERFCINV_CST)
    # MAD is the Mean Absolute Deviation
    scaled_mad = c * np.median(np.abs(measures - np.median(measures)))

    outlier_tf = np.logical_or((not neg_only)*(measures > np.median(measures) + scale * scaled_mad),
                                (not pos_only)*(measures < np.median(measures) - scale * scaled_mad))

    return outlier_tf