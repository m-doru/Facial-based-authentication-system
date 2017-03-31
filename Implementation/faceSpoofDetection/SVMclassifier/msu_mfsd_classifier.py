import os

from sklearn import svm
from sklearn.grid_search import GridSearchCV
from sklearn import neural_network
import joblib

from faceSpoofDetection import features

import dbfeatures
import feature_computer

# pickels filenames
saved_classifier_filename = '../classifiers/msu_mfsd.pkl'
saved_realfaces_features_filename = '../featuresVectors/msu_mfsd_realfaces_features_joblib.pkl'
saved_spooffaces_features_filename = '../featuresVectors/msu_mfsd_spooffaces_features_joblib.pkl'

# wheather to compute new features or load the features from saved files
load_features = True
load_classifier = True

# descriptor computer
mlbp_feature_computer = feature_computer.FrameFeatureComputer(features.MultiScaleLocalBinaryPatterns((8, 1), (24, 3),
                                                                                                    (40, 5)))
#mlbp_feature_computer = feature_computer.FrameFeatureComputer(features.LocalBinaryPatterns(8,1))


# compute feature vectors for every frame in the videos with real faces
if not load_features:
    real_features = dbfeatures.compute_face_features_msu_mfsd(mlbp_feature_computer, real=True)
    #with open(saved_realfaces_features_filename, 'w') as f:
        #pickle.dump(real_features, f)
    joblib.dump(real_features, saved_realfaces_features_filename)

    # compute feature vectors for every frame in the videos with spoof faces
    spoof_features = dbfeatures.compute_face_features_msu_mfsd(mlbp_feature_computer, real=False)
    #with open(saved_spooffaces_features_filename, 'w') as f:
    #    pickle.dump(spoof_features, f)
    joblib.dump(spoof_features, saved_spooffaces_features_filename)
else:
    #with open(saved_realfaces_features_filename, 'r') as f:
    #    real_features = pickle.load(f)
    real_features = joblib.load(saved_realfaces_features_filename)

    #with open(saved_spooffaces_features_filename, 'r') as f:
    #    spoof_features = pickle.load(f)
    spoof_features = joblib.load(saved_spooffaces_features_filename)



# create the necessary labels
labels_real = [1 for _ in range(len(real_features))]
labels_spoof = [-1 for _ in range(len(spoof_features))]

# create the full features and corresponding labels
features = real_features + spoof_features
labels = labels_real + labels_spoof

if not load_classifier:
    '''print("Fitting the classifier to the training set")
    param_grid = [
        {'C': [0.01, 0.1, 1, 10, 100], 'kernel': ['linear']},
        {'C': [0.01, 0.1, 1, 10, 100], 'gamma':[0.001,0.0001], 'kernel': ['rbf'], 'class_weight':['balanced', None]},
    ]
    clf = GridSearchCV(svm.SVC(class_weight='balanced', verbose=True, probability=True), param_grid,
                       verbose=True)
    print("Best estimator found by grid search:")'''

    param_grid = [
        {'C':[0.0001, 0.001, 0.01], 'kernel':['linear'], 'class_weight':['balanced', None]},
        {'C':[0.0001, 0.001, 0.01], 'kernel':['rbf'],'gamma':[0.001, 0.0001], 'class_weight':['balanced', None]}
    ]
    clf = GridSearchCV(svm.SVC(verbose=True, probability=True), param_grid, verbose=True)
    clf.fit(features, labels)
    print(clf.best_estimator_)

    joblib.dump(clf, saved_classifier_filename)
    #with open(saved_classifier_filename, 'w') as f:
    #    pickle.dump(clf, f)
else:
    clf = joblib.load(saved_classifier_filename)

print(clf.score(features, labels))
