import random
import cv2
import features
from sklearn.externals import joblib


class FaceSpoofValidator:
    def __init__(self, lbp):
        self._lbp = lbp
        self._sift = features.DSIFT()
        self.clf = joblib.load('../classifiers/casia.pkl')

    def validateFace(self, face):
        cv2.imshow('face', face)

        grey_aligned_face = cv2.cvtColor(face, cv2.COLOR_BGR2GRAY)

        lbp_feature = self._lbp.computeFeaturePatchWise(grey_aligned_face)
        #dsift_feature = self._sift.compute(grey_aligned_face, 8, 16)

        feature_vector = lbp_feature

        if self.clf.predict(feature_vector) == 1:
            return True
        else:
            return False