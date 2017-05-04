from __future__ import print_function
import itertools
import os
import re
import matplotlib.pyplot as pyplot
import joblib
from facespair import FacesPair
from face import Face

def get_faces_with_ids(path_to_db, verbose = False):
    face_id_multiple_pattern = re.compile(".+[1-9]+\.[a-z]{3}")
    faces = []
    for root, dirs, _ in os.walk(path_to_db):
        for dir in dirs:
            path_to_subject = os.path.join(path_to_db, dir)
            for _, _, imgs in os.walk(path_to_subject):
                for img_file in imgs:
                    if verbose:
                        print('Processing subject {} => {}'.format(dir, img_file))
                    if face_id_multiple_pattern.match(img_file) is not None:
                        continue

                    try:
                        face = Face.from_image_path_with_id(os.path.join(path_to_subject, img_file), dir)
                    except Exception as e:
                        face = None
                        if verbose:
                            print(e.message)
                    if face is not None:
                        faces.append(face)

                break

        break

    return faces



def main(load=False):
    saved_face_pairs_filename = "sorted_face_pairs.pkl"
    if not load:
        path_to_db = '/home/doru/Desktop/MsCelebV1-Faces-Aligned.Samples'
        faces = get_faces_with_ids(path_to_db)
        face_pairs = []
        for (face1, face2) in itertools.combinations(faces, 2):
            fp = FacesPair(face1, face2)
            face_pairs.append(fp)

        face_pairs.sort(key=lambda fp:fp.distance)
        joblib.dump(face_pairs, saved_face_pairs_filename)
    else:
        face_pairs = joblib.load(saved_face_pairs_filename)

    distances = []
    same_id = []

    for fp in face_pairs:
        if fp.same_id:
            distances.append(fp.distance)
            same_id.append(0)
        else:
            distances.append(fp.distance)
            same_id.append(1)

    pyplot.plot(distances, same_id, '.b')
    pyplot.show()


if __name__ == "__main__":
    main(True)