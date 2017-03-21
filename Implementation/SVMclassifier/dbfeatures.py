from __future__ import print_function

import os
import cv2


fileDir = os.path.dirname(os.path.realpath(__file__))
dbsDir = os.path.join(fileDir, '..','databases')

def is_casia_real_face(path):
    name = path.split('/')[-1]

    return name == '1.avi' or name == '2.avi' or name == 'HR_1.avi':

def get_frames_features(video_path, feature_computer):
    video_feed = cv2.VideoCapture(video_path)

    while True:
        ret, frame = video_feed.read()
        
        if ret == False:
            break

        # compute features here
        


def compute_realface_features_casia(feature_computer):
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
                    continue

                video_features = get_frames_features(full_file_path, feature_computer)
                features.extend(video_features)

    return features


def compute_spoofface_features_casia():
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
                    continue

                video_features = get_frames_features(full_file_path)
                features.extend(video_features)

    return features

if __name__ == '__main__':
    compute_realface_features_casia()
