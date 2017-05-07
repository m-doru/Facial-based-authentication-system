from __future__ import print_function

from facespair import FacesPair
from face import Face

import itertools
import os
import re

import joblib
import matplotlib.pyplot as pyplot
import matplotlib.patches as mpatches

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

def get_face_pairs(faces, examples_per_subject):
    filtered_faces = []
    used_faces = {}
    for face in faces:
        if face.id not in used_faces:
            used_faces[face.id] = 1
        if used_faces[face.id] < examples_per_subject:
            filtered_faces.append(face)
            used_faces[face.id] += 1

    face_pairs = []
    for (face1, face2) in itertools.combinations(filtered_faces, 2):
        fp = FacesPair(face1, face2)
        face_pairs.append(fp)

    face_pairs.sort(key=lambda fp:fp.distance)

    return face_pairs


def main(load=False, examples_per_subject=None):
    saved_faces_filename = "sorted_face_pairs.pkl"
    if not load:
        path_to_db = '../databases/MsCelebsV1-Faces-Cropper-07'
        faces = get_faces_with_ids(path_to_db, True)
        joblib.dump(faces, saved_faces_filename)
    else:
        faces = joblib.load(saved_faces_filename)

    face_pairs = get_face_pairs(faces, examples_per_subject)
    same_id_distances = []
    diff_id_distances = []
    for fp in face_pairs:
        if fp.same_id:
            same_id_distances.append(fp.distance)
        else:
            diff_id_distances.append(fp.distance)

    pyplot.figure(1)
    pyplot.hist(same_id_distances, 40, normed=1, facecolor='green')
    pyplot.title('Distribution of face distances')
    pyplot.xlabel('Faces distance')
    pyplot.ylabel('# of face pairs')
    pyplot.axis([0, 4, 0, 1])
    pyplot.grid(True)
    pyplot.hist(diff_id_distances, 40, normed=1, facecolor='red', alpha=0.75)

    diff_subj_patch = mpatches.Patch(color='red', label='Different subjects')
    same_subj_patch = mpatches.Patch(color='green', label='Same subjects')
    pyplot.legend(handles=[same_subj_patch, diff_subj_patch])

    pyplot.show()

if __name__ == "__main__":
    main(False, 10)