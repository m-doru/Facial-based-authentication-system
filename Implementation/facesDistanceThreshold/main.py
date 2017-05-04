import itertools
from facespair import FacesPair

def get_faces_with_ids():
    pass

def main():
    faces = get_faces_with_ids()
    face_pairs = []
    for (face1, face2) in itertools.combinations(faces, 2):
        fp = FacesPair(face1, face2)
        face_pairs.append(fp)
    