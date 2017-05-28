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


def test_on_ussa():
    pass

tested_on = 3

classifier_name = 'classifier_tested_on' + str(tested_on) + '.pkl'
classifier_path = '../classifiers/'+classifier_name

load_classifier = False

if tested_on != 0:
    (idiap_train_features, idiap_train_labels) = idiap_classifier.get_train_features_and_labels(True)
    print('Loaded idiap training features')
else:
    idiap_train_features = []
    idiap_train_labels = []
(idiap_test_features, idiap_test_labels) = idiap_classifier.get_test_features_and_labels(True)
print('Loaded idiap test features')

if tested_on != 1:
    (casia_train_features, casia_train_labels) = casia_classifier.get_train_features_and_labels(True)
    print('Loaded casia training features')
else:
    casia_train_features = []
    casia_train_labels = []
(casia_test_features, casia_test_labels) = casia_classifier.get_test_features_and_labels(True)
print('Loaded casia test features')

if tested_on != 2:
    (mfsd_train_features, mfsd_train_labels) = msu_mfsd_classifier.get_train_features_and_labels(True)
    print('Loaded msu mfsd training features')
else:
    mfsd_train_features = []
    mfsd_train_labels = []
(mfsd_test_features, mfsd_test_labels) = msu_mfsd_classifier.get_test_features_and_labels(True)
print('Loaded msu mfsd test features')

(ussa_real_features, ussa_spoof_features_per_dir, ussa_real_labels, ussa_spoof_labels_per_dir) = \
    msu_ussa_classifier.get_features_and_labels(True, None, False)
print('Loaded msu ussa features')
ussa_features = ussa_real_features
ussa_labels = ussa_real_labels
for i in range(len(ussa_spoof_features_per_dir)):
    ussa_features.extend(ussa_spoof_features_per_dir[i])
    ussa_labels.extend(ussa_spoof_labels_per_dir[i])


train_data = [idiap_train_features, casia_train_features, mfsd_train_features, ussa_features]
train_labels = [idiap_train_labels, casia_train_labels, mfsd_train_labels, ussa_labels]
test_data = [idiap_test_features, casia_test_features, mfsd_test_features,[]]
test_labels = [idiap_test_labels, casia_test_labels, mfsd_test_labels, []]

if load_classifier:
    clf = joblib.load(classifier_path)
    print('Loaded classifier from ' + classifier_path)
else:
    clf = svm.SVC(verbose=True, probability=True, C=0.001, kernel='linear', class_weight='balanced')
    training_data = []
    training_labels = []
    for i in range(len(train_data)):
        if i == tested_on:
            continue
        training_data.extend(train_data[i])
        training_labels.extend(train_labels[i])
        training_data.extend(test_data[i])
        training_labels.extend(test_labels[i])

    print('Started classifier training')
    clf.fit(training_data, training_labels)
    print('Classifier trained')
    joblib.dump(clf, classifier_path)

if tested_on == 3:
    testing_data = ussa_features
    testing_labels = ussa_labels
else:
    testing_data = test_data[tested_on]
    testing_labels = test_labels[tested_on]

test_labels_bin = label_binarize(testing_labels, classes=[-1, 1])

print('Starting classification of test data')
pred_labels = clf.predict(testing_data)
pred_confidences = clf.predict_proba(testing_data)

plot_roc_curve(test_labels_bin, pred_confidences)

roc_auc = roc_auc_score(testing_labels, pred_confidences[:, 1])
print('ROC area under the curve score {}'.format(roc_auc))

# compute the equal error rate
fpr, tpr, _ = roc_curve(testing_labels, pred_confidences[:, 1])
eer = brentq(lambda x: 1. - x - interp1d(fpr, tpr)(x), 0., 1.)
print('Equal error rate {}'.format(eer))

print('Accuracy score {}'.format(accuracy_score(testing_labels, pred_labels)))
print('Confusion matrix {}'.format(confusion_matrix(testing_labels, pred_labels)))
