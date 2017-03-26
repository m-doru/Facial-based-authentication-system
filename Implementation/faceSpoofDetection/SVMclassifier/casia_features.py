import os

from sklearn import svm
from sklearn.externals import joblib
import pickle

from faceSpoofDetection import features

import dbfeatures
import feature_computer

# pickels filenames
saved_classifier_filename = '../classifiers/casia.pkl'
saved_realfaces_features_filename = '../featuresVectors/casia_realfaces_features.pkl'
saved_spooffaces_features_filename = '../featuresVectors/casia_spooffaces_features.pkl'

# descriptor computer
mlbp_feature_computer = feature_computer.FrameFeatureComputer(features.MultiScaleLocalBinaryPatterns((8, 1), (24, 3),
                                                                                                     (40, 5)))
# compute feature vectors for every frame in the videos with real faces
real_features = dbfeatures.compute_realface_features_casia(mlbp_feature_computer)
#joblib.dump(real_features, saved_realfaces_features_filename)
with open(saved_realfaces_features_filename, 'w') as f:
    pickle.dump(real_features, f)


# compute feature vectors for every frame in the videos with spoof faces
spoof_features = dbfeatures.compute_spoofface_features_casia(mlbp_feature_computer)
#joblib.dump(spoof_features, saved_spooffaces_features_filename)
with open(saved_spooffaces_features_filename, 'w') as f:
    pickle.dump(spoof_features, f)

# create the necessary labels
labels_real = [1 for _ in range(len(real_features))]
labels_spoof = [0 for _ in range(len(spoof_features))]

# create the full features and corresponding labels
features = real_features + spoof_features
labels = labels_real + labels_spoof

clf = svm.SVC()
clf.fit(features, labels)

#joblib.dump(clf, saved_classifier_filename)
with open(saved_classifier_filename, 'w') as f:
    pickle.dump(clf, f)