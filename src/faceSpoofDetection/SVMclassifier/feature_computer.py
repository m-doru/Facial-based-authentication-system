import cv2
from faceSpoofDetection import features

class FrameFeatureComputer:
    def __init__(self, feature_computer):
        self.feature_computer = feature_computer

    def compute_features(self, frame):
        small_frame = cv2.resize(frame, features.FRAME_SIZE)

        #gray image
        #matrix = cv2.cvtColor(small_frame, cv2.COLOR_BGR2GRAY)
        #red channel
        matrix = small_frame[:,:,2]

        return self.feature_computer.compute(matrix)