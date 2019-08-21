import numpy as np

class FacesPair:
    def __init__(self, face1, face2):
        self.face1 = face1
        self.face2 = face2
        self.same_id = self.face1.id == self.face2.id
        self.distance = self.face1.compute_distance(self.face2.representation)