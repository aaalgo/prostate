# Datasets
[TCIA Portal](http://www.cancerimagingarchive.net/)

## [Prostate-3T](https://wiki.cancerimagingarchive.net/display/Public/Prostate-3T)

This is the dataset of a [prostate segmentation challenge](https://wiki.cancerimagingarchive.net/display/Public/NCI-ISBI+2013+Challenge+-+Automated+Segmentation+of+Prostate+Structures).

- T2W MRI images, 3.0T Siemens TrioTim.

### Files
- `data/Prostate3T/MR`: MR images.
- `data/Prostate3T/CG_PZ`: segmentation of CG and PZ zones.
- `data/Prostate3T/SV_NVB`: segmentation of SV and NVB zones.


## [PROSTATEx and PROSTATEx-2](https://wiki.cancerimagingarchive.net/display/Public/SPIE-AAPM-NCI+PROSTATEx+Challenges#935fa28f51c546c588e892026a1396c6)

346 cases, each containing at least one biopsy-proved lesion.

All studies include the following kinds of images:
- T2W (T2-weighted): resolution 0.5mm, thickness 3.6mm.
- DCE (dynamic contrast enhanced): resolution 1.5mm, thickness 4mm, temporal 3.5s. Ktrans is computed from this.
- PD-W (proton density-weighted).  (same as DCE)
- DW (diffusion-weighted): 2mm, 3.5mm thickness. ADC images are computed from this.

The goal of PROSTATEx is to predict clinical significance (malignancy?) of lesions
(True/False).  Among the 350 cases, 60% is used for training and 40% is
used for testing.  Predictions are evaluated with the ROC AUC score.

The goal of PROSTATEx-2 is to predict [Gleason
score](https://en.wikipedia.org/wiki/Gleason_grading_system) of lesions.
Only 182 lesions, from 162 out of 346 cases, have Gleason sores (others
being benign or non-tumor). 112 is
used for training and the remaining 70 for testing.
Predictions are evaluated with quadratic-weighted Cohen’s kappa coefficient.

- [View Imported Positive Lesions](http://www.aaalgo.com/demos/prostate/view/pos)
- [View Imported Negative Lesions](http://www.aaalgo.com/demos/prostate/view/neg)

### Files:
- `data/PROSTATEx/MR`: MR images.
- `data/PROSTATEx/Ktrans`: Ktrans images.
- `data/PROSTATEx/*Information*`: labels and other meta data.

### TODO:
- Find PROSTATEx test set groundtruth.
- Find PROSTATEx-2 label data.

### Links

PROSTATEx 2016-11-21 - 2017-02-16
- http://spiechallenges.cloudapp.net/competitions/6
- http://spiechallenges.cloudapp.net/forums/6/

PROSTATEx-2 2017-05-15 - 2017-08-03
- http://spiechallenges.cloudapp.net/competitions/7
- http://spiechallenges.cloudapp.net/forums/7/
- https://www.aapm.org/GrandChallenge/PROSTATEx-2/

## Prostate Fused-MRI-Pathology(https://wiki.cancerimagingarchive.net/display/Public/Prostate+Fused-MRI-Pathology)

28 cases with

- T1, T2, DW and DCE MRI images.
- H&E histopathology images
  * sectioned & quartered, 4 slides for each section.
  * 4 slides/section, scanned 20x with Aperio slide scanner into 4. svs images.
  * stitched to make .tiff

## [TCGA-PRAD](https://wiki.cancerimagingarchive.net/display/Public/TCGA-PRAD)

- 14 patients with CT, PT and MR.
- Clinical data at [GDC Data
  Portal](https://gdc-portal.nci.nih.gov/projects/t?filters=%7B%22op%22:%22and%22,%22content%22:%5B%7B%22op%22:%22in%22,%22content%22:%7B%22field%22:%22program.name%22,%22value%22:%5B%22TCGA%22%5D%7D%7D%5D%7D) 


## [NaF Prostate](https://wiki.cancerimagingarchive.net/display/Public/NaF+Prostate)
- PET/CT

## [PROSTATE-DIAGNOSIS](https://wiki.cancerimagingarchive.net/display/Public/PROSTATE-DIAGNOSIS)

- 92 patients
- T1, T2 and DCE


## Other Datasets with Limited Access

-[Qin Prostate](http://dx.doi.org/10.7937/K9/TCIA.2016.fADs26kG)
-[Prostate-MRI](http://dx.doi.org/10.7937/K9/TCIA.2016.6046GUDv)


# DICOM Geometry

[Coordinate Systems](https://www.slicer.org/wiki/Coordinate_systems)
[DICOM Fields](ftp://dicom.nema.org/MEDICAL/dicom/2015b/output/chtml/part03/sect_C.7.6.2.html)

- World coordinate: X = (x, y, z)
- ijk coordinate: i-column, j-row, k-slice.  Sort all dicoms by
  InstanceNumber and k is the 0-based index.
- World matrix (wm):     col(x, y, z, 1) = wm x col(i, j, k, 1)
- O = dcm.ImagePositionPatient: world coordinate of pixel (0,0)
- dirI, dirJ = dcm.dcm.ImageOrientationPatient: direction of first row
  and first column.
- spJ, spI = dcm.PixelSpacing
- i = dot(X-O, dirI) / spI
- j = dot(X-O, dirJ) / spJ

# Prostate Anatomy

- [Zone Explanation](http://www.cancer.ca/en/cancer-information/cancer-type/prostate/prostate-cancer/the-prostate/?region=on)
- [Zone Explanation 2](https://www.earthslab.com/anatomy/prostate/)

- AS: anterior fib. stroma ??
- PZ: peripheral zone
- SV: seinal vesical
- TZ: transition zone
- CZ: central zone (not seen in data)

# Links
- [TCIA](http://www.cancerimagingarchive.net/)
- [知乎: T1看解剖，T2看病变](https://www.zhihu.com/question/38567276/answer/152934823)

