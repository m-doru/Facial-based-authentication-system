from __future__ import print_function

import os
import cv2
from faceSpoofDetection import face_detector

fileDir = os.path.dirname(os.path.realpath(__file__))
dbsDir = os.path.join(fileDir, '..', '..', 'databases')

face_det = face_detector.FaceDetector()


def get_frames_features(video_path, feature_computer):
    video_feed = cv2.VideoCapture(video_path)

    features = []

    while True:
        ret, frame = video_feed.read()

        if ret == False:
            break

        # compute features vectors here
        # should I compute the feature vector for faces or the entire frame?
        # I will go with faces
        faces = face_det.get_aligned_faces_in_frame(frame)
        for face in faces:
            features.append(feature_computer.compute_features(face))

        # skip some frames
        i = 0
        while i < 10 and ret:
            ret = video_feed.grab()
            i += 1

    return features

def compute_face_features_idiap(feature_computer, stage='train',real=True, verbose = False):
    if stage not in ['train', 'devel']:
        raise Exception('Stage not a valid option. Use train or devel')

    if real:
        face_type = 'real'
    else:
        face_type = 'attack'
    if verbose:
        print('Started processing idiap {} faces database for {}'.format(face_type, stage))

    dbpath = os.path.join(dbsDir, 'idiap', stage, face_type)

    features = []
    # when processing the attack files, I forgot that there are 2 aditional directories: fixed and hand
    for _, dirs, _ in os.walk(dbpath):
        if len(dirs) == 0:
            dirs.append("")
        for dir in dirs:
            path = os.path.join(dbpath, dir)
            for _, _, files in os.walk(path):
                for file in files:
                    filepath = os.path.join(dbpath, dir, file)
                    if verbose:
                        print('Processing file {}'.format(filepath))

                    full_file_path = os.path.join(dbpath, filepath)

                    video_features = get_frames_features(full_file_path, feature_computer)

                    features.extend(video_features)

        break

    return features


def compute_realface_features_casia(feature_computer, train=True):
    print('Started processing casia real faces database')
    if train:
        dbpath = os.path.join(dbsDir, 'cbsr_antispoofing', 'train_release')
    else:
        dbpath = os.path.join(dbsDir, 'cbsr_antispoofing', 'test_release')

    features = []

    dirs = []
    for _, ds, _ in os.walk(dbpath):
        dirs.extend(ds)
        break

    for dir in dirs:
        print('Processing subject {}'.format(dir))
        dirpath = os.path.join(dbpath, dir)
        for _, _, files in os.walk(os.path.join(dbpath, dir)):
            for file in files:
                full_file_path = os.path.join(dirpath, file)

                if is_casia_real_face(full_file_path):
                    print('Processing file {}'.format(file))

                    video_features = get_frames_features(full_file_path, feature_computer)
                    features.extend(video_features)
            break

    return features


def compute_spoofface_features_casia(feature_computer, train=True):
    print('Started processing casia spoof faces database')
    if train:
        dbpath = os.path.join(dbsDir, 'cbsr_antispoofing', 'train_release')
    else:
        dbpath = os.path.join(dbsDir, 'cbsr_antispoofing', 'test_release')

    features = []

    dirs = []
    for _, ds, _ in os.walk(dbpath):
        dirs.extend(ds)
        break

    for dir in dirs:
        print('Processing subject {}'.format(dir))
        dirpath = os.path.join(dbpath, dir)
        for _, _, files in os.walk(os.path.join(dbpath, dir)):
            for file in files:
                full_file_path = os.path.join(dirpath, file)

                if not is_casia_real_face(full_file_path):
                    print('Processing file {}'.format(file))

                    video_features = get_frames_features(full_file_path, feature_computer)
                    features.extend(video_features)
            break

    return features


def is_casia_real_face(path):
    name = path.split('/')[-1]

    return name == '1.avi' or name == '2.avi' or name == 'HR_1.avi'


def compute_face_features_msu_mfsd(feature_computer, real=True, train=True):
    print('Started processing msu mfsd spoof faces database')
    if real:
        dbpath = os.path.join(dbsDir, 'MSU_MFSD', 'MSU-MFSD', 'scene01', 'real')
    else:
        dbpath = os.path.join(dbsDir, 'MSU_MFSD', 'MSU-MFSD', 'scene01', 'attack')

    subjects = get_msu_mfsd_stage_subjects(train=train)

    features = []

    for _, _, files in os.walk(dbpath):
        for file in files:
            full_file_path = os.path.join(dbpath, file)

            if is_msu_mfsd_stage_subject(file, subjects) and not file.endswith('face'):
                print('Processing file {}'.format(file))

                video_features = get_frames_features(full_file_path, feature_computer)
                features.extend(video_features)
        break

    return features


def is_msu_mfsd_stage_subject(filename, train_subjects):
    subject_id = filename.split('_')[1][-2:]

    if subject_id in train_subjects:
        return True

    return False


def get_msu_mfsd_stage_subjects(train=True):
    if train:
        sub_list_filename = os.path.join(dbsDir, 'MSU_MFSD', 'MSU-MFSD', 'train_sub_list.txt')
    else:
        sub_list_filename = os.path.join(dbsDir, 'MSU_MFSD', 'MSU-MFSD', 'test_sub_list.txt')

    train_videos = []

    with open(sub_list_filename, 'r') as f:
        for line in f:
            train_videos.append(line.strip())

    return train_videos


def compute_realface_features_msu_ussa(feature_computer, five_fold_train):
    five_fold_subject_id_path = '/home/doru/Desktop/Licenta/Implementation/databases/MSU_USSA/MSU_USSA_Public/FiveFoldSubjectID'
    subjects_fold_number = compute_msu_ussa_subjects_folds_dict()

    dbpath = os.path.join(dbsDir, 'MSU_USSA', 'MSU_USSA_Public', 'LiveSubjectsImages')

    features = []

    for _, _, files in os.walk(dbpath):
        files.sort(key=lambda item:(len(item), item))
        for file in files:
            full_file_path = os.path.join(dbpath, file)

            crt_subject_id = file.split('.')[0]

            if crt_subject_id not in subjects_fold_number:
                continue

            fold_number = subjects_fold_number[crt_subject_id]

            # check if current subject is part of the choisen five fold subjects division
            if fold_number in five_fold_train:
                print('Processing file {}'.format(file))

                image_features = get_frames_features(full_file_path, feature_computer)
                features.extend(image_features)
        break

    return features


def compute_spoofface_features_msu_ussa(feature_computer, five_fold_train,
                                        dirs=('MacBook_FrontCamera', 'MacBook_RearCamera', 'Nexus_FrontCamera',
                                              'Nexus_RearCamera', 'PrintedPhoto_FrontCamera', 'PrintedPhoto_RearCamera',
                                              'Tablet_FrontCamera', 'Tablet_RearCamera')):
    subjects_fold_number = compute_msu_ussa_subjects_folds_dict()

    dbpath = os.path.join(dbsDir, 'MSU_USSA', 'MSU_USSA_Public', 'SpoofSubjectImages')

    features_per_dir = []

    for dir in dirs:
        dirpath = os.path.join(dbpath, dir)
        features = []
        for _, _, files in os.walk(dirpath):
            files.sort(key=lambda item:(len(item), item))
            for file in files:
                full_file_path = os.path.join(dirpath, file)

                # check if current subject is part of the choisen five fold subjects division
                crt_subject_id = file.split('.')[0]

                if crt_subject_id not in subjects_fold_number:
                    continue

                fold_number = subjects_fold_number[crt_subject_id]
                if fold_number in five_fold_train:
                    print('Processing file {}'.format(file))

                    image_features = get_frames_features(full_file_path, feature_computer)
                    features.extend(image_features)
            break
        features_per_dir.append(features)

    return features_per_dir


def compute_msu_ussa_subjects_folds_dict():
    # computes a dictionary that maps the subject id to the fold he belongs
    five_fold_subject_id_path = '/home/doru/Desktop/Licenta/Implementation/databases/MSU_USSA/MSU_USSA_Public/FiveFoldSubjectID'
    subjects_id = {}
    with open(five_fold_subject_id_path, 'r') as f:
        for i, line in enumerate(f):
            subjects_id[str(i)] = int(line.strip())

    return subjects_id

def compute_msu_ussa_subjects_folds_arr():
    five_fold_subject_id_path = '/home/doru/Desktop/Licenta/Implementation/databases/MSU_USSA/MSU_USSA_Public/FiveFoldSubjectID'
    subjects_id = []
    with open(five_fold_subject_id_path, 'r') as f:
        for i, line in enumerate(f):
            subjects_id.append(int(line))
            if i >= 980:
                break

    return subjects_id