# CRTS coadd 
This is a repository regarding the co-additions of the CRTS all-sky survey. 
Here we present some extra information, which is not mentioned in the paper. It also contains all the necessary files (and some temporary files) required to recreate the work (users must have a separate access to the raw CRTS images).

The **Appendix.pdf** has some detailed information about the reasons due to which some images couldn't be included into the co-add.
In the Appendix we also compare the limiting magnitude of outcome of coadding using different algorithms, and lastly a brief discussion on size of the coadded images and its importance. 

If 2 images are very far from each other (in sky location), their coadd will consist of a large spherical rectangle which circumscribes both the images. For images with large separation, the size of the coadd could be very large, hence several images were discarded in order to limit the size of the final output. Another reason for discarding an image could be, having a poor meta file, which we defined as a description for the columns of **scatter_list.txt** .  

Due to some initial crashes the coadding process was divided into different phases and we share the output of log files which contains information on which fields had at least one image rejected. Also, if a final output co-add file was greater than 700MB, they were deleted and were co-added again without scattered images in Phase-2.


## Files necessary to reproduce CRTS co-addition
  * **CRTS_id_num.txt** - Contains 2 columns, one containing the names of the field and other the total number of images taken for that field. Out of the total number of images available only those were co-added which were not rejected for either poor meta-data and/or their separation from the rest of the images. Higher the number of images used in the co-add, the deeper the co-add will be in terms of limited magnitude. There are a total of 7894 fields and 798388 total images available for co-add (sum of 2nd column). However not all images were used in co-add.
  
  * **bsub_CRTS.py** - Co-adding all the ~8000 CRTS fields is computationally demanding for a single CPU, hence it is advised to distribute the workload to multiple CPUs in parallel, where 1 CPU co-adds 1 field at a time. It is less time efficient to allot multiple CPUs for single field co-add as compared to 1 CPU per field. Since for this study we had a different server for the storage ~0.8 million CRTS images and a different server to be used to co-add them, some of the functions are dedicated to moving data at the correct place. Hence some users may have to modify those functions accordingly. As per the current structure of the code, along with this code, the user would need CRTS_id_num.txt/CRTS_id_num_R.txt, swarp_conf_varun.swarp and all the necessary images to be co-added along with Mask_S.fits in a same directory.  Users must make sure they modify the addresses in the code accordingly. 
  
  * **sc_CRTS_new.py** - As discussed, images which are separated very far apart are not co-added as it will significantly increase the output size and will have no incremental scientific value in terms of depth/limiting magnitude of the image. Hence the fields which were deleted in Phase-1 run, were co-added by the newer code, which ignore the scattered images more efficiently. This code has more detailed log system and 
  
  * **swarp_conf_varun.swarp** - It is a modified version of default configuration files necessary for SWarp software. These configuration parameters will be overwritten when the SWarp command is given additional flags. The python code allows the user to modify some of the useful configuration. The reason for the choices of the parameters have been explained in the paper.
  
  * [**Mask_S.fits**](https://drive.google.com/file/d/1ocMkvuA4lURhDvn7RexaMpjFlWUZUxtn/view?usp=sharing) - Not all of the pixels of the camera (CCD) records the light correctly and some are rather dead, hence one has to mask out those pixels by giving them zero weights.  
  
## Software tools necessary to reproduce/analyse CRTS co-add
 * [SWarp](https://github.com/astromatic/swarp)
 * [SExtractor](https://www.astromatic.net/software/sextractor)
 * Optional: [Montage](http://montage.ipac.caltech.edu/docs/index.html)
  
### Logfiles in Phase-1:
 * File name: **wcs_error_list.txt**
   * Contains the list of all the fields which had at least one image which was rejected due to incompatible WCS. The number of such images and total images in the field are also stored
   * Columns:
   1. "Field" - Name of the field
   2. "wcs_err" - Number of files which were rejected due to WCS not being appropriate for the coadd
   3. "tot" - Total number of images in that field
  
 * File name: **Coadd_FAIL.txt**
   * List of all the fields which failed the co-addition process in the Phase-1, while running bsub_CRTS.py. This file was meant to be both human readable and machine readable. Along with the fields the columns also store the time taken to run (failed) co-adding command, the total time taken by process the field, along with the date and time of execution
   * Columns:
   1. Field - Name of the field that failed during co-addition
   2. F - Redundant: for human readability. Signifies that this field failed
   3. C - Redundant: for human readability. Signifies Coadd-time
   4. Co-T - Time taken (in sec) to run (failed) co-adding command
   5. T - Redundant: for human readability. Signifies Total Time Taken (TTT)
   6. To-T - total time taken by process the field (in sec)


### Logfiles in Phase-2: 
 * File name: **scatter_list.txt**
  * Columns: 
   1. "Field" - Name of the field
   2. "Less scattered" - Among the images which are coadd-able, number of images which are clustered to small space in sky. (These are the images which were finally coadded)
   3. "Good WCS" - Number of Images whose WCS is appropriate, but their position in sky may or may be as per requirement
   4. "Failed Mask" - Number of images which does not overlap exactly with the mask
   5. "Poor WCS" - Number of images whose WCS does not return any error while reading but is not similar to other images
   6. "Failed WCS" - Number of images whose WCS returned error while reading 
   7. "tot" - Total number of images in that field
   8. "fr" - Number of less scattered images / Total images (fraction of images which were coadded) (Rounded to 1 decimal)
   9. "na" - First character of the Field name. Usually the ones with value 'N' or 'S' have more science content, but for completeness we added 'F' and 'U' (explained in the paper)
 * File name: **Sc_Coadd_FAIL.txt**
  * List of all the fields which were removed in Phase-1 but could not successfully co-add in the Phase-2 either, while running sc_CRTS_new.py. This file was meant to be both human readable and machine readable. Along with the fields the columns also store the time taken to run (failed) co-adding command, the total time taken by process the field, along with the date and time of execution
  * Columns:
  1. Field - Name of the field that failed during co-addition
  2. F - Redundant: for human readability. Signifies that this field failed
  3. C - Redundant: for human readability. Signifies Coadd-time
  4. Co-T - Time taken (in sec) to run (failed) co-adding command
  5. T - Redundant: for human readability. Signifies Total Time Taken (TTT)
  6. To-T - total time taken by process the field (in sec)
  7. date - Date of execution
  8. time - Time of execution
 * File name: **SSE_Coadd_FAIL.txt**
  * List of all the fields which failed in Phase-1 due to ssh/scp error but could not successfully co-add in the Phase-2, while running sc_CRTS_new.py. This file was meant to be both human readable and machine readable. Along with the fields the columns also store the time taken to run (failed) co-adding command, the total time taken by process the field, along with the date and time of execution
  * Columns:
  1. Field - Name of the field that failed during co-addition
  2. F - Redundant: for human readability. Signifies that this field failed
  3. C - Redundant: for human readability. Signifies Coadd-time
  4. Co-T - Time taken (in sec) to run (failed) co-adding command
  5. T - Redundant: for human readability. Signifies Total Time Taken (TTT)
  6. To-T - total time taken by process the field (in sec)
  7. date - Date of execution
  8. time - Time of execution
 * File name: **FITS.txt**
  * output of `ls -lh *fits` in the directory where all the final co-adds are stored. Size of the co-add can be a pseudo measure for the quality of the co-add image, which is explained in the paper as well. 
 * File name: **CORD_coord.txt**
  * This file contains all 4 corner coordinates (RA,Dec) in degrees and the center RA, Dec of all teh co-added fields. 
  * Columns
   * Field - Name of the field
   * r1, d1, r2, d2, r3, d3, r4, d4, r0, d0 - 5 sets RA,Dec (ri,di, for i ->0,1,2,3,4) of each co-added image
   * CT - Actual number of co-added images for that field
   * CN - Total number of images in CRTS repository for that field 
    
