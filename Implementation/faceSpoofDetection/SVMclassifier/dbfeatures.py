from __future__ import print_function

import os
import cv2
from faceSpoofDetection import face_detector

fileDir = os.path.dirname(os.path.realpath(__file__))
dbsDir = os.path.join(fileDir, '..','..','databases')

face_det = face_detector.FaceDetector()

def get_frames_features(video_path, feature_computer):
    video_feed = cv2.VideoCapture(video_path)

    features = []

    while True:
        ret, frame = video_feed.read()

        if ret == False:
            break

        # compute features vectors here
        # should I compute the feature fector for faces or the entire frame?
        # I will go with faces
        faces = face_det.get_faces_in_frame(frame)
        for face in faces:
            features.append(feature_computer.compute_features(face))

        # skip next 30 frames
        i = 0
        while i < 0 and ret:
            ret = video_feed.grab()
            i += 1

    return features


def compute_realface_features_casia(feature_computer):
    print('Started processing casia real faces database')
    dbpath = os.path.join(dbsDir, 'cbsr_antispoofing', 'train_release')

    features = []

    dirs = []
    for _, ds, _ in os.walk(dbpath):
        dirs.extend(ds)
        break

    for dir in dirs:
        dirpath = os.path.join(dbpath, dir)
        for _, _, files in os.walk(os.path.join(dbpath, dir)):
            for file in files:
                full_file_path = os.path.join(dirpath, file)

                if is_casia_real_face(full_file_path):
                    print('Processing file {}'.format(file))

                    video_features = get_frames_features(full_file_path, feature_computer)
                    features.extend(video_features)
            break
        break


    return features

def compute_spoofface_features_casia(feature_computer):
    print('Started processing casia spoof faces database')
    dbpath = os.path.join(dbsDir, 'cbsr_antispoofing', 'train_release')

    features = []

    dirs = []
    for _, ds, _ in os.walk(dbpath):
        dirs.extend(ds)
        break

    for dir in dirs:
        dirpath = os.path.join(dbpath, dir)
        for _, _, files in os.walk(os.path.join(dbpath, dir)):
            for file in files:
                full_file_path = os.path.join(dirpath, file)

                if not is_casia_real_face(full_file_path):
                    print('Processing file {}'.format(file))

                    video_features = get_frames_features(full_file_path, feature_computer)
                    features.extend(video_features)
            break
        break

    return features

def is_casia_real_face(path):
    name = path.split('/')[-1]

    return name == '1.avi' or name == '2.avi' or name == 'HR_1.avi'

def compute_face_features_msu_mfsd(feature_computer, real = True):
    print('Started processing msu mfsd spoof faces database')
    if real:
        dbpath = os.path.join(dbsDir, 'MSU_MFSD', 'MSU-MFSD', 'scene01', 'real')
    else:
        dbpath = os.path.join(dbsDir, 'MSU_MFSD', 'MSU-MFSD', 'scene01', 'attack')
    train_subjects = get_msu_mfsd_train_subjects()

    features = []

    for _, _, files in os.walk(dbpath):
        for file in files:
            full_file_path = os.path.join(dbpath, file)

            if is_msu_mfsd_train_subject(file, train_subjects) and not file.endswith('face'):
                print('Processing file {}'.format(file))

                video_features = get_frames_features(full_file_path, feature_computer)
                features.extend(video_features)
        break

    return features

def is_msu_mfsd_train_subject(filename, train_subjects):
    subject_id = filename.split('_')[1][-2:]

    if subject_id in train_subjects:
        return True

    return False

def get_msu_mfsd_train_subjects():
    train_sub_list_filename = os.path.join(dbsDir, 'MSU_MFSD', 'MSU-MFSD', 'train_sub_list.txt')

    train_videos = []

    with open(train_sub_list_filename, 'r') as f:
        for line in f:
            train_videos.append(line.strip())

    return train_videos


def compute_realface_features_msu_ussa(feature_computer, five_fold_train):
    five_fold_subject_id_path = '/home/doru/Desktop/Licenta/Implementation/databases/MSU_USSA/MSU_USSA_Public/FiveFoldSubjectID'
    subjects_id = compute_subjects_id(five_fold_subject_id_path)

    dbpath = os.path.join(dbsDir, 'MSU_USSA', 'MSU_USSA_Public', 'LiveSubjectsImages')

    features = []

    for _, _, files in os.walk(dbpath):
        for file in files:
            full_file_path = os.path.join(dbpath, file)

            #check if current subject is part of the choisen five fold subjects division
            if subjects_id[file.split('.')[0]] in five_fold_train:
                print('Processing file {}'.format(file))

                image_features = get_frames_features(full_file_path, feature_computer)
                features.extend(image_features)
        break

    return features

def compute_spoofface_features_msu_ussa(feature_computer, five_fold_train, dirs=('MacBook_FrontCamera',
                                                                                 'MacBook_RearCamera',
                                                                                 'Nexus_FrontCamera',
                                                                                 'Nexus_RearCamera',
                                                                                 'PrintedPhoto_FrontCamera',
                                                                                 'PrintedPhoto_RearCamera',
                                                                                 'Tablet_FrontCamera',
                                                                                 'Tablet_RearCamera')):
    five_fold_subject_id_path = '/home/doru/Desktop/Licenta/Implementation/databases/MSU_USSA/MSU_USSA_Public/FiveFoldSubjectID'
    subjects_fold_number = compute_subjects_id(five_fold_subject_id_path)

    dbpath = os.path.join(dbsDir, 'MSU_USSA', 'MSU_USSA_Public', 'SpoofSubjectsImages')

    features = []

    for dir in dirs:
        dirpath = os.path.join(dbpath, dir)
        for _, _, files in os.walk(dirpath):
            for file in files:
                full_file_path = os.path.join(dirpath, file)

                #check if current subject is part of the choisen five fold subjects division
                crt_subject_id = file.split('.')[0]
                fold_number = subjects_fold_number[crt_subject_id]
                if fold_number in five_fold_train:
                    print('Processing file {}'.format(file))

                    image_features = get_frames_features(full_file_path, feature_computer)
                    features.extend(image_features)
            break

    return features


def compute_subjects_id(path):
    subjects_id = {}
    with open(path, 'r') as f:
        for i, line in enumerate(f):
            subjects_id[i] = line

    return subjects_id