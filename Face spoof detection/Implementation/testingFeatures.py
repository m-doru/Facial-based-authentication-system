from __future__ import print_function
import openface
import features
import cv2
import numpy as np
import matplotlib.pyplot as plt

P = 16
R = 2

lbp = features.LocalBinaryPatterns(P, R)

faceImg = cv2.imread('data/face2.jpg', cv2.IMREAD_COLOR)
spoofFaceImg = cv2.imread('data/spoofFace2.jpg', cv2.IMREAD_COLOR)

faceImg = cv2.cvtColor(faceImg, cv2.COLOR_BGR2RGB)
spoofFaceImg = cv2.cvtColor(spoofFaceImg, cv2.COLOR_BGR2RGB)

align = openface.AlignDlib("/home/doru/Desktop/Licenta/Face spoof detection/Implementation/models/dlib/shape_predictor_68_face_landmarks.dat")

# Get all bounding boxes
bb = align.getAllFaceBoundingBoxes(faceImg)
bbs = align.getAllFaceBoundingBoxes(spoofFaceImg)

if bb is None or bbs is None:
    raise Exception("No faces detected")


alignedFaces = []

for box in bb:
    alignedFaces.append(align.align(
            260,
            faceImg,
            box,
            landmarkIndices=openface.AlignDlib.OUTER_EYES_AND_NOSE))

if alignedFaces is None:
        raise Exception("Unable to align the frame")

alignedSpoofFaces = []
for box in bbs:
    alignedSpoofFaces.append(align.align(
        260,
        spoofFaceImg,
        box,
        landmarkIndices=openface.AlignDlib.OUTER_EYES_AND_NOSE
    ))

if alignedSpoofFaces is None:
        raise Exception("Unable to align the frame")

grayImg = cv2.cvtColor(alignedFaces[0], cv2.COLOR_RGB2GRAY)
#grayImg = cv2.cvtColor(faceImg, cv2.COLOR_RGB2GRAY)
hist, bins, lbpFV = lbp.compute(grayImg)

graySpoofFace = cv2.cvtColor(alignedSpoofFaces[0], cv2.COLOR_RGB2GRAY)
#graySpoofFace = cv2.cvtColor(spoofFaceImg, cv2.COLOR_RGB2GRAY)
histSpoof, binsSpoof, lbpFVSpoof = lbp.compute(graySpoofFace)

f, ((ax1, ax2), (ax3, ax4)) = plt.subplots(nrows=2, ncols=2, figsize=(9,6))

ax1.imshow(alignedFaces[0])
ax3.hist(hist.ravel(), normed=True, bins = P+2, range=(0, P+2))

ax2.imshow(alignedSpoofFaces[0])
ax4.hist(hist.ravel(), normed=True, bins=P+2, range = (0, P+2))

plt.show()

lbpFV = lbpFV.astype('uint8')
cv2.imshow('lbp', lbpFV)

lbpFVSpoof = lbpFVSpoof.astype('uint8')
cv2.imshow('lbpspoof', lbpFVSpoof)
while(1):
    if cv2.waitKey(0) & 0xFF == ord('q'):
        break

cv2.destroyAllWindows()



