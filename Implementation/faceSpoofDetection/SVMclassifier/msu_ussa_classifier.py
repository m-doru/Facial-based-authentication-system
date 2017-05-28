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

def get_features_and_labels(load_train_features, mlbp_feature_computer, np_array=True):
    saved_realfaces_features_filename = '../featuresVectors/msu_ussa_realfaces_features_joblib.pkl'
    saved_spooffaces_features_filename = '../featuresVectors/msu_ussa_spooffaces_features_joblib.pkl'

    if load_train_features == False:
        print("Computing features for MSU USSA spoof faces")
        # copute feature vectors for every frame in the videos with spoof faces
        spoof_features_per_dir = dbfeatures.compute_spoofface_features_msu_ussa(mlbp_feature_computer, [1, 2, 3, 4, 5])
        joblib.dump(spoof_features_per_dir, saved_spooffaces_features_filename)

        print("Computing features for MSU USSA real faces")
        real_features = dbfeatures.compute_realface_features_msu_ussa(mlbp_feature_computer, [1,2,3,4,5])
        joblib.dump(real_features, saved_realfaces_features_filename)

    elif load_train_features == True:
        print("Loading MSU USSA real faces features")
        real_features = joblib.load(saved_realfaces_features_filename)

        print("Loading MSU USSA spoof faces features")
        spoof_features_per_dir = joblib.load(saved_spooffaces_features_filename)

        if np_array:
            real_features = np.asarray(real_features)
            spoof_features_per_dir = np.asarray([np.asarray(spoof_features_per_dir[i]) for i in range(len(
                spoof_features_per_dir))])

    if load_train_features is not None:
        # create the necessary labels
        if np_array:
            labels_real = np.asarray([1 for _ in range(len(real_features))])

            labels_spoof_per_dir = np.asarray([np.asarray([-1 for _ in range(len(spoof_features_per_dir[i]))]) for i
                                               in range(len(
                spoof_features_per_dir))])
        else:
            labels_real = [1 for _ in range(len(real_features))]
            labels_spoof_per_dir = [[-1 for _ in range(len(spoof_features_per_dir[i]))] for i in range(len(
                spoof_features_per_dir))]
        #---labels_spoof = [-1 for _ in range(len(spoof_features_per_dir))]

    return (real_features, spoof_features_per_dir, labels_real, labels_spoof_per_dir)

def main():

    # pickels filenames
    saved_classifier_filename = '../classifiers/msu_mfsd.pkl'

    # load or recompute train features. If none, the train features are not loaded into memory
    load_train_features = True
    # retrain or load classifier
    load_classifier = True
    # load or recompute test features
    load_test_features = True
    # descriptor computer

    mlbp_feature_computer = feature_computer.FrameFeatureComputer(features.MultiScaleLocalBinaryPatterns((8,1), (8,2),
                                                                                                         (16,2)))
    #mlbp_feature_computer = feature_computer.FrameFeatureComputer(features.LocalBinaryPatterns(8,1))

    (real_features, spoof_features_per_dir, labels_real, labels_spoof_per_dir) = get_features_and_labels(
        load_train_features, mlbp_feature_computer)

    # here I should do a cross validation on the features
    '''
    param_grid = [
            {'C': [0.0001, 0.001, 0.01], 'kernel':['linear'], 'class_weight':['balanced', None]},
            {'C': [0.0001, 0.001, 0.01], 'kernel':['rbf'],'gamma':[0.0001, 0.001], 'class_weight':['balanced', None]}
        ]
    '''
    test_fold = dbfeatures.compute_msu_ussa_subjects_folds_arr()
    ps = PredefinedSplit(test_fold=test_fold)

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
            train_features = np.concatenate((train_features, spoof_features_per_dir[i][train_index]), 0)
            test_features = np.concatenate((test_features, spoof_features_per_dir[i][test_index]),0)
            train_labels = np.concatenate((train_labels, labels_spoof_per_dir[i][train_index]),0)
            test_labels = np.concatenate((test_labels, labels_spoof_per_dir[i][test_index]),0)

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

if __name__=='__main__':
    main()