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
from matplotlib import pyplot as plt
import os
import nibabel as nib

def get_image(image_fname):
    """ Calculate TEMPORAL dvars metric on Nibabel image `img`

    The dvars calculation between two volumes is defined as the square root of
    (the sum of the (voxel differences squared) divided by the number of
    voxels).

    Parameters
    ----------
    image_fname : path to a nii image, like r".\data\group-00\sub-01\func\sub-01_task-taskzero_run-01_bold.nii.gz"

    Returns
    -------
    filename : name of the nii to rename rightly the output
    img : nibabel image
    data : from nibabel to be able to compute values
    """
    filename = os.path.basename(image_fname)  # get the name of the image
    img = nib.load(image_fname) #nibabel image
    data = img.get_fdata()

    return filename,img,data

def dvars(image_fname,plot=True):
    """ Calculate TEMPORAL dvars metric on Nibabel image `img`

    The dvars calculation between two volumes is defined as the square root of
    (the sum of the (voxel differences squared) divided by the number of
    voxels).

    Parameters
    ----------
    image_fname : path to a nii image, like r".\data\group-00\sub-01\func\sub-01_task-taskzero_run-01_bold.nii.gz"
    plot : boolean, true or false, true if you want the nii as outputs to check the function

    Returns
    -------
    dvals : 1D array
        One-dimensional array with n-1 elements, where n is the number of
        volumes in `img`.
    dvars_norm : dvals normalized
    dvars_median : median of dvals
    """
    # Hint: remember 'axis='.  For example:
    # In [2]: arr = np.array([[2, 3, 4], [5, 6, 7]])
    # In [3]: np.mean(arr, axis=1)
    # Out[2]: array([3., 6.])
    #
    # You may be be able to solve this in four lines, without a loop.
    # But solve it any way you can.

    filename,img,data=get_image(image_fname)

    voxel_per_time = np.reshape(data, (-1, data.shape[-1])) #np.reshape(data,new_shape)
    diff = np.diff(voxel_per_time)
    dvals = np.sqrt(np.mean(diff ** 2, axis=0))

    dvars_norm=dvals/np.std(diff, axis=0) #make sense ?
    dvars_median=np.median(dvals) #make sense ?

    if plot:
        # SAVING OUTPUTS
        print("AS FOR NOW in testing mode --> generating & saving outputs. Comment the lines below in the final code.")
        # Save as nii
        print("---Saving as nii dvars map. \nWill be in /output_for_tests/")
        # nib.Nifti1Image to convert to a spatial image
        nib.save(nib.Nifti1Image(dvals, img.affine),
                 os.path.join(os.getcwd(), 'output_for_tests', filename + "_desc-dvals.nii.gz"))

    return dvals,dvars_norm,dvars_median

def dvars_spatial(image_fname,plot=True):
    """ Calculate dvars metric on Nibabel image `img`

    The dvars calculation between two volumes is defined as the square root of
    (the sum of the (voxel differences squared) divided by the number of
    voxels).

    Parameters
    ----------
    image_fname : path to a nii image, like r".\data\group-00\sub-01\func\sub-01_task-taskzero_run-01_bold.nii.gz"
    plot : boolean, true or false, true if you want the nii as outputs to check the function

    Returns
    -------
    dvals : 1D array
        One-dimensional array with n-1 elements, where n is the number of
        volumnes in `img`.
    """

    filename,img,data=get_image(image_fname)

    voxel_per_z = np.reshape(data, (-1, data.shape[-2]))
    diff = np.diff(voxel_per_z)
    dvals = np.sqrt(np.mean(diff ** 2, axis=0))

    if plot:
        # SAVING OUTPUTS
        # Save as nii
        print("---Saving as nii dvars map across time. \nWill be in /output_for_tests/")
        # nib.Nifti1Image to convert to a spatial image
        nib.save(nib.Nifti1Image(dvals, img.affine),
                 os.path.join(os.getcwd(), 'output_for_tests', filename + "_desc-dvals-spatial.nii.gz"))

    return dvals

#def standardized_dvar(img):
    #https: // warwick.ac.uk / fac / sci / statistics / staff / academic - research / nichols / scripts / fsl / standardizeddvars.pdf

def basic_stats(image_fname,plot=True):
    """ Calculate basic stats metrics to be reused in different metrics
    for outlier detection

    Parameters
    ----------
    image_fname : path to a nii image, like r".\data\group-00\sub-01\func\sub-01_task-taskzero_run-01_bold.nii.gz"
    plot : boolean, true or false, true if you want the nii as outputs to check the function

    Returns
    -------
    mean_data : 3D array, nii image (x,y,z axis)
        Mean of the image over time
    sd_data : 3D array, nii image (x,y,z axis)
        Temporal deviation map, Standard deviation of the image over time

    meanmap_median : float, median of the mean nifti
    sdmap_median : float, median of the sd nifti
    """

    filename,img,data=get_image(image_fname)

    mean_data = np.mean(data,axis=-1)
    #mean of image on the 4th dim, time
    sd_data=np.std(data,axis=-1) #temporal deviation map

    # Median #make sense ?
    meanmap_median=np.median(mean_data)
    sdmap_median = np.median(sd_data)

    if plot:
        # SAVING OUTPUTS
        # Save as nii
        print("---Saving as nii mean map across time adn sd map. \nWill be in /output_for_tests/")
        # nib.Nifti1Image to convert to a spatial image
        nib.save(nib.Nifti1Image(mean_data, img.affine),os.path.join(os.getcwd(),'output_for_tests',filename+"_desc-meanmap-acrosstime.nii.gz"))
        nib.save(nib.Nifti1Image(sd_data, img.affine), os.path.join(os.getcwd(),'output_for_tests',filename+"_desc-sdmap-acrosstime.nii.gz"))

        # Save the middle plane of this mean volume as a png to read for easier visualisation
        print("---Save one slice of the mean map across time of the nii - for testing here + easier visualization. \nWill be in /output_for_tests/test_mean_map_acrosstime.png")
        fig = plt.figure()
        plt.imshow(mean_data[:, :, 14], cmap='gray')
        plt.title("Mean map across time - slice14")
        figure_to_save = os.path.join(os.getcwd(),'output_for_tests',filename+"_desc-meanmap-acrosstime-slice14.png")
        plt.savefig(figure_to_save)
        #plt.close(fig)

        print("---Save one slice of the sd map across time of the nii - for testing here + easier visualization.. \nWill be in /output_for_tests/test_sd_map_acrosstime.png")
        fig = plt.figure()
        plt.imshow(sd_data[:, :, 14], cmap='gray')
        plt.title("Standard deviation map across time - slice14")
        figure_to_save = os.path.join(os.getcwd(),'output_for_tests',filename+"_desc-sdmap-acrosstime-slice14.png")
        plt.savefig(figure_to_save)

    return mean_data,sd_data,meanmap_median,sdmap_median

def coefficient_of_variation(image_fname,plot=True):
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
    image_fname : path to a nii image, like r".\data\group-00\sub-01\func\sub-01_task-taskzero_run-01_bold.nii.gz"
    plot : boolean, true or false, true if you want the nii as outputs to check the function

    Returns
    -------

    """

    #test to do ?
    #assert

    filename,img,data=get_image(image_fname)

    mean_data,sd_data,meanmap_median,sdmap_median=basic_stats(image_fname)
    CV=np.where(mean_data == 0,0,np.divide(sd_data,mean_data))
    #return 0 if mean is 0

    if plot:
        # Save as nii
        print("AS FOR NOW in testing mode --> generating & saving outputs. Comment the lines below in the final code.")
        print("---Saving as nii coeff-of-variation. \nWill be in /output_for_tests/")
        # nib.Nifti1Image to convert to a spatial image
        nib.save(nib.Nifti1Image(CV, img.affine),
                 os.path.join(os.getcwd(), 'output_for_tests', filename + "_desc-coeff-of-variation.nii.gz"))

    # Median
    #not sure it makes a lot of sense, just a test here
    median_CV1=np.median(CV) #to have one value to plot for the dist
    median_CV2=np.where(mean_data == 0,0,np.median(sd_data)/np.median(mean_data)) #should be better

    return CV,median_CV1,median_CV2

#TO DO - average_bold_signal_across_time
# def average_bold_signal(img):
#     ...
#     return

#TO FINISH, need the average_bold_signal
def tSNR(image_fname,average_bold_signal_across_time,plot=True):
    """ Temporal SNR

        Parameters
        ----------
        image_fname : path to a nii image, like r".\data\group-00\sub-01\func\sub-01_task-taskzero_run-01_bold.nii.gz"
        plot : boolean, true or false, true if you want the nii as outputs to check the function

        Returns
        -------

        """
    filename,img,data=get_image(image_fname)

    mean_data,sd_data,meanmap_median,sdmap_median = basic_stats(image_fname)
    tSNR=average_bold_signal_across_time/sd_data #temporal variation tSNR
    tSNR_median=np.median(tSNR) #better than mean to not erase diff

    if plot:
        # Save as nii
        print("AS FOR NOW in testing mode --> generating & saving outputs. Comment the lines below in the final code.")
        print("---Saving as nii tSNR. \nWill be in /output_for_tests/")
        # nib.Nifti1Image to convert to a spatial image
        nib.save(nib.Nifti1Image(tSNR, img.affine),
                 os.path.join(os.getcwd(), 'output_for_tests', filename + "_desc-tSNR.nii.gz"))


    return tSNR,tSNR_median

def easy_masking(image_fname,value_mask,plot=True):
    """ For a quite masking of the background
        In case we cannot use nifti masker

        NB : USEFUL for : SNR of the background vs SNR of the head (normally brain
        but using this mask, might be difficult just to have the brain)


        Parameters
        ----------
        img : nibabel image
        value_mask : float for filtering

        Returns
        -------
        brain_mask : masked image with value set at 1 if voxel value > value_mask
        """
    #from nilearn.maskers import NiftiMasker

    filename,img,data=get_image(image_fname)

    brain_mask = np.where(img > value_mask, 1, 0)

    if plot:
        #all the value in the img above value_mask will be set to 1
        plt.imshow(brain_mask, cmap='gray')
        plt.axis('off')
        plt.show()
        # Save as nii
        print("AS FOR NOW in testing mode --> generating & saving outputs. Comment the lines below in the final code.")
        print("---Saving as nii mean map across time adn sd map. \nWill be in /output_for_tests/")
        # nib.Nifti1Image to convert to a spatial image
        nib.save(nib.Nifti1Image(brain_mask, img.affine),
                 os.path.join(os.getcwd(), 'output_for_tests', filename + "_desc-brain-mask.nii.gz"))

    return brain_mask

# def SNR(img):
#   #use masking
#     ...
#     return snr

#ideas
#https://nilearn.github.io/stable/auto_examples/06_manipulating_images/plot_compare_mean_image.html#sphx-glr-auto-examples-06-manipulating-images-plot-compare-mean-image-py
#can we do some registration using external toolbox ?

