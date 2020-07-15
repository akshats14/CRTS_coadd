# CRTS coadd 
This is a repository regarding the co-additions of the CRTS all-sky survey. 
Here we present some extra information, which is not mentioned in the paper. It also contains all the necessary files (and some temporary files) required to recreate the work (user must have a separate access to the raw CRTS images).

The **Appendix.pdf** has some detailed information about the reasons due to which some images couldn't be included into the coadd.
In the Appendix we also compare limitting magnitude of outcome of coadding using different algorithm, and lastly a brief discussion on size of the coadded images and its importance. 

If 2 images are very far from each other (in sky location), their coadd will consist of a large spherical rectangle which circumscribes both the images. For images with large separation, the size of the coadd could be very large, hence several images were discarded in order to limit the size of the final output. Another reason for discarding the an image could be, having a poor meta file, which we defined as description for the columns of **scatter_list.txt** .  

Due to some initial crashes the coadding process was divided into different phases and we share the output of log files which contains information on which fields had at least one image rejected. Also, if a final output co-add file was greater than 700MB, they were deleted and were co-added again without scattered images in Phase-2.


## Files necessary to reproduce CRTS co-addition
  * CRTS_id_num.txt
    * Contains 2 columns, one containing the names of the field and other the total number of images taken for that field. Out of the total number of images available only those were co-added which were not rejected for either poor meta-data and/or their seperation from the rest of the images. Higher the number of images used in the co-add, the deeper the co-add will be in terms of limitted magnitude. There are total 7894 fields and 798388 total images available for co-add (sum of 2nd column). Hwever not all images were used in co-add.
  * bsub_CRTS.py
    * Co-adding all the ~8000 CRTS fields is computatioanally demanding, there 
  * sc_CRTS_new.py
  * swarp_conf_varun_edit.swarp
  * [Mask_S.fits](https://drive.google.com/file/d/1ocMkvuA4lURhDvn7RexaMpjFlWUZUxtn/view?usp=sharing)
  
### Logfiles in Phase 1:
* File name: **wcs_error_list.txt**
  * Columns:
   1. "Field" - Name of the field
   2. "wcs_err" - Number of files whcih were rejected due to WCS not being approriate for the coadd
   3. "tot" - Total number of images in that field
  
* File name: **Coadd_FAIL.txt**
  * Columns:
   1. Field 
   2. F 
   3. C 
   4. Co-T 
   5. T 
   6. To-T 


### Logfiles in Phase 2: 
* File name: **scatter_list.txt**
  * Columns: 
  1. "Field" - Name of the field
  2. "Less scattered" - Among the images which are coadd-able, number of images which are clustered to small space in sky. (These are the images which were finally coadded)
  3. "Good WCS" - Number of Images whose WCS is approriate, but their position in sky may or may be as per requirement
  4. "Failed Mask" - Number of images which does not overlap exactly with the mask
  5. "Poor WCS" - Number of images whose WCS does not return any error while reading but is not similar to other images
  6. "Failed WCS" - Number of images whose WCS returned error while reading 
  7. "tot" - Total number of images in that field
  8. "fr" - Number of less scattered images / Total images (fraction of images which were coadded) (Rounded to 1 decimal)
  9. "na" - First character of the Field name. Usually the ones with value 'N' or 'S' have more science content, but for completeness we added 'F' and 'U' (explained in the paper)
  

 * File name: **Sc_Coadd_FAIL.txt**
   * Columns:
   1. Field 
   2. F 
   3. C 
   4. Co-T 
   5. T 
   6. To-T 
   7. date 
   8. time
 
 * File name: **SSE_Coadd_FAIL.txt**
   * Columns:
   1. Field 
   2. F 
   3. C 
   4. Co-T 
   5. T 
   6. To-T 
   7. date 
   8. time
 
 * File name: **FITS.txt**
 output of `ls -lh *fits` in the directory where all the final co-adds are stored. 
 * File name: **CORD_coord.txt**
   * Columns
     * Field 
     * r1, d1, r2, d2, r3, d3, r4, d4, r0, d0
     * CT
     * CN

