# SEBAL
Python code to run SEBAL method

---
bibliography: '/home/rafatieppo/Dropbox/BIBTEX/REFERENCES.bib'
css: sl
---

SEBAL model by means GRASS and PYTHON
=====================================

Motivation
----------

Now days it is noticed several occurrences about water shortage in
agriculture, decreasing yield crops and profits. The irrigation system
is a resource to aid the farmers to manage the system production to
achieve a reasonable yield. Among several variables for a irrigation
management, there are two of them with a major importance, the crop
coefficient (kc) and Reference crop evapotranspiration (ETo)
[@GONDIM2005TB].

In the last decades the remote sensing techniques has been used to
identify landscapes, soil classes, and water energy balance as well,
providing conditions to analyze data in a regional scale. By means
orbital sensors and algorithms to convert digital numbers to reflectance
and radiation flux, remotesensing methods to predict the
evapotranspiration is a important tool to handle the hydrological cycle
[@BERNARDO2006SM].

The SEBAL (Surface Energy Balance Algorithm for Land) uses the surface
energy balance to predict some hydrological features
(evapotranspiration, water deficit, etc) and Its main creator is
Professor Wim G. M. Bastiaanssen [@BASTIAANSSEN1998MFH]. That method has
been validated under several conditions for different locations
([@BASTIAANSSEN2000],[@BASTIAANSSEN2002AC], [@SANTOS210FA]).

There are several available algorithms to evapotranspiration prediction
([@WOLF2016SEBAL], [@CAVALCANTE2016IBJC], [@HESSELS2017OTB]). However is
missing a specific code to run on python 3 and GRASS 74. Thus we aimed
to implement SEBAL model for Landsat 8 iamges using the language Python
version 3 [@PYTHONR] and GRASS version 7.4 [@GRASS2012NB].

Requirements
------------

-   [GRASS GIS version 7.4](https://grass.osgeo.org/#)
    -   GRASS GUI
    -   GRASS DEV
-   Python 3.x, sugestion: [CONDA](https://anaconda.org/anaconda/python)

Make sure your system has Python Libraries: - math - numpy - os -
grass\_session - grass.script - osgeo

How to use
----------

1.  Download at Landsat 8 images (LS8 - OLI/TIRS)
2.  Reproject all the images (LS8 images) for the interested coordinate
    reference system (e.g. EPSG:32721)
3.  For all images remove null values
4.  Get Digital Elevation Model (DEM) from ASTER
5.  You must reproject the DEM file for the same coordinate reference
    system of interest, rename it as **MDT\_Sebal.TIF**
6.  Create a *GRASS* Session with GRASS-GIS software. You need to assign
    *GRASS location* and *GRASS Mapset*. Note that all maps must have
    the same coordinate reference system (projection). For further
    information about *GRASS* you can check
    [GRASS-GIS](https://grass.osgeo.org/).
7.  Make sure that all files are in the same folder, `SEBAL_v10.py`
    inclusive.
8.  Launch a text editor file and open `SEBAL_v10.py`. Find the lines
    **67, 68, 69**, you will find:

<!-- -->

    PERMANENT.open(gisdb='/home/rafatieppo/Documents/QGIS_SEBAL/20170904/',
                   location='sirgas2000utm21s',
                   create_opts='EPSG:31981')

Replace the text between quotes, e.g.:

    PERMANENT.open(gisdb='path for YOUR files',
                   location='YOUR folder location',
                   create_opts='YOUR reference coordinate system')

after that, save and close it.

10. If use Linux launch the *Terminal*, or if are Windows user launch
    *DOS Prompt*. Once you are in correct folder (that one with all your
    files) just run `python SEBAL_v10.py`, and insert the required
    values.

Notes
-----

Tested on Ubuntu 16.04 LTS

References
----------

<?xml version="1.0" encoding="utf-8"?>
<style xmlns="http://purl.org/net/xbiblio/csl" version="1.0" default-locale="en-US">
  <!-- Generated with https://github.com/citation-style-language/utilities/tree/master/generate_dependent_styles/data/elsevier -->
  <info>
    <title>Computers and Electronics in Agriculture</title>
    <id>http://www.zotero.org/styles/computers-and-electronics-in-agriculture</id>
    <link href="http://www.zotero.org/styles/computers-and-electronics-in-agriculture" rel="self"/>
    <link href="http://www.zotero.org/styles/elsevier-harvard" rel="independent-parent"/>
    <category citation-format="author-date"/>
    <issn>0168-1699</issn>
    <updated>2014-05-18T02:57:11+00:00</updated>
    <rights license="http://creativecommons.org/licenses/by-sa/3.0/">This work is licensed under a Creative Commons Attribution-ShareAlike 3.0 License</rights>
  </info>
</style>
