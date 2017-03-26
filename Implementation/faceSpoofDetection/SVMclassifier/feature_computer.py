import cv2
from faceSpoofDetection import features

class FrameFeatureComputer:
    def __init__(self, feature_computer):
        self.feature_computer = feature_computer

    def compute_features(self, frame):
        small_frame = cv2.resize(frame, features.FRAME_SIZE)

        grey_small_frame = cv2.cvtColor(small_frame, cv2.COLOR_BGR2GRAY)

        return self.feature_computer.compute(grey_small_frame)
