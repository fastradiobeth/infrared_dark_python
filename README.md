# infrared_dark_python
basic python code and outputs for use with catalogues of Hi-GAL IRDC sources.

#####Known issues with IRDP

* Some (~5) pdf image files may be misplaced or missing due to rearrangements between categories. All cutouts and pdf files will be recreated for subcategories, with numbering from 0 in each category

* source_print.py fills up the matplotlib cache whilst running due to the use of TeX characters. This will likely cause disk quota problems on JBCA accounts (standard limit is 300MB, ~150MB used for full sample).

* source_print, cutsources and main are all currently set up for finding FITS files with non-exact coordinate matches in map names. This will introduce problems if multiple IRDC files are found with a catalogue map coordinate as a substring (e.g. a catalogue source listed as in map 350.898-0.9 will be matched to every IRDC FITS file with HGL350.898-0.9xx in the name). *This is currently unavoidable without failure on >50% of sources when cutting from files.* See full_sample_file_problems.pdf for more details.


Beth's favourite source is found at **infrared_dark_python/print_format_250_350_18.0asec/HGL28.087+0.067_160_quiet_printing_360.pdf**

All cutouts and full sample pdf files are available from scratch space. 

#### PDF source images key
-------------------------------------------------------
######Marker colours
* 70 microns - blue
* 160 microns - green
* 250 microns - red
* 350 microns - black

#### Misc. subsets of sources
-------------------------------------------------------

##### extinction at 70
  - This is the directory used for 160-quiet sources that show strong extinction at 70 microns, with both very obvious sources and sources that are less obvious but may be of interest.

##### interesting sources
  - This is the folder of sources found that fit various different subcategories within produced catalogues and suitably highlight differences betweeen objects found by the same find_counterparts_alpha run.
  - Description of sources is contained within the subdirectory

####160-quiet catalogues
--------------------------------------------------------
All catalogues are found in *./IRDC_catalogues*

1. *python_src_assoc_250_350_18.0asec* are the catalogues of 160-quiet sources in 15 < l < 55 contains 841 sources.
  - Sources in this catalogue are used when sorting 160-quiet sources into categories

2. *python_src_assoc_70_250_350_10.2asec* are the catalogues of 160-quiet sources with identified 70micron counterparts. Contains 30 sources, 15 < l < 55.

3. *full_sample_python_src_assoc_250_350_18asec_2015-09-18* are the 160-quiet catalogues of the full sample of IRDCs, with 4015 sources.

#####Categories
The sources in **python_src_assoc_250_350_18.0asec.dat** have been sorted into 4 broad categories and some subcategories from visual inspection. Note that this sorting should not be taken as entirely accurate and is sensitive to human judgement. The entire set of Galactic Longitude 15 < l < 55 has been sorted into the categories as shown in the diagram alongside the number of sources of each type. (If image does not display, the pdf and png versions are in this directory). 

![categories chart]
(https://github.com/fastradiobeth/infrared_dark_python/blob/master/quiet_at_160_categories.png)

Various plots in **plots/** show the longitude distribution of the 15<l<55 160-quiet catalogue, as well as the distributions of the categories and subcategories with some comparison to the multiwavelength Hyper catalogues starting *IRDC_l015_l055**.

Catelogues are in the *160_quiet_categories/* directory, with subdirectories containing the pdf images sorted into each main category- see note at top, subcategory directories will be created and missing sources recovered.

####protostellar catalogues
--------------------------------------------------------
all outputs for this section are located in *protostellar_comparison/*
A protostellar catalogue from IRDP has been compared to the Hyper catalogues of protostellar (70-350 presence) and starless (160-350 presence) clumps, with all comparison results shown in the diagram below: 
![protostellar chart]
(https://github.com/fastradiobeth/infrared_dark_python/blob/master/protostellar_catalogue_comparison.png)

All comparisons run using catalogue_compare_alpha.py. Catalogues 4, 5, and 6 are printed in the format of Catalogue 1.
Protostellar source catalogue was created using Hi-GAL wavelengths [70, 160, 250, 350]microns, 160microns as the reference wavelength and a maximum separation to be considered the same object of 10.2" (70micron beam). All fifferences between outputs have been studied and largely accounted for, as listed on the diagram.
