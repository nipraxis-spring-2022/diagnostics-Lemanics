
import nibabel as nib
import numpy as np
from matplotlib import pyplot as plt

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


def easy_masking(img,value_mask,plot=True):
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

    data=img.get_fdata()

    brain_mask = np.where(data > float(value_mask), 1, 0)

    if plot:
        #all the value in the img above value_mask will be set to 1
        #plt.imshow(brain_mask, cmap='gray')
        # Save as nii
        print("AS FOR NOW in testing mode --> generating & saving outputs. Comment the lines below in the final code.")
        print("---Saving as nii mean map across time adn sd map. \nWill be in /output_for_tests/")
        # nib.Nifti1Image to convert to a spatial image
        nib.save(nib.Nifti1Image(brain_mask, img.affine),
                 os.path.join(os.getcwd(), 'output_for_tests', filename + "_desc-brain-mask.nii.gz"))

    return brain_mask