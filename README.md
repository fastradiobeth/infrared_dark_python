# infrared_dark_python
basic python code and outputs for use with catalogues of Hi-GAL IRDC sources.
FITS cutouts of images have not been uploaded due to directory restrictions.

Some (~5) pdf image files may be misplaced or missing due to rearrangements between categories. This will be ammended shortly.

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
infrared_dark_python/find_counterparts_alpha.py outputs of sources detected in at least [250, 350] microns with no presence in 160 microns.

1. **python_src_assoc_250_350_18.0asec.dat** and **python_src_assoc_250_350_18.0asec_full.dat**
  - uses minimum required wavelength beam (18.0", 250 microns), reference wavelength 250 microns, and does not check for 70 micron sources.
  - Contains 841 sources.
  - Sources in this catalogue are used when sorting 160-quiet sources into categories

2. **python_src_assoc_70_250_350_10.2asec.dat** and **python_src_assoc_70_250_350_10.2asec_full.dat**
  - uses minimum required wavelength beam (10.2", 70 microns), reference wavelength 250 microns.
  - Contains 30 sources.

####160-QUIET CATEGORIES
--------------------------------------------------------
The sources in **python_src_assoc_250_350_18.0asec.dat** have sorted into 4 broad categories from visual inspection. Note that this sorting should not be taken as entirely accurate and is sensitive to human judgement. The entire set of Galactic Longitude 15 < l < 55 has been sorted into the main categories.

The longitude distributions of the 4 different categories are shown in **longitude_IRDP_categories** and **longitude_IRDP_categories_stacked**, located in **plots/**. The longitude distribution of the 160-quiet set of all 841 sources is shown alongside the distributions of the *Hyper* starless and protostellar sets in **longitude_hyper_vs_IRDP_10bins**.

#####Category I: Appears quiet at 160
  - Defined as showing no/very weak emission at 160 microns, and present in 250 and 350. All sources showed no bright features at 70 microns. The subcategories specify whether the source is quiet or appears as a similarly shaped* dark feature at 70 microns. 
  - Contains 358 sources (42.6%)

######Subcategories (full set)
    i. Dark at 70 (86 sources)
    ii. Quiet at 70 (272 sources)

#####Category II: Appears bright at 160
  - Shows emission at 160 microns that appears to be related to the 250 and 350 counterparts. 70 micron state is not specified.
  - Comparison plots between the Hyper and IRDP protostellar and starless data sets are located in **plots/**
  - Contains 230 sources (27.3%)

######Subcategories (full set)
    i. Appears quiet or dark at 70 microns [starless] (185)
    ii. Appears bright at 70 [protostellar] (24 sources)
    iii. Ambiguous at 70 (21 sources)

#####Category III: Ambiguous at 160
  - The source may appear 'quieter' but still visible at 160 microns, or it may not be clear whether the 160 micron emission is related to the clump, leading to ambiguity in whether a source is quiet at 160. 
  - Contains 119 sources (14.1%)

#####Category IV: Unclassified
  - Some sources are very difficult to classify due to other bright features nearby. Some sources listed in a given map may also be outside the border, and therefore are not actually visible in the map. These are the two subcategories below.
  - Contains 134 sources (15.9%)

######Subcategories (full set)
    i. Map problems (25 sources) - 3.0% of entire set
    ii. Other bright feature(s) nearby (109 sources) - 13.0% of entire set

Catelogues are within the **infrared_dark_python/160_quiet_categories** directory, with subdirectories containing the pdf images created by **source_print.py** in each category. More sources and subcategories coming soon...

*Note that 'similarly shaped' implies that this sorting should be taken as an estimate rather than an absolute.

####PROTOSTELLAR CATALOGUES
--------------------------------------------------------
all outputs related for this section are located in **infrared_dark_python/protostellar_comparison/**
infrared_dark_python/find_counterparts_alpha.py protostellar catalogue has been compared to the Hyper catalogues of protostellar (70-350 presence) and starless (160-350 presence) sources and the following catalogues produced:

1. **python_src_assoc_70_160_250_350_10.2asec.dat**
  - output from find_counterparts_alpha.py of all sources with counterparts found in all four wavelengths. glon and glat of each counterpart centroid are printed, with one row per source.
  - Contains 1200 sources.
      
2. **python_src_assoc_70_160_250_350_10.2asec_full.dat**
  - output from find_counterparts_alpha.py of all sources with counterparts found in all four wavelengths. One row is used per wavelength band per source. Contains glon, glat, ra, dec and distance of source from reference wavelength centroid.
  - Contains 1200 sources.
      
3. **protostellar_hyper_proto_not_found.dat**
  - catalogue of Hyper protostellar sources not recovered by find_counterparts_alpha.py, in format of original Hyper catalogue.
  - Comparison used 70micron coordinates.
  - Contains 49 sources.

4. **protostellar_agreed_sources.dat**
  - catalogue of find_counterparts_alpha.py protostellar sources also found in Hyper protostellar catalogue.
  - Comparison used 70micron coordinates.
  - Contains 993 sources. 

5. **protostellar_misclassified_sources.dat**
 - catalogue of find_counterparts_alpha.py protostellar objects not appearing in Hyper protostellar catalogue but found in Hyper starless catalogue.
 - Comparisons against Hyper protostellar and starless catalogues used 70micron and 160micron coordinates respectively.
 - Contains 65 sources. 

6. **protostellar_extra_sources.dat**
  - catalogue of extra protostellar sources found by find_counterparts_alpha.py, appearing in neither the starless or protostellar Hyper catalogues. 
  - Comparisons run against Hyper protostellar and starless used 70micron and 160micron coordinates respectively.
  - Contains 142 sources.
      

All comparisons run using catalogue_compare_alpha.py. Catalogues 4, 5, and 6 are printed in the format of Catalogue 1.
Protostellar source catalogue was created using Hi-GAL wavelengths [70, 160, 250, 350]microns, 160microns as the reference wavelength and a maximum separation to be considered the same object of 10.2" (70micron beam).
