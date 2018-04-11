#!/usr/bin/env python3
import sys 
import os
import logging
import pickle
import numpy as np
import pandas as pd
import subprocess as sp
from volume import DicomVolume

class Finding:
    # one lesion, with multiple views

    def __init__ (self, row):            # construct from a row from finding csv table
        self.ProxID = row['ProxID']      # patient ID
        self.fid = row['fid']            # finding ID
                                         # (ProxID, fid) is unique
        self.pos = np.array([float(x) for x in row['pos'].strip().split(' ')])
        self.zone = row['zone']
        self.ClinSig = row['ClinSig']
        self.views = {'T2_cor': [], # pattern "^t2_" and "cor"
                      'T2_sag': [], #                    "sag"
                      'T2_tra': [], #                 and others
                      'PD': [], # pattern "PD" or "dynamisch"
                      'DW': [], # pattern "diff" but not "t2"
                      'others': []
                      }
        pass

    def add_image (self, row):          # add a row from the image csv table
        view = None
        name = row['DCMSerDescr']
        # determine view name
        if 't2' in name:
            if 'cor' in name:
                view = 'T2_cor'
            elif 'sag' in name:
                view = 'T2_sag'
            else:
                view = 'T2_tra'
                pass
        elif 'diff' in name:
            view = 'DW'
        elif 'PD' in name or 'dynamisch' in name:
            view = 'PD'
        else:
            view = 'others'

        assert row['ProxID'] == self.ProxID
        assert row['fid'] == self.fid
        pos = np.array([float(x) for x in row['pos'].strip().split(' ')])
        if not np.all(pos == self.pos):
            print('these should equal')
            print(pos)
            print(self.pos)
        self.views[view].append(row)
        pass
    pass


# Each dataset, training or testing, consists three files: image csv, image_ktrans and findgs csv
if not os.path.exists('data/dcm_list.pickle'):
    # scan all dicom files
    sp.check_call('./scan_and_sanity_check.py', shell=True)
    pass
with open('data/dcm_list.pickle', 'rb') as f:
    dcm_list = pickle.load(f)
    pass

def sanity_check_coord (row):
    # each lesion has an ijk index and a position
    # the two are linked by the world matrix, i.e.
    #       pos = wm * ijk
    # wm has shape 4x4, last row being (0,0,0,1)
    # https://www.slicer.org/wiki/Coordinate_systems
    # 
    try:
        pos = row['pos'].strip().split(' ')
        wm = row['WorldMatrix'].strip().split(',')
        ijk = row['ijk'].strip().split(' ')
        pos = np.array([float(x) for x in pos] + [1])
        wm = np.reshape(np.array([float(x) for x in wm]), (4,4))
        ijk = np.array([float(x) for x in ijk] + [1])
        ijkp = np.matmul(np.linalg.inv(wm), pos)
        assert np.all(np.abs(ijk - ijkp) < 0.5000001)   # consider 0.5 OK for rounding error
    except:
        logging.exception('coordinates in consistant [pos, ijk, inv(wm)xijk]')
        logging.error(pos)
        logging.error(ijk)
        logging.error(ijkp)
    pass

def sanity_check_coord_dicom (row, dcm):
    # each lesion has an ijk index and a position

    # ftp://dicom.nema.org/MEDICAL/dicom/2015b/output/chtml/part03/sect_C.7.6.2.html

    # X -> right
    # Y -> back
    # Z -> head

    # i/column
    # j/row

    # dcm
    origin = [float(v) for v in dcm.ImagePositionPatient]
    rx, ry, rz, cx, cy, cz = [float(v) for v in dcm.ImageOrientationPatient]
    dir_i = np.array([rx, ry, rz])    # row direction
    dir_j = np.array([cx, cy, cz])    # column direction
    dir_i /= np.linalg.norm(dir_i)   # norm should already be 1
    dir_j /= np.linalg.norm(dir_j)   # norm should already be 1
    dir_k = np.cross(dir_i, dir_j)    # ixj -> k

    pos = np.array([float(x) for x in row['pos'].strip().split(' ')])
    ijk = np.array([float(x) for x in row['ijk'].strip().split(' ')])

    pos -= origin

    spa_j, spa_i = [float(v) for v in dcm.PixelSpacing]
    assert spa_j == spa_i

    i = np.dot(pos, dir_i) / spa_i
    j = np.dot(pos, dir_j) / spa_j
    k = np.dot(pos, dir_k)
    #print("========")
    #print(ijk)
    #print(i, j, k)
    assert max(abs(ijk[0] - i), abs(ijk[1] - j)) < 1.00001
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
        sanity_check_coord(row)
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


def merge_csv (images, ktrans, findings):
    # returns [[Findings]], array (by proxId) of array (by fid)
    lookup = {}
    for _, row in findings.iterrows():
        lookup.setdefault(row['ProxID'], {})[row['fid']] = Finding(row)
        pass
    for _, row in images.iterrows():
        lookup[row['ProxID']][row['fid']].add_image(row)
        pass

    findings = []
    proxIDs = list(lookup.keys())
    proxIDs.sort()
    for k in proxIDs:
        v = list(lookup[k].values())
        v.sort(key=lambda x: x.fid)
        findings.append(v)
    return findings

def load_train_csv ():
    return merge_csv(load_images_csv('raw/ProstateX-TrainingLesionInformationv2/ProstateX-Images-Train.csv'), \
           load_ktrans_csv('raw/ProstateX-TrainingLesionInformationv2/ProstateX-Images-KTrans-Train.csv'), \
           load_findings_csv('raw/ProstateX-TrainingLesionInformationv2/ProstateX-Findings-Train.csv'))

def load_test_csv ():
    return merge_csv(load_images_csv('raw/ProstateX-TestLesionInformation/ProstateX-Images-Test.csv'), \
           load_ktrans_csv('raw/ProstateX-TestLesionInformation/ProstateX-Images-KTrans-Test.csv'), \
           load_findings_csv('raw/ProstateX-TestLesionInformation/ProstateX-Findings-Test.csv'))


if __name__ == '__main__':
    load_train_csv()
    load_test_csv()

