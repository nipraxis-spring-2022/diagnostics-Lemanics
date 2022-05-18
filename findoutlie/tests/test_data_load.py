""" Test script for data load functions

Run these tests with::

    python3 findoutlie/tests/test_data_load.py

or better, in IPython::

    %run findoutlie/tests/test_data_load.py
"""

import os.path as op
import sys

MY_DIR = op.dirname(__file__)

sys.path.append("findoutlie")
from nibabel import nifti1

from data_load import get_fname, load_sub_run


def test_get_fname():
    
    # Testing simple filenames
    fname_to_test = get_fname(1, 2)
    assert fname_to_test == 'data/group-00/sub-01/func/sub-01_task-taskzero_run-02_bold.nii.gz'
    fname_to_test = get_fname(5, 5)
    assert fname_to_test == 'data/group-00/sub-05/func/sub-05_task-taskzero_run-05_bold.nii.gz'

    # Testing manual data directory
    fname_to_test = get_fname(5, 5, data_dir = 'another_data')
    assert fname_to_test == 'another_data/group-00/sub-05/func/sub-05_task-taskzero_run-05_bold.nii.gz'

def test_load():
    
    # Testing data loading
    img_to_test = load_sub_run(1, 2)
    assert type(img_to_test) == nifti1.Nifti1Image

    # Testing compatibility with multiple loadings (as lists)
    img_list = load_sub_run([1, 2], 2)
    assert len(img_list) == 2
    assert type(img_list) == list
    assert type(img_list[0]) == nifti1.Nifti1Image

    img_list = load_sub_run([1, 2], [1, 2])
    assert len(img_list) == 4
    assert type(img_list) == list
    assert type(img_list[2]) == nifti1.Nifti1Image
    
    


if __name__ == "__main__":
    # File being executed as a script
    test_get_fname()
    test_load()
    print("Tests passed")
