# -*- coding: utf-8 -*-
"""
Created on Sun Mar 27 18:51:35 2022

@author: johbla@ous-hf.no

Python Enviroment: Conda-installed env. called "Radiomics", version 3.7.10

Stolen from the tutorial, trying to adjust to run on non-negative PET-images

"""

from __future__ import print_function

import nrrd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

from radiomics import featureextractor, getFeatureClasses
import radiomics

import scipy.stats

import sys
import os
import logging
import six

#%% Load and run some sanity check on the images

imageName, maskName = ("SlicerScenes/21 PET Lever Q.Clear 4.nrrd", 
                       "SlicerScenes/PhantomDefinition.seg.nrrd")

image_array, image_header = nrrd.read(imageName, index_order='C') # 10 hrs
mask_array, mask_header = nrrd.read(maskName, index_order='C') # 10 hrs

for label in range(1, np.max(mask_array)+1):
    print(label)
    print("Mean" + str(label) + ": " + str(np.mean(image_array[mask_array == label])))
    print("Voxel nums in label: " + str(np.sum(mask_array == label)))

#%%

# Get the PyRadiomics logger (default log-level = INFO)
logger = radiomics.logger
logger.setLevel(logging.DEBUG)  # set level to DEBUG to include debug log messages in log file

# Write out all log entries to a file
handler = logging.FileHandler(filename='testLog.txt', mode='w')
formatter = logging.Formatter('%(levelname)s:%(name)s: %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)

#%%

#featureClasses = getFeatureClasses()
#imageName, maskName = radiomics.getTestCase('brain1')

imageName, maskName = ("SlicerScenes/21 PET Lever Q.Clear 4.nrrd", 
                       "SlicerScenes/PhantomDefinition.seg.nrrd")

if imageName is None or maskName is None:  # Something went wrong, in this case PyRadiomics will also log an error
    raise Exception('Error getting testcase!')  # Raise exception to prevent cells below from running in case of "run all"

#%%

# Alternative: use hardcoded settings (separate for settings, input image types and enabled features)
settings = {}
settings['binWidth'] = 25
settings['resampledPixelSpacing'] = None
# settings['resampledPixelSpacing'] = [3, 3, 3]  # This is an example for defining resampling (voxels with size 3x3x3mm)
settings['interpolator'] = 'sitkBSpline'
settings['verbose'] = True

extractor = featureextractor.RadiomicsFeatureExtractor(**settings)

print('Enabled input images:')
for imageType in extractor.enabledImagetypes.keys():
    print('\t' + imageType)
    
#%%

# Disable all classes
extractor.disableAllFeatures()

# Enable all features in firstorder
extractor.enableFeatureClassByName('firstorder')

# Alternative; only enable 'Mean' and 'Skewness' features in firstorder
extractor.enableFeaturesByName(firstorder=['Mean', 'Skewness'])

for label in range(1,np.max(mask_array)):

    print('Calculating features for label ' + str(label) + "\n")
    featureVector = extractor.execute(imageName, maskName, label = label)
    
    for featureName in featureVector.keys():
        print('Computed %s: %s' % (featureName, featureVector[featureName]))

#%%

# Show output
for featureName in featureVector.keys():
    print('Computed %s: %s' % (featureName, featureVector[featureName]))
