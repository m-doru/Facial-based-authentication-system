from __future__ import print_function

from facespair import FacesPair
from face import Face

import itertools
import os
import re
import time
import random

import joblib
import matplotlib.pyplot as pyplot
import matplotlib.patches as mpatches


def get_faces_with_ids(path_to_db, verbose = False):
    face_id_multiple_pattern = re.compile(".+[1-9]+\.[a-z]{3}")
    faces = []
    identities = 0
    faces_per_identity = []
    for root, dirs, _ in os.walk(path_to_db):
        for dir in dirs:
            path_to_subject = os.path.join(path_to_db, dir)
            # we sample the data so that we take 30 photos from 3% of the faces in an random way so that the
            # distribution it is kept
            if random.random() <= 0.96:
                continue

            identities += 1
            faces_taken = 0
            for _, _, imgs in os.walk(path_to_subject):
                for img_file in imgs:
                    if random.random() > 0.3:
                        continue
                    faces_taken += 1
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
            faces_per_identity.append(faces_taken)

        break
    print("We randomly selected " + str(identities))
    print("With an average of faces per identity of: " + str(sum(faces_per_identity)/len(faces_per_identity)))
    print("With same identity faces {}".format(sum(faces_per_identity)))
    perechi_fete_identice = 0
    for i in range(len(faces_per_identity)):
        perechi_fete_identice += faces_per_identity[i]*(faces_per_identity[i]-1)/2
    print("Number of pairs same identity {}".format(perechi_fete_identice))
    print("Number of faces {}".format(len(faces_per_identity)))
    print(faces_per_identity)
    print("Totalling {}".format(len(faces)))
    return faces

def get_face_pairs(faces, examples_per_subject):
    take_all = examples_per_subject <= 0
    filtered_faces = []
    used_faces = {}
    for face in faces:
        if face.id not in used_faces:
            used_faces[face.id] = 1
        if used_faces[face.id] < examples_per_subject or take_all:
            filtered_faces.append(face)
            used_faces[face.id] += 1

    face_pairs = []
    for (face1, face2) in itertools.combinations(filtered_faces, 2):
        fp = FacesPair(face1, face2)
        face_pairs.append(fp)

    face_pairs.sort(key=lambda fp:fp.distance)

    return face_pairs

def get_faces_distances(faces, examples_per_subject):
    take_all = examples_per_subject <= 0
    filtered_faces = []
    used_faces = {}
    if not take_all:
        for face in faces:
            if face.id not in used_faces:
                used_faces[face.id] = 1
            if used_faces[face.id] < examples_per_subject:
                filtered_faces.append(face)
                used_faces[face.id] += 1
    else:
        filtered_faces = faces
    same_id_distances = []
    diff_id_distances = []
    count = 0
    for (face1, face2) in itertools.combinations(filtered_faces, 2):
        if face1.id == face2.id:
            same_id_distances.append(face1.compute_distance(face2.representation))
        else:
            diff_id_distances.append(face1.compute_distance(face2.representation))
        if count%10000 == 0:
            print("We processed {}0.000 distances".format(count/10000))
        count += 1

    return (same_id_distances, diff_id_distances)

def main(load_faces=False, load_distances=False, examples_per_subject=-1):
    saved_faces_filename = "ids_sorted_face_pairs.pkl"
    if load_faces is not None:
        if not load_faces:
            path_to_db = '../databases/MsCelebsV1-Faces-Cropper-07'
            #path_to_db = '/home/doru/Desktop/MsCelebV1-Faces-Aligned.Samples'
            faces = get_faces_with_ids(path_to_db, True)
            print("Faces read")
            joblib.dump(faces, str(len(faces))+saved_faces_filename)
            print("Faces loaded")
        else:
            faces = joblib.load(saved_faces_filename)
            print("Faces loaded")

    print("We have {}".format(len(faces)))

    saved_distances_same_id_filename = "same_id_distances_"+str(examples_per_subject)+".pkl"
    saved_distances_diff_id_filename = "diff_id_distances_"+str(examples_per_subject)+".pkl"

    if not load_distances or not (os.path.exists(saved_distances_same_id_filename)
                                or os.path.exists(saved_distances_diff_id_filename)):
        (same_id_distances, diff_id_distances) = get_faces_distances(faces, examples_per_subject)
        print("Computed distances")
        '''
        joblib.dump(same_id_distances, saved_distances_same_id_filename)
        print("Saved same id distances")
        joblib.dump(diff_id_distances, saved_distances_diff_id_filename)
        print("Saved different id distances")
        '''
    else:
        with open(saved_distances_same_id_filename, 'rb') as f:
            same_id_distances = joblib.load(f)
            print("Loaded same id distances")
        with open(saved_distances_diff_id_filename, 'rb') as f:
            diff_id_distances = joblib.load(f)
            print("Loaded different id distances")

    (n_s, _, _) = pyplot.hist(same_id_distances, 40, normed=True,facecolor='green')
    (n_d, _, _) = pyplot.hist(diff_id_distances,40, normed=True, facecolor='red', alpha=0.75)
    pyplot.title('Distribution of face distances')
    pyplot.xlabel('Faces distance')
    pyplot.ylabel('# of face pairs')
    pyplot.axis([0, 4, 0, max([max(n_s), max(n_d)])])
    pyplot.grid(True)

    diff_subj_patch = mpatches.Patch(color='red', label='Different subjects')
    same_subj_patch = mpatches.Patch(color='green', label='Same subjects')
    pyplot.legend(handles=[same_subj_patch, diff_subj_patch])

    pyplot.show()
    pyplot.savefig('dist_faces_' + str(examples_per_subject) + '.png')

if __name__ == "__main__":
    start = time.time()
    main(False, False)
    print("Processing took {}".format(time.time() - start))
