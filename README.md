# CRTS_coadd
This is a repository for CRTS all-sky survey coadd
Here we present some extra information, which is not mentioned in teh paper.
The Appendix.pdf has some detailed information about the reasons due to which some images couldn't be included into the coadd.
In the Appendix we also compare limitting magnitude of outcome of coadding using different algorithm, and lastly a brief discussion on size of the coadded images

If 2 images are very far from each other (in sky location), their coadd will consist of a large spherical rectangle which circumscribe both the images. For images with large separation, the size of the coadd could be very large, hence several images images were discarded in order to limit the final output. Another reason could be having poor meta file, which we define as below.  

Due to some initial crashes the coadding process was divided into different phases and we share teh output of log files which contains information on which fields had at least one image rejected.

## Logfile in Phase 1:
*File name: wcs_error_list.txt
*Columns:
  1. Field - Name of the field
  2. wcs_err - Number of files whcih were rejected due to WCS not being approriate for the coadd
  3. tot - Total number of images in that field

## Logfile in Phase 2: 
*File name: scatter_list.txt
*Columns: 
  1. Field - Name of the field
  2. "Less scattered" - Among the images which are coadd-able, number of images which are clustered to small space in sky. (These are the images which were finally coadded)
  3. "Good WCS" - Number of Images whose WCS is approriate, but their position in sky may or may be as per requirement
  4. "Failed Mask" - Number of images which does not overlap exactly with the mask
  5. "Poor WCS" - Number of images whose WCS does not return any error while reading but is not similar to other images
  6. "Failed WCS" - Number of images whose WCS returned error while reading 
  7. tot - Total number of images in that field
  8. fr - Number of less scattered images / Total images (fraction of images which were coadded) (Rounded to 1 decimal)
  9. na - First character of the Field name. Usually the ones with value 'N' or 'S' have more science content, but for completeness we added 'F' and 'U' (explained in the paper)
