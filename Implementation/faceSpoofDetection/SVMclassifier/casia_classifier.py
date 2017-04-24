import os

from sklearn import svm
import joblib
from sklearn.grid_search import GridSearchCV
from sklearn.preprocessing import label_binarize

import dbfeatures
import feature_computer
from plot_roc_curve import plot_roc_curve
from faceSpoofDetection import features

# pickels filenames
extension = '.pkl'
version = 'redchannel'
saved_classifier_filename = '../classifiers/casia.pkl'
saved_realfaces_train_features_filename = '../featuresVectors/casia_realfaces_features_' + version + extension
saved_spooffaces_train_features_filename = '../featuresVectors/casia_spooffaces_features_' + version + extension
saved_realfaces_test_features_filename = '../featuresVectors/casia_realfaces_test_features_' + version + extension
saved_spooffaces_test_features_filename ='../featuresVectors/casia_spooffaces_test_features_' + version + extension

# load or recompute train features
load_train_features = None
# retrain or load classifier
load_classifier = True
# load or recompute test features
load_test_features = True

# descriptor computer
mlbp_feature_computer = feature_computer.FrameFeatureComputer(features.MultiScaleLocalBinaryPatterns((8, 1), (24, 3),
                                                                                                           (40, 5)))
if load_train_features == False:
    # compute feature vectors for every frame in the videos with real faces
    real_features_train = dbfeatures.compute_realface_features_casia(mlbp_feature_computer)
    joblib.dump(real_features_train, saved_realfaces_train_features_filename)


    # compute feature vectors for every frame in the videos with spoof faces
    spoof_features_train = dbfeatures.compute_spoofface_features_casia(mlbp_feature_computer)
    joblib.dump(spoof_features_train, saved_spooffaces_train_features_filename)
elif load_train_features == True:
    real_features_train = joblib.load(saved_realfaces_train_features_filename)
    spoof_features_train = joblib.load(saved_spooffaces_train_features_filename)

if load_train_features is not None:
    # create the necessary labels
    labels_real = [1 for _ in range(len(real_features_train))]
    labels_spoof = [-1 for _ in range(len(spoof_features_train))]

    # create the full features and corresponding labels
    train_features = real_features_train + spoof_features_train
    train_labels = labels_real + labels_spoof

if not load_classifier:
    '''
    param_grid = [
        {'C': [0.0001, 0.001, 0.01], 'kernel':['linear'], 'class_weight':['balanced', None]},
        {'C': [0.0001, 0.001, 0.01], 'kernel':['rbf'],'gamma':[0.0001, 0.001], 'class_weight':['balanced', None]}
    ]
    clf = GridSearchCV(svm.SVC(verbose=True, probability=True), param_grid, verbose=True)
    '''
    clf = svm.SVC(verbose=True, probability=True, C = 0.0001, kernel='linear', class_weight='balanced')
    clf.fit(train_features, train_labels)

    #print("Best estimator found by grid search:")
    #print(clf.best_estimator_)

    joblib.dump(clf, saved_classifier_filename)
else:
    clf = joblib.load(saved_classifier_filename)


if not load_test_features:
    real_features_test = dbfeatures.compute_realface_features_casia(mlbp_feature_computer,train=False)
    joblib.dump(real_features_test,saved_realfaces_test_features_filename)

    spoof_features_test = dbfeatures.compute_spoofface_features_casia(mlbp_feature_computer, train=False)
    joblib.dump(spoof_features_test, saved_spooffaces_test_features_filename)
else:
    real_features_test = joblib.load(saved_realfaces_test_features_filename)
    spoof_features_test = joblib.load(saved_spooffaces_test_features_filename)

test_labels_real = [1 for _ in range(len(real_features_test))]
test_labels_spoof = [-1 for _ in range(len(spoof_features_test))]

test_features = real_features_test + spoof_features_test
test_labels = test_labels_real + test_labels_spoof
test_labels_bin = label_binarize(test_labels, classes=[-1,1])


pred_labels = clf.predict(test_features)
pred_confidences = clf.predict_proba(test_features)

plot_roc_curve(test_labels_bin, pred_confidences)

from sklearn.metrics import roc_curve, accuracy_score,confusion_matrix, roc_auc_score, auc
from scipy.optimize import brentq
from scipy.interpolate import interp1d

roc_auc = roc_auc_score(test_labels, pred_confidences[:,1])
print('ROC area under the curve score {}'.format(roc_auc))

# compute the equal error rate
fpr, tpr, _ = roc_curve(test_labels, pred_confidences[:,1])
eer = brentq(lambda x: 1. - x - interp1d(fpr, tpr)(x), 0., 1.)
print('Equal error rate {}'.format(eer))

print('Accuracy score {}'.format(accuracy_score(test_labels, pred_labels)))
print('Confusion matrix {}'.format(confusion_matrix(test_labels, pred_labels)))