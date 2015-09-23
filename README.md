# infrared_dark_python
basic python code and outputs for use with catalogues of Hi-GAL IRDC sources.

#####Known issues with IRDP

* FITS cutouts of images have not been uploaded due to directory restrictions on number of files per directory
* Original IRDC cloud FITS files are also not present due to size and number
* pdf versions of the sources found in the full galactic longitude run have not been uploaded due to the number (~4000)

*All of the above are available from scratch space if requested.*

* Some (~5) pdf image files may be misplaced or missing due to rearrangements between categories. All cutouts and pdf files will be recreated for subcategories, with numbering from 0 in each category
* A large number of files have been renamed and moved to and from scratch space and pulls may take longer than expected
* source_print.py fills up the matplotlib cache whilst running due to the use of TeX characters. This will likely cause disk quota problems on JBCA accounts (standard limit is 300MB) when used to produce large numbers of pdf files, even if the output is to scratch space or external storage
* source_print, cutsources and main are all currently set up for finding FITS files with non-exact coordinate matches in map names, due to clipping of decimal places in the Hyper single wavelength catalogues in use. This will introduce problems if multiple IRDC files are found with a catalogue map coordinate as a substring (e.g. a catalogue source listed as in map 350.898-0.9 will be matched to every IRDC FITS file with HGL350.898-0.9xx in the name). *this is currently unavoidable without failure on >50% of sources when cutting from files*


Beth's favourite source is found at **infrared_dark_python/print_format_250_350_18.0asec/HGL28.087+0.067_160_quiet_printing_360.pdf**

#### SOURCE IMAGES
-------------------------------------------------------
######Marker colours
* 70 microns - blue
* 160 microns - green
* 250 microns - red
* 350 microns - black

#####1. **160-quiet sources**
  - The print format pdf files of all sources in **python_src_assoc_250_350_18.0asec.dat** are stored here, in the same order of appearance as the catalogue. The source images can be found in categories in 160_quiet_categories.
  - Note: some sources do not fit within boundaries of assigned map and may not be visible. Source 663 is also missing due to an unresolved issue whilst formatting the FITS file.

#####3. **'misclassified' protostellar sources**
  - print format images of the 65 sources found protostellar by find_counterparts but appear in the starless Hyper catalogue are in **protostellar_comparison/misclassified_print** 

#####2. **interesting sources**
  - This is the folder of sources found that fit various different subcategories within produced catalogues and suitably highlight differences betweeen objects found by the same find_counterparts_alpha run.
  - Description of sources is contained within the subdirectory

####160-QUIET CATALOGUES
--------------------------------------------------------

1. **python_src_assoc_250_350_18.0asec.dat** and **python_src_assoc_250_350_18.0asec_full.dat**
  - uses minimum required wavelength beam (18.0", 250 microns), reference wavelength 250 microns, and does not check for 70 micron sources.
  - Contains 841 sources.
  - Sources in this catalogue are used when sorting 160-quiet sources into categories

2. **python_src_assoc_70_250_350_10.2asec.dat** and **python_src_assoc_70_250_350_10.2asec_full.dat**
  - uses minimum required wavelength beam (10.2", 70 microns), reference wavelength 250 microns.
  - Contains 30 sources.


####160-QUIET CATEGORIES
--------------------------------------------------------
The sources in **python_src_assoc_250_350_18.0asec.dat** have been sorted into 4 broad categories and some subcategories from visual inspection. Note that this sorting should not be taken as entirely accurate and is sensitive to human judgement. The entire set of Galactic Longitude 15 < l < 55 has been sorted into the categories as shown in the diagram alongside the number of sources of each type. (If image does not display, the pdf and png versions are in this directory). 

![categories chart]
(https://github.com/fastradiobeth/infrared_dark_python/blob/master/quiet_at_160_categories.png)

Various plots in **plots/** show the longitude distribution of the 15<l<55 160-quiet catalogue, as well as the distributions of the categories and subcategories with some comparison to the multiwavelength Hyper catalogues starting *IRDC_l015_l055**.

Catelogues are in the *160_quiet_categories/* directory, with subdirectories containing the pdf images sorted into each main category- see note at top, subcategory directories will be created and missing sources recovered.

####PROTOSTELLAR CATALOGUES
--------------------------------------------------------
all outputs for this section are located in *protostellar_comparison/*
A protostellar catalogue from IRDP has been compared to the Hyper catalogues of protostellar (70-350 presence) and starless (160-350 presence) clumps, with all comparison results shown in the diagram below: 
![protostellar chart]
(https://github.com/fastradiobeth/infrared_dark_python/blob/master/protostellar_catalogue_comparison.png)

All comparisons run using catalogue_compare_alpha.py. Catalogues 4, 5, and 6 are printed in the format of Catalogue 1.
Protostellar source catalogue was created using Hi-GAL wavelengths [70, 160, 250, 350]microns, 160microns as the reference wavelength and a maximum separation to be considered the same object of 10.2" (70micron beam). All fifferences between outputs have been studied and largely accounted for, as listed on the diagram.
