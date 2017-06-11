from __future__ import print_function
import cv2
import features
import pickle
import joblib


class FaceSpoofValidator:
    def __init__(self, lbp, path_to_classifier):
        self._lbp = lbp
        self._sift = features.DSIFT()
        self.clf = joblib.load(path_to_classifier)

    def validate_face(self, face):
        print(face.shape)

        face = cv2.resize(face, features.FRAME_SIZE)
        #matrix = cv2.cvtColor(face, cv2.COLOR_BGR2GRAY)
        matrix = face[:,:,2]
        

        lbp_feature = self._lbp.compute(matrix)
        #dsift_feature = self._sift.compute(matrix, 8, 16)

        feature_vector = lbp_feature

        print(self.clf.predict_proba([feature_vector]))
        pred_confidence = self.clf.predict_proba([feature_vector])

        if pred_confidence[0][0] < 0.5:
            return True
        else:
            return False

    def validate_frame(self, frame):
        cv2.imshow('validating frame', frame)

        grey_small_frame = cv2.cvtColor(cv2.resize(frame, features.FRAME_SIZE), cv2.COLOR_BGR2GRAY)
        if self.clf.fit(self._lbp.compute(grey_small_frame)) == 1:
            return True

        return False