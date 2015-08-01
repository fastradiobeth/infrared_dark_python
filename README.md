# infrared_dark_python
basic python code for use with catalogues of Hi-GAL IRDC sources

Beth's favourite source is found at **infrared_dark_python/print_format_250_350_18.0asec/HGL28.087+0.067_160_quiet_printing_360.pdf**

#### SOURCE IMAGES
-------------------------------------------------------
######Marker colours
* 70 microns - blue
* 160 microns - green
* 250 microns - red
* 350 microns - black

#####1. **160-quiet sources**
  - The print format pdf files of all sources in **python_src_assoc_250_350_18.0asec.dat** are stored here, in the same order of appearance as the catalogue.
  - Note: some sources do not fit within boundaries of assigned map and may not be visible. Source 663 is also missing due to an unresolved issue whilst formatting the FITS file.

#####3. **'misclassified' protostellar sources**
  - print format images of the 65 sources found protostellar by find_counterparts but appear in the starless Hyper catalogue

#####2. **interesting sources**
  - This is the folder of sources found that fit various different subcategories within produced catalogues and suitably highlight differences betweeen objects found by the same find_counterparts_alpha run.
  - Description of sources is contained within the subdirectory

####160-QUIET CATALOGUES
--------------------------------------------------------
infrared_dark_python/find_counterparts_alpha.py outputs of sources detected in at least [250, 350] microns with no presence in 160 microns.

1. **python_src_assoc_250_350_18.0asec.dat** and **python_src_assoc_250_350_18.0asec_full.dat**
  - uses minimum required wavelength beam (18.0", 250 microns), reference wavelength 250 microns, and does not check for 70 micron sources.
  - Contains 841 sources.

2. **python_src_assoc_70_250_350_10.2asec.dat** and **python_src_assoc_70_250_350_10.2asec_full.dat**
  - uses minimum required wavelength beam (10.2", 70 microns), reference wavelength 250 microns.
  - Contains 30 sources.


####PROTOSTELLAR CATALOGUES
--------------------------------------------------------
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
