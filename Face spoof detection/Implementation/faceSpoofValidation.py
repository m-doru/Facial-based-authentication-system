import cv2
import random

class FaceSpoofValidator:
    def __init__(self, lbp):
        self._lbp = lbp
        # Also load here the classifier

    def validateFace(self, face):
        cv2.imshow('face', face)

        greyAlignedFace = cv2.cvtColor(face, cv2.COLOR_BGR2GRAY)

        mlbpFeature = self._lbp.computeFeaturePatchWise(greyAlignedFace)

        #Get the classification for hist

        #cv2.imshow('LBP', lbpFV)

        print("Aligned face size {}".format(face.shape))

        if random.random() > 0.2:
            return True
        else:
            return False