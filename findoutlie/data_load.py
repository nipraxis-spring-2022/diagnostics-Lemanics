"""
This module defines functions to load data from files.

Test this module with:

    python3 findoutlie/tests/test_data_load.py

or better, in IPython::

    %run findoutlie/tests/test_data_load.py
"""

import os.path as op
import nibabel as nib

def get_fname(sub_id, run_num, data_dir = "data/"):
    """Get the filename for a specified subject-run functional data.

    Parameters
    ----------
    sub_id : int
        Subject ID to load data from.
    run_num : int
        Run number to load.
    data_dir : str, optional
        Path to the "data" directory, by default "data/"

    Returns
    -------
    path_to_run
        Path to the subject-run file containing the functional data.

    Raises
    ------
    TypeError
        Type of "sub_id" or "run_num" was not recognized, expected "int".
    """

    try:
        filename = f"sub-{sub_id:02d}_task-taskzero_run-{run_num:02d}_bold.nii.gz"
    except ValueError:
        print('Fixing type for "sub_id" or/and "run_num"')
        filename = f"sub-{int(sub_id):02d}_task-taskzero_run-{int(run_num):02d}_bold.nii.gz"
    except:
        raise TypeError('Unrecognized type for "sub_id" or/and "run_num", expected "int",',
                        f'got {type(sub_id)}, {type(run_num)}')

    path_to_run = op.join(data_dir, "group-00", f"sub-{sub_id:02d}", "func", filename)

    return path_to_run

def load_sub_run(sub_id, run_num, **kwargs):
    """Load functional images of a specified subject-run.

    Parameters
    ----------
    sub_id : int or list
        Subject ID(s) to load data from.
    run_num : int or list
        Run number(s) to load.

    Returns
    -------
    func_img
        Nifti image(s) of the functional run(s).

    Raises
    ------
    FileNotFoundError
        Functional file was not found in the specified directory.
    """

    if type(sub_id) == int:
        sub_id = [sub_id]
        
    if type(run_num) == int:
        run_num = [run_num]

    images = []

    for sub in sub_id:
        for run in run_num:
            path_to_run = get_fname(sub, run, **kwargs)

            if not op.isfile(path_to_run):
                raise FileNotFoundError(f'File "{path_to_run}" does not exist')

            images.append(nib.load(path_to_run))

    # Returns only one image if a single subject-run was specified
    if len(sub_id) == len(run_num) == 1:
        images = images[0]

    return images

def load_image(fname):
    """ Load the functional 4D image from a filepath

    Parameters
    ----------
    fname : str
        Path to the nifit file

    Returns
    -------
    nibabel image
        Functional 4D image

    Raises
    ------
    FileNotFoundError
        Specified fname was not found.
    """

    if not op.isfile(fname):
        raise FileNotFoundError(f'File "{fname}" does not exist')

    image = nib.load(fname)

    return image
