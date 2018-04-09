#!/usr/bin/env python3
import sys
import logging
from glob import glob
import dicom

class PatientInfo:
    # information that should be same for all images of the patient
    def __init__ (self, path):
        # path e.g. raw/PROSTATEx/ProstateX-0148/1.3.6.1.4.1.....
        self.PatientName = path.split('/')[2]
        print(self.PatientName)
        pass
    pass

class SeriesInfo:
    # information that applies to all DICOMS under the same directory
    def __init__ (self, dcm, patient):
        try:
            # extract series info and sanity check patient info
            assert dcm.PatientName == patient.PatientName
            assert dcm.PatientID == patient.PatientName
            # StudyDescription
            self.SeriesDescription = dcm.SeriesDescription
            self.PatientSex = dcm.PatientSex
            self.PatientAge = dcm.PatientAge

            self.ManufacturerModelName = dcm.ManufacturerModelName
            assert dcm.ManufacturerModelName == 'TrioTim' or dcm.ManufacturerModelName == 'Skyra'
            # PatientSize is not always available
            # self.PatientSize = dcm.PatientSize  # height??
            self.PatientWeight = dcm.PatientWeight  # KG??
            self.SliceThickness = dcm.SliceThickness
            self.Rows = dcm.Rows
            self.Columns = dcm.Columns
            self.PixelSpacing = dcm.PixelSpacing
            self.ImageOrientationPatient = dcm.ImageOrientationPatient
        except:
            logging.exception(dcm.path)
        pass
    pass

class ImageInfo:
    def __init__ (self, dcm, series):
        # extract image info and sanity check series info
        try:
            assert dcm.Modality == 'MR'
            assert dcm.Manufacturer == 'SIEMENS'
            assert dcm.BodyPartExamined == 'PROSTATE'
            assert dcm.PatientPosition == 'FFS'
            assert dcm.SamplesPerPixel == 1
            assert dcm.PhotometricInterpretation == 'MONOCHROME2'
            assert dcm.BitsAllocated == 16
            assert dcm.BitsStored == 12
            assert dcm.HighBit == 11
            assert dcm.PixelRepresentation == 0
            assert dcm.SmallestImagePixelValue < 100

            assert series.ManufacturerModelName == dcm.ManufacturerModelName
            assert series.SeriesDescription == dcm.SeriesDescription
            assert series.PatientSex == dcm.PatientSex
            assert series.PatientAge == dcm.PatientAge
            #assert series.PatientSize == dcm.PatientSize  # height??
            assert series.PatientWeight == dcm.PatientWeight  # KG??
            assert series.SliceThickness == dcm.SliceThickness
            assert series.Rows == dcm.Rows
            assert series.Columns == dcm.Columns
            assert series.PixelSpacing == dcm.PixelSpacing
            assert series.ImageOrientationPatient == dcm.ImageOrientationPatient

            self.ImagePositionPatient = dcm.ImagePositionPatient
            #self.ImageOrientationPatient = dcm.ImageOrientationPatient
            self.SliceLocation = dcm.SliceLocation
        except:
            logging.exception(dcm.path)
        pass
        # not using DCM fields
        # InstanceCreationDate
        # InstanceCreationTime
        # StudyDate/Time
        # SeriesDate/Time
        # AcquisitionDate/Time
        # ContentDate/Time

        # RepetitionTime
        # EchoTime
        # ImagingFrequency
        # ImageNucleus 
        # EchoNumbers
        # MagneticFieldStrenght
        # NumberOfPhaseEncodingSteps
        # EchoTrainLength
        # PercentSampling
        # PercentPhaseFieldOfView
        # PixelBandwidth
        # ContrastXXX
        # AcquisitionMatrix
        # InPlanePhaseEncodingDirection
        # FlipAngle
        # VariableFlipAngleFlag
        # SAR
        # dBdt
        # PatientPosition

        # SeriesNumber
        # AcquisitioniNumber
        # InstanceNumber

        # WindowCenter
        # WindowWidth
        # WindowCenterWidthExplanation
    pass

def scan_series (root, patient):
    series = None
    for dcm_path in glob(root + '/*'):
        dcm = dicom.read_file(dcm_path)
        dcm.path = dcm_path
        if series is None:
            series = SeriesInfo(dcm, patient)
        # sanity check each image
        image = ImageInfo(dcm, series)
        break
    pass

def scan_patient (root):
    patient = None
    # scan directory of a patient
    # root e.g. raw/PROSTATEx/ProstateX-0113
    for sub in glob(root + '/*'):
        for series in glob(sub + '/*'):
            if patient is None:
                patient = PatientInfo(series)
            scan_series(series, patient)
    pass

def scan_all ():
    for d in glob('raw/PROSTATEx/*'):
        scan_patient(d)
        pass
    pass


scan_all()
