"""
WARNING:
This script was created in October 2018 when the specification
for MP2RAGE files was not fully finalized. Please double check with
latest version of the specs to make sure this is accurate.

This script will create the JSON files required for an MP2RAGE file.
To function it requires a BIDS data set with properly named image files:
The script will go through all the folders of a BIDS data set and will create
the JSON files in every folder where it finds a file ending
with '_inv-1_part-mag_MPRAGE.nii.gz'.

Created by RG 2018-10-03
"""

import os
import json
import glob
from collections import OrderedDict

# DEFINE CONTENT OF JSON FILES

# defining the content of the JSON file for the
# first inversion image (sub-*_inv-1_MPRAGE.json)
data_inv_1 = OrderedDict([
    ('InversionTime', '900'),
    ('FlipAngle', '5')  # ms
])

# defining the content of the JSON file for the
# second inversion image (sub-*_inv-2_MPRAGE.json)
data_inv_2 = OrderedDict([
    ('InversionTime', '2750'),
    ('FlipAngle', '3')  # ms
])

# defining the content of the JSON files for the
# T1w (sub-*_T1w.json) and the T1map (sub-*_T1map.json)
data_T1 = OrderedDict([
    ('EstimationMethod', 'Marques et al., 2013'),
])

# defining the content of the main JSON file (sub-*_MPRAGE.json)
data_MP2RAGE = OrderedDict([
    ('MagneticFieldStrength',  ''),
    ('ExcitationRepetitionTime',  ''),
    ('InversionRepetitionTime',  ''),
    ('NumberShots',  ''),
    ('Manufacturer',  ''),
    ('ManufacturersModelName',  ''),
    ('DeviceSerialNumber',  ''),
    ('SoftwareVersions',  ''),
    ('StationName',  ''),
    ('InstitutionName',  ''),
    ('InstitutionAddress',  ''),
    ('InstitutionalDepartmentName',  ''),
    ('ReceiveCoilName',  ''),
    ('ReceiveCoilActiveElements',  ''),
    ('GradientSetType',  ''),
    ('MRTransmitCoilSequence',  ''),
    ('MatrixCoilMode',  ''),
    ('CoilCombinationMethod',  ''),
    ('NonlinearGradientCorrection',  ''),
    ('WaterFatShift',  ''),
    ('EchoTrainLength',  ''),
    ('DwellTime',  ''),
    ('MultibandAccelerationFactor',  ''),
    ('AnatomicalLandmarkCoordinates',  ''),
    ('MRAcquisitionType',  ''),
    ('ScanningSequence',  ''),
    ('SequenceVariant',  ''),
    ('ScanOptions',  ''),
    ('SequenceName',  ''),
    ('PulseSequenceType',  'MP2RAGE'),
    ('PulseSequenceDetails',  ''),
    ('ParallelReductionFactorInPlane',  ''),
    ('ParallelAcquisitionTechnique',  ''),
    ('PartialFourier',  ''),
    ('PartialFourierDirection',  ''),
    ('EffectiveEchoSpacing',  ''),
    ('TotalReadoutTime',  ''),
    ('PhaseEncodingDirection',  ''),
    ('EchoTime1',  ''),  # sec
    ('EchoTime2',  ''),  # sec
    ('SliceThickness',  '')  # mm
])

# WRITE THEM

indent = 4

start_dir = ''  # insert here path to your BIDS data set

# list all subjects and  create iterator with full path for subjects folder
subj_ls = glob.iglob(os.path.join(start_dir, 'sub*'))

for iSubj in subj_ls:

    # list all subfolders and files for that subject
    subj_dir = os.walk(iSubj)

    # go through all the files for that subject
    for path, subdirs, files in subj_dir:
        for f in files:
            # creates the json files in the folder where the magnitude image
            # of the first inversion is found
            if '_inv-1_part-mag_MPRAGE.nii.gz' in f:

                #  define filename, excluding last three key-value pairs
                fname = '_'.join(f.split('_')[:-3])

                json_folder = path

                # creating JSON file for the first inversion image
                json_name = '{}_inv-1_MPRAGE.json'.format(fname)
                # create the file
                with open(os.path.join(json_folder, json_name), 'w') as ff:
                    json.dump(data_inv_1, ff, sort_keys=False, indent=indent)

                # creating JSON file for the second inversion image
                json_name = '{}_inv-2_MPRAGE.json'.format(fname)
                with open(os.path.join(json_folder, json_name), 'w') as ff:
                    json.dump(data_inv_2, ff, sort_keys=False, indent=indent)

                # creating main JSON file for the MP2RAGE
                json_name = '{}_MPRAGE.json'.format(fname)
                with open(os.path.join(json_folder, json_name), 'w') as ff:
                    json.dump(data_MP2RAGE, ff, sort_keys=False, indent=indent)

                # adding content to JSON files for the T1w and T1map
                # as its content is subject dependent
                inv1_mag = os.path.join('anat', '{}_inv1_part-mag_MPRAGE.nii.gz'.format(fname))
                inv1_phs = os.path.join('anat', '{}_inv1_part-phase_MPRAGE.nii.gz'.format(fname))
                inv2_mag = os.path.join('anat', '{}_inv1_part-mag_MPRAGE.nii.gz'.format(fname))
                inv2_phs = os.path.join('anat', '{}_inv1_part-phase_MPRAGE.nii.gz'.format(fname))

                data_T1['BasedOn'] = '{0}, {1}, {2}, {3}, '.format(inv1_mag, inv1_phs,
                                                                   inv2_mag, inv2_phs)

                # creating JSON files for the T1w and T1map
                json_name = fname + '_T1map.json'
                with open(os.path.join(json_folder, json_name), 'w') as ff:
                    json.dump(data_T1, ff, sort_keys=False, indent=indent)

                json_name = fname + '_T1w.json'
                with open(os.path.join(json_folder, json_name), 'w') as ff:
                    json.dump(data_T1, ff, sort_keys=False, indent=indent)
