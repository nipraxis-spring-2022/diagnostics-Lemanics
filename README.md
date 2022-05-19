# Lemanics team project

Repository containing the Lemanics' team project for the 2022 edition of the nipraxis course.


## Table of contents
<!--  comment * [General information](#General-information) 
README/
[steps](README.md#installation--usage -->
* [Diagnostics project](#diagnostics-project)
* [Project plan](#proejct-plan)
* [Installation & Usage](#installation--usage)

<!-- * [Common](#Common issues - debugging)
* [Example](#Example)-->

# Diagnostics project
## Goal
The purpose of this project is to implement a framework to detect outliers.
This README file has instructions on how to get, validate and process the data.

## Guidelines
- Scripts go in the `scripts` directory.

- Library code (Python modules) goes in the `findoutlie` directory.

- You should put the code in this `findoutlie` directory on your Python PATH.

# Project plan
## Group
Work by group of 2 or 3 so to facilitate peer reviewing (please add your group below, the best might be to mix python level of coding):
- group 1 : ....
- group 2 : ....

**How to work on git - reminder**: for each feature, create a branch, merge to the origin etc. 

## Metrics
The idea is for now to pick two metrics (more if we have time, 1 metric per group) and then to compute a final score. 

For the metric, the idea are - for now :

    *this part below was added by Soraya, let me know what you think and feel free to add your metrics. I think picking SNR and Shannon entropy could be nice.Shannon will be more difficult to implement. Then if we have time we can pick other one.*

- **Metrics based on noise measurements - pick 1 metric**
    - **Classic signal to noise ratio (SNR)**
    There are 4 approaches for SNR : 1) the pixel-by-pixel standard deviation (SD) in multiple repeated acquisitions; 2) the signal statistics in a difference image; and 3) and 4) the statistics in two separate regions of a single image employing either the mean value or the SD of background noise [Dietrich 2007](https://onlinelibrary.wiley.com/doi/10.1002/jmri.20969). There is also the remporal variation tSNR which is the average BOLD signal across time divided by the temporal deviation map [Kruger 2001](https://onlinelibrary.wiley.com/doi/10.1002/mrm.1240)

    -**Contrast-to-noise ratio (CNR)**: The cnr [Magnota 2006](https://link.springer.com/article/10.1007/s10278-006-0264-x), is an extension of the SNR calculation to evaluate how separated the tissue distributions of GM and WM are.Higher values indicate better quality. 
    
- **Metrics based on spatial information**
    - Shannon entropy of voxel intensities for bluriness and ghosting [Atkinson1997](https://ieeexplore.ieee.org/document/650886).Lower values are better.
    cf *"Shannon entropy H was calculated in each voxel independently (i.e. using the voxel probability distribution obtained by standard histogram method)", see the full formula in the article below* [DiNuzzo 2003](https://www.researchgate.net/publication/277668496_Shannon_entropy_method_applied_to_fMRI_data_series_during_evoked_and_resting_state_activity)


- **Metrics based on temporal information**
    - DVARS, rate of change per frame (can be spatial or temporal,cf practical)
    - tSNR cf below in SNR

--> Updating & using [findoutlie/metric.py/metric_name](/findoutlie/metric.py)

## Distribution
The distribution of all the metrics in regards to all the database should be plot to faciliate the detection of outliers (Boxplots per metrics ?).

--> Updating & using [findoutlie/outfind.py/detect_outliers](/findoutlie/outfind.py)
    --> should use the [findoutlie/detectors.py/iqr_detector](/findoutlie/detectors.py) which detect outliers in measures using interquartile range
    --> then outfind.py will be used by [scripts/find_outliers.py](/scripts/find_outliers.py) to print the list of outliers

--> Therefore the function to plot the distribution should be in [scripts/find_outliers.py](/scripts/find_outliers.py) 

## Computation of a final score
How to ? - to fill

Independent metric, an array ? Or different weight should be attributed per metric ?

# Installation & Usage
## Get the data

```
cd data
curl -L https://figshare.com/ndownloader/files/34951602 -o group_data.tar
tar xvf group_data.tar
cd ..
```

## Check the data

```
python3 scripts/validate_data.py data
```

## Find outliers

```
python3 scripts/find_outliers.py data
```

This should print output to the terminal of form:

```
<filename>, <outlier_index>, <outlier_index>, ...
<filename>, <outlier_index>, <outlier_index>, ...
```

Where `<filename>` is the name of the image that has outlier scans, and
`<outlier_index>` is an index to the volume in the 4D image that you have
identified as an outlier.  0 refers to the first volume.  For example:

```
data/group-01/sub-01/func/sub-01_task-taskzero_run-01_bold.nii.gz, 3, 21, 22, 104
data/group-01/sub-01/func/sub-01_task-taskzero_run-02_bold.nii.gz, 11, 33, 91
data/group-01/sub-03/func/sub-03_task-taskzero_run-02_bold.nii.gz, 101, 102, 132
data/group-01/sub-08/func/sub-08_task-taskzero_run-01_bold.nii.gz, 0, 1, 2, 166, 167
data/group-01/sub-09/func/sub-08_task-taskzero_run-01_bold.nii.gz, 3
```
