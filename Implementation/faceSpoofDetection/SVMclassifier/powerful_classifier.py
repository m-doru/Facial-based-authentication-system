from __future__ import print_function
from sklearn import svm
from sklearn.preprocessing import label_binarize
from plot_roc_curve import plot_roc_curve

from sklearn.metrics import roc_curve, accuracy_score, confusion_matrix, roc_auc_score
from scipy.optimize import brentq
from scipy.interpolate import interp1d

import joblib
import idiap_classifier
import casia_classifier
import msu_mfsd_classifier
import msu_ussa_classifier

import feature_computer
from faceSpoofDetection import features

mlbp_feature_computer = feature_computer.FrameFeatureComputer(features.MultiScaleLocalBinaryPatterns((8, 1), (8, 2),
                                                                                                               (16, 2)))

classifier_name = 'powerful_classifier.pkl'
classifier_path = '../classifiers/'+classifier_name

(idiap_train_features, idiap_train_labels) = idiap_classifier.get_train_features_and_labels(True, mlbp_feature_computer)
print('Loaded idiap training features')
(idiap_test_features, idiap_test_labels) = idiap_classifier.get_test_features_and_labels(True, mlbp_feature_computer)
print('Loaded idiap test features')

(casia_train_features, casia_train_labels) = casia_classifier.get_train_features_and_labels(True,
                                                                                            mlbp_feature_computer)
print('Loaded casia training features')
(casia_test_features, casia_test_labels) = casia_classifier.get_test_features_and_labels(True, mlbp_feature_computer)
print('Loaded casia test features')

(mfsd_train_features, mfsd_train_labels) = msu_mfsd_classifier.get_train_features_and_labels(True,
                                                                                             mlbp_feature_computer)
print('Loaded msu mfsd training features')
(mfsd_test_features, mfsd_test_labels) = msu_mfsd_classifier.get_test_features_and_labels(True, mlbp_feature_computer)
print('Loaded msu mfsd test features')
print(len(mfsd_train_features[0]))

(ussa_real_features, ussa_spoof_features_per_dir, ussa_real_labels, ussa_spoof_labels_per_dir) = \
    msu_ussa_classifier.get_features_and_labels(True, mlbp_feature_computer, False)
print('Loaded msu ussa features')
ussa_features = ussa_real_features
ussa_labels = ussa_real_labels
print(len(ussa_real_features[0]))
for i in range(len(ussa_spoof_features_per_dir)):
    ussa_features.extend(ussa_spoof_features_per_dir[i])
    print(len(ussa_spoof_features_per_dir[i][0]))
    ussa_labels.extend(ussa_spoof_labels_per_dir[i])

train_data = []
train_labels = []
test_data = []
test_labels = []

train_data.extend(idiap_train_features)
train_labels.extend(idiap_train_labels)
test_data.extend(idiap_test_features)
test_labels.extend(idiap_test_labels)

train_data.extend(casia_train_features)
train_labels.extend(casia_train_labels)
test_data.extend(casia_test_features)
test_labels.extend(casia_test_labels)

train_data.extend(mfsd_train_features)
train_labels.extend(mfsd_train_labels)
test_data.extend(mfsd_test_features)
test_labels.extend(mfsd_test_labels)

train_data.extend(ussa_features)
train_labels.extend(ussa_labels)


clf = svm.SVC(verbose=True, probability=True, C=1, kernel='poly')

print("Starting training the classifier")
clf.fit(train_data, train_labels)
print("Classifier trained")

joblib.dump(clf, classifier_path)


test_labels_bin = label_binarize(test_labels, classes=[-1, 1])

print('Starting classification of test data')
pred_labels = clf.predict(test_data)
pred_confidences = clf.predict_proba(test_data)

plot_roc_curve(test_labels_bin, pred_confidences)

roc_auc = roc_auc_score(test_labels, pred_confidences[:, 1])
print('ROC area under the curve score {}'.format(roc_auc))

# compute the equal error rate
fpr, tpr, _ = roc_curve(test_labels, pred_confidences[:, 1])
eer = brentq(lambda x: 1. - x - interp1d(fpr, tpr)(x), 0., 1.)
print('Equal error rate {}'.format(eer))

print('Accuracy score {}'.format(accuracy_score(test_labels, pred_labels)))
print('Confusion matrix {}'.format(confusion_matrix(test_labels, pred_labels)))
