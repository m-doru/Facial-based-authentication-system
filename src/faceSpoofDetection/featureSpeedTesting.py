from __future__ import print_function

import sys
import os

fileDir = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.join(fileDir, ".."))


import time

import cv2
import numpy as np

import features
import openface

import os

mlbp = features.MultiScaleLocalBinaryPatterns((8, 1), (24, 3), (40, 5))

filePath = os.path.dirname(os.path.realpath(__file__))
imagePath = os.path.join(filePath, "..", "data", "face2.jpg")
faceImg = cv2.imread(imagePath, cv2.IMREAD_COLOR)
# spoofFaceImg = cv2.imread('../data/spoofFace2.jpg', cv2.IMREAD_COLOR)

print(faceImg.shape)
faceImg = cv2.resize(faceImg, (640, 480))
print(faceImg.shape)

# faceImg = cv2.cvtColor(faceImg, cv2.COLOR_BGR2RGB)
# spoofFaceImg = cv2.cvtColor(spoofFaceImg, cv2.COLOR_BGR2RGB)

"""
cv2.imshow('img', faceImg)
if cv2.waitKey(0) & 0xFF == ord('q'):
    pass
"""

align = openface.AlignDlib(
    "/home/doru/Desktop/Licenta/Implementation/models/dlib/shape_predictor_68_face_landmarks.dat"
)
start = time.time()
# Get all bounding boxes
bb = align.getAllFaceBoundingBoxes(faceImg)

if bb is None:
    raise Exception("No faces detected")


alignedFaces = []

for box in bb:
    alignedFaces.append(
        align.align(
            144, faceImg, box, landmarkIndices=openface.AlignDlib.OUTER_EYES_AND_NOSE
        )
    )

if alignedFaces is None:
    raise Exception("Unable to align the frame")

print("Detection of the face took {}".format(time.time() - start))

start = time.time()
lbpFaceFeature = mlbp.computeFeaturePatchWise(
    cv2.cvtColor(alignedFaces[0], cv2.COLOR_RGB2GRAY)
)
print("Computing the mlbp feature of a face took {}".format(time.time() - start))

start = time.time()
lbpFeature = mlbp.computeFeaturePatchWise(cv2.cvtColor(faceImg, cv2.COLOR_RGB2GRAY))
print(
    "Computing the mlbp feature of the entire frame took {}".format(time.time() - start)
)

dsift = features.DSIFT()

start = time.time()

gray = cv2.cvtColor(alignedFaces[0], cv2.COLOR_RGB2GRAY)
gray = gray.astype("float32")

kp, dsiftFaceFeature = dsift.compute(gray, 8, 16)
dsiftFaceFeature = np.transpose(dsiftFaceFeature)
print("Computing the dsift feature of the face took {}".format(time.time() - start))

start = time.time()
kpFull, dsiftFeature = dsift.compute(faceImg, 8, 8)
print(
    "Computing the dsift feature of the full image took {}".format(time.time() - start)
)

print("Length of the face mlbp feature: ", len(lbpFaceFeature))
print("Length of the full mlbp feature: ", len(lbpFeature))

print("Length of the face dsift feature: ", len(dsiftFaceFeature[0]) * 128)
print("Length of the full dsift feature: ", len(dsiftFeature[0]) * 128)
