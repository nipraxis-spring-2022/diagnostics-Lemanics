""" Module with routines for finding outliers
"""

import os.path as op
from glob import glob

import numpy as np

import findoutlie.data_load as data_load
import findoutlie.detectors as detectors
# Unused for now
import findoutlie.metrics as metrics


def detect_outliers(fname):
    """ Outlier detection routine.

    Parameters
    ----------
    fname : str
        Path to the file containing the functional image

    Returns
    -------
    list
        List of frames considered as outliers.
    """

    # Configuration list for metrics and detectors names
    CONFIG = [['dvars', 'coefficient_of_variation'], ['median_detector', 'iqr_detector']]

    image = data_load.load_image(fname)

    metrics_list = CONFIG[0]
    detectors_list = CONFIG[1]

    n_metrics = len(CONFIG[0])
    n_timepoints = image.shape[-1]
    outlier_tfs = np.zeros((n_metrics, n_timepoints))

    for i, (metric_name, detector_name) in enumerate(zip(metrics_list, detectors_list)):
        # Later to be called from metrics.py
        metric = metrics.compute_metric(image, metric_name)
        outlier_tfs[i] = detectors.compute_outliers(metric, n_timepoints, detector_name)

    outlier_decision_tf = detectors.consensus_outliers(outlier_tfs, decision='any')
    outlier_frames_id = np.where(outlier_decision_tf > 0)[0]

    return list(outlier_frames_id)


def find_outliers(data_directory):
    """ Return filenames and outlier indices for images in `data_directory`.

    Parameters
    ----------
    data_directory : str
        Directory containing containing images.

    Returns
    -------
    outlier_dict : dict
        Dictionary with keys being filenames and values being lists of outliers
        for filename.
    """
    image_fnames = glob(op.join(data_directory, '**', 'sub-*.nii.gz'),
                        recursive=True)
    outlier_dict = {}
    for fname in image_fnames:
        outliers = detect_outliers(fname)
        outlier_dict[fname] = outliers
    return outlier_dict

