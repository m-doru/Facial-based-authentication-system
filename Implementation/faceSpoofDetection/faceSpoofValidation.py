import random

import cv2

import features


class FaceSpoofValidator:
    def __init__(self, lbp):
        self._lbp = lbp
        self._sift = features.DSIFT()
        # Also load here the classifier

    def validateFace(self, face):
        cv2.imshow('face', face)

        greyAlignedFace = cv2.cvtColor(face, cv2.COLOR_BGR2GRAY)

        mlbpFeature = self._lbp.computeFeaturePatchWise(greyAlignedFace)
        dsiftFeature = self._sift.compute(greyAlignedFace, 8, 16)

        # featureVector = concatenation of mlbpFeature and dsiftFeature

        # Get the classification for featureVector
        # and return it

        #cv2.imshow('LBP', lbpFV)

        print("Aligned face size {}".format(face.shape))

        if random.random() > 0.2:
            return True
        else:
            return False