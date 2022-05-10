"""
This module defines functions implementing algorithms in SPM

Here you want the get_spm_globals function from the earlier
``four_dimensions_exercise``, with anything that function imports and other
definitions that the function needs.

See:
    https://bic-berkeley.github.io/psych-214-fall-2016/four_dimensions_exercise.html

In the same directory as this file, you will find a 'tests' directory.

Test this module with:

    python3 findoutlie/tests/test_spm_funcs.py

or better, in IPython::

    %run findoutlie/tests/test_spm_funcs.py
"""

# Any imports you need
# +++your code here+++
import numpy as np
import nibabel as nib


def spm_global(vol):
    """ Calculate SPM global metric for array `vol`

    Parameters
    ----------
    vol : array
        Array giving image data, usually 3D.

    Returns
    -------
    g : float
        SPM global metric for `vol`
    """

    T = np.mean(vol) / 8
    return np.mean(vol[vol > T])


def get_spm_globals(fname):
    """ Calculate SPM global metrics for volumes in image filename `fname`

    Parameters
    ----------
    fname : str
        Filename of file containing 4D image

    Returns
    -------
    spm_vals : array
        SPM global metric for each 3D volume in the 4D image.
    """
    func_img = nib.load(fname)
    n_tp = func_img.shape[-1]

    func_dat = func_img.get_fdata()

    global_metric = np.zeros((n_tp))
    for t in range(n_tp):
        global_metric[t] = spm_global(func_dat[..., t])

    return global_metric