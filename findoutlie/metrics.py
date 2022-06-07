""" Scan outlier metrics

Currently implemented metrics : 
    - dvars

To implement : 
    - ...

Template function : 

def metric_name(img):
    " Calculate metric on Nibabel image `img`

    metric description

    Parameters
    ----------
    img : nibabel image

    Returns
    -------
    metric : 1D array
        One-dimensional array containing the computed metric
    "
    --- do stuff ---
    return metric

"""

import numpy as np

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

    metric_func = globals()[metric_name]
    metric_tf = metric_func(img, **kwargs)

    return metric_tf

def dvars(img):
    """ Calculate TEMPORAL dvars metric on Nibabel image `img`

    The dvars calculation between two volumes is defined as the square root of
    (the sum of the (voxel differences squared) divided by the number of
    voxels).

    Parameters
    ----------
    img : nibabel image

    Returns
    -------
    dvals : 1D array
        One-dimensional array with n-1 elements, where n is the number of
        volumes in `img`.
    """
    # Hint: remember 'axis='.  For example:
    # In [2]: arr = np.array([[2, 3, 4], [5, 6, 7]])
    # In [3]: np.mean(arr, axis=1)
    # Out[2]: array([3., 6.])
    #
    # You may be be able to solve this in four lines, without a loop.
    # But solve it any way you can.
    data = img.get_fdata()
    voxel_per_time = data.reshape(-1, data.shape[-1]) #np.reshape(data,new_shape)
    diff = np.diff(voxel_per_time)
    dvals = np.sqrt(np.mean(diff ** 2, axis=0))
    return dvals


#def standardized_dvar(img):
    #https: // warwick.ac.uk / fac / sci / statistics / staff / academic - research / nichols / scripts / fsl / standardizeddvars.pdf


def coefficient_of_variation(img):
    #looking at the output nii I am not quite sure this is right
    """ Calculate the coefficient of variation (CV)
    also known as relative standard deviation (RSD),
    is a standardized measure of dispersion of a probability distribution
    or frequency distribution. It is often expressed as a percentage,
    and is defined as the ratio of the standard deviation to the mean

    NB : Issue if  mean value is close to zero, should not be the case though
    TO DO ? : would be better to do it for each tissue class
    or at least on the brain vs background, not sure it makes a lot of sense here

    Parameters
    ----------
    img : nibabel image

    Returns
    -------
    CV : 1D array
        One-dimensional array with n elements, where n is the number of
        volumes in `img`. This array contains the coefficient of variation for each volume.

    """
    data = img.get_fdata()
    cv=np.std(data, axis=(0,1,2))/np.mean(data, axis=(0,1,2))

    return cv


