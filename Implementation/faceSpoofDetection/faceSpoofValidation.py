from __future__ import print_function
import cv2
import features
import pickle


class FaceSpoofValidator:
    def __init__(self, lbp, path_to_classifier):
        self._lbp = lbp
        self._sift = features.DSIFT()
        #self.clf = joblib.load(path_to_classifier)
        with open(path_to_classifier, 'r') as f:
            self.clf = pickle.load(f)

    def validate_face(self, face):
        print(face.shape)

        face = cv2.resize(face, features.FRAME_SIZE)
        grey_aligned_face = cv2.cvtColor(face, cv2.COLOR_BGR2GRAY)

        lbp_feature = self._lbp.compute(grey_aligned_face)
        #dsift_feature = self._sift.compute(grey_aligned_face, 8, 16)

        feature_vector = lbp_feature

        print(self.clf.predict([feature_vector]))

        if self.clf.predict([feature_vector]) == 1:
            return True
        else:
            return False

    def validate_frame(self, frame):
        cv2.imshow('validating frame', frame)

        grey_small_frame = cv2.cvtColor(cv2.resize(frame, features.FRAME_SIZE), cv2.COLOR_BGR2GRAY)
        if self.clf.fit(self._lbp.compute(grey_small_frame)) == 1:
            return True

        return False