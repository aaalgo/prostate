[Data Source](https://wiki.cancerimagingarchive.net/display/Public/SPIE-AAPM-NCI+PROSTATEx+Challenges#935fa28f51c546c588e892026a1396c6)


All studies include the following imaging methods:

T2W (T2-weighted): resolution 0.5mm, thickness 3.6mm.

PD-W (proton density-weighted):  (same as DCE)

DCE (dynamic contrast enhanced): resolution 1.5mm, thickness 4mm,
temporal 3.5s.
	(Ktrans computed from this)

DW (diffusion-weighted): 2mm, 3.5mm thickness
	(ADC images computed from this)

Challenge Notes:

Each case will contain at least one prostate lesion with biopsy-proven
malignancy status or with imaging findings with sufficiently low
suspicion of clinical significance.

 Lesion locations will be provided, but Gleason scores and PI_RADS
 scores will not be released with this challenge,
 
http://spiechallenges.cloudapp.net/competitions/6
http://spiechallenges.cloudapp.net/competitions/7

challenges:
- PROSTATEx 2016-11-21 - 2017-02-16
- PROSTATEx-2 2017-05-15 - 2017-08-03

Misc links
[知乎: T1看解剖，T2看病变](https://www.zhihu.com/question/38567276/answer/152934823)


Tasks:
- Predict level of suspicion
- Gleason Grade Group for each case (lesion) 
  quadratic-weighted Cohen’s kappa coefficient of agreement with the
  reference standard Gleason Grade Group for each lesion.

  tie-breaker: ability to identify Gleason grade > 1



Challenge:	PROSTATEx
	350 cases, 60% training, 40% testing
	each case contains at least one prostate lesion with biopsy-proved
	(Gleason & PI-RADS hide out for follow-up challenge)

	http://spiechallenges.cloudapp.net/competitions/6
	http://spiechallenges.cloudapp.net/forums/6/

Challenge:  PROSTATEx-2

	162 cases, 182 lesions (112 + 70); subset of PROSTATEx challenge
	(train is subset of train, test is subset of test)

	Please note that the findings from PROSTATEx that are not included
	in PROSTATEx-2 are findings for which Gleason Grade Group assignment
	is not possible (they are benign or non-tumor).

	http://spiechallenges.cloudapp.net/competitions/7
	http://spiechallenges.cloudapp.net/forums/7/
	https://www.aapm.org/GrandChallenge/PROSTATEx-2/

	

		
