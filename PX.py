#!/usr/bin/env python3
import sys 
import os
import logging
import pickle
import numpy as np
import pandas as pd
import subprocess as sp
from volume import DicomVolume

# Each dataset, training or testing, consists three files: image csv, image_ktrans and findgs csv
if not os.path.exists('data/dcm_list.pickle'):
    sp.check_call('./scan_and_sanity_check.py', shell=True)
    pass
with open('data/dcm_list.pickle', 'rb') as f:
    dcm_list = pickle.load(f)
    pass

def load_images_csv (path):
    df = pd.read_csv(path, header = 0, index_col = None,
                dtype={'ProxID': str,   # e.g. ProstateX-0000
                       'Name': str,     # e.g. ep2d_diff_tra_DYNDIST_ADC0
                       'fid': int,      # finding ID
                       'pos': str,      # Scanner coordinate position of the finding
                                        # e.g. 25.7457 31.8707 -38.511
                       'WorldMatrix': str,
                                        # Matrix describing image orientation and scaling
                                        # e.g. 2,4.0067e-010,0.00377059,-46.6873,-0.000797221,1.89675,0.95144,-114.14,-0.00238396,-0.634294,2.84513,-18.0506,0,0,0,1
                       'ijk': str,      # Image column (i),row (j), and slice (k) coordinates of the finding.  Using the VTK/ITK/Python array convention, (0,0,0) represents the first column and first row of the first slice.
                                        # e.g. 36 72 9
                       'TopLevel': str, # 0-image  1-volume  NA-??
                       'SpacingBetweenSlices': float,   # 3
                       'VoxelSpacing': str, # 2,2,3
                       'Dim': str,      # 84x128x19x1
                       'DCMSerDescr': str, #  ep2d_diff_tra_DYNDIST_ADC
                       'DCMSerNum': int})
    for _, row in df.iterrows():
        prox = row['ProxID']
        if not row['DCMSerDescr'] in dcm_list[prox]:
            print(prox, row['DCMSerDescr'], 'not found')
            print(dcm_list[prox].keys())
    return df

def load_ktrans_csv (path):
    df = pd.read_csv(path, header = 0, index_col = None,
                dtype = {'ProxID': str,
                         'fid': int,
                         'pos': str,
                         'WorldMatrix': str,
                         'ijk': str})
    return df

def load_findings_csv (path):
    df = pd.read_csv(path, header = 0, index_col = None,
                dtype = {'ProxID': str,
                         'fid': int,
                         'pos': str,    # e.g. 25.7457 31.8707 -38.511
                         'zone': str,
                         'ClinSig': bool})   # TRUE/FALSE
    return df


def load_train_csv ():
    return load_images_csv('raw/ProstateX-TrainingLesionInformationv2/ProstateX-Images-Train.csv'), \
           load_ktrans_csv('raw/ProstateX-TrainingLesionInformationv2/ProstateX-Images-KTrans-Train.csv'), \
           load_findings_csv('raw/ProstateX-TrainingLesionInformationv2/ProstateX-Findings-Train.csv')

def load_test_csv ():
    return load_images_csv('raw/ProstateX-TestLesionInformation/ProstateX-Images-Test.csv'), \
           load_ktrans_csv('raw/ProstateX-TestLesionInformation/ProstateX-Images-KTrans-Test.csv'), \
           load_findings_csv('raw/ProstateX-TestLesionInformation/ProstateX-Findings-Test.csv')


if __name__ == '__main__':
    load_train_csv()
    load_test_csv()

