Notes

# PROSTATEx and PROSTATEx-2

## Data Overview

[TCIA Data Page](https://wiki.cancerimagingarchive.net/display/Public/SPIE-AAPM-NCI+PROSTATEx+Challenges#935fa28f51c546c588e892026a1396c6)

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

## Competition Links

PROSTATEx 2016-11-21 - 2017-02-16
- http://spiechallenges.cloudapp.net/competitions/6
- http://spiechallenges.cloudapp.net/forums/6/

PROSTATEx-2 2017-05-15 - 2017-08-03
- http://spiechallenges.cloudapp.net/competitions/7
- http://spiechallenges.cloudapp.net/forums/7/
- https://www.aapm.org/GrandChallenge/PROSTATEx-2/


## Misc Links
- [知乎: T1看解剖，T2看病变](https://www.zhihu.com/question/38567276/answer/152934823)

# DICOM Geometry

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


