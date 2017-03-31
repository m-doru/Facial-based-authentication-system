from sklearn import svm
from sklearn.cross_validation import PredefinedSplit
from sklearn.metrics import roc_curve, auc
from sklearn.metrics import confusion_matrix
from scipy.optimize import brentq
from scipy.interpolate import interp1d

import numpy as np
import joblib

from faceSpoofDetection import features
import dbfeatures
import feature_computer

# pickels filenames
saved_classifier_filename = '../classifiers/msu_mfsd.pkl'
saved_realfaces_features_filename = '../featuresVectors/msu_ussa_realfaces_features_joblib.pkl'
saved_spooffaces_features_filename = '../featuresVectors/msu_ussa_spooffaces_features_joblib.pkl'

# wheather to compute new features or load the features from saved files
load = True

# descriptor computer
mlbp_feature_computer = feature_computer.FrameFeatureComputer(features.MultiScaleLocalBinaryPatterns((8, 1), (24, 3),
                                                                                                    (40, 5)))
#mlbp_feature_computer = feature_computer.FrameFeatureComputer(features.LocalBinaryPatterns(8,1))


# compute feature vectors for every frame in the videos with real faces
if not load:
    print("Computing features for MSU USSA spoof faces")
    # copute feature vectors for every frame in the videos with spoof faces
    spoof_features_per_dir = dbfeatures.compute_spoofface_features_msu_ussa(mlbp_feature_computer, [1, 2, 3, 4, 5])
    #with open(saved_spooffaces_features_filename, 'w') as f:
    #    pickle.dump(spoof_features, f)
    joblib.dump(spoof_features_per_dir, saved_spooffaces_features_filename)

    print("Computing features for MSU USSA real faces")
    real_features = dbfeatures.compute_realface_features_msu_ussa(mlbp_feature_computer, [1,2,3,4,5])
    #with open(saved_realfaces_features_filename, 'w') as f:
        #pickle.dump(real_features, f)
    joblib.dump(real_features, saved_realfaces_features_filename)

else:
    print("Loading MSU USSA real faces features")
    #with open(saved_realfaces_features_filename, 'r') as f:
    #    real_features = pickle.load(f)
    real_features = joblib.load(saved_realfaces_features_filename)
    real_features = np.asarray(real_features)

    print("Loading MSU USSA spoof faces features")
    #with open(saved_spooffaces_features_filename, 'r') as f:
    #    spoof_features = pickle.load(f)
    spoof_features_per_dir = joblib.load(saved_spooffaces_features_filename)
    spoof_features_per_dir = np.asarray(spoof_features_per_dir)

# create the necessary labels
labels_real = np.asarray([1 for _ in range(len(real_features))])
#---labels_spoof = [-1 for _ in range(len(spoof_features_per_dir))]
labels_spoof_per_dir = np.asarray([[-1 for _ in range(len(spoof_features_per_dir[0]))] for _ in range(len(
        spoof_features_per_dir))])

# create the full features and corresponding labels
#features = np.asarray(real_features + spoof_features)
#---labels = np.asarray(labels_real + labels_spoof)

# here I should do a cross validation on the features
'''
param_grid = [
        {'C': [0.0001, 0.001, 0.01], 'kernel':['linear'], 'class_weight':['balanced', None]},
        {'C': [0.0001, 0.001, 0.01], 'kernel':['rbf'],'gamma':[0.0001, 0.001], 'class_weight':['balanced', None]}
    ]
'''

ps = PredefinedSplit(test_fold=dbfeatures.compute_msu_ussa_subjects_folds_arr())

clf = svm.SVC(verbose=True, probability=True, C=0.0001, kernel='linear', class_weight='balanced')

folds_eer = []
threshes = []
confusion_matrices = []
for train_index, test_index in ps:
    # split the features into current train and test folds
    train_features = real_features[train_index]
    test_features = real_features[test_index]
    train_labels = labels_real[train_index]
    test_labels = labels_real[test_index]
    for i in range(len(spoof_features_per_dir)):
        train_features = np.append(train_features, spoof_features_per_dir[i][train_index])
        test_features = np.append(test_features, spoof_features_per_dir[i][test_index])
        train_labels = np.append(train_labels, labels_spoof_per_dir[i][train_index])
        test_labels = np.append(test_labels, labels_spoof_per_dir[i][test_index])


    #train the classifier
    clf.fit(train_features, train_labels)

    #use the classifier to predict the labels for test_features
    pred_labels = clf.predict(test_features)

    #create the roc curve
    fpr, tpr, threshold = roc_curve(test_labels, pred_labels, pos_label=1)

    # compute the equal error rate
    eer = brentq(lambda x: 1. - x - interp1d(fpr, tpr)(x), 0., 1.)
    thresh = interp1d(fpr, threshold)(eer)

    folds_eer.append(eer)
    threshes.append(thresh)

    conf_mat = confusion_matrix(test_labels, pred_labels)
    confusion_matrices.append(conf_mat)

# print the mean and standard deviation of equal error rate across the folds
print(np.mean(folds_eer), np.std(folds_eer))
for conf_mat in confusion_matrices:
    print(conf_mat)