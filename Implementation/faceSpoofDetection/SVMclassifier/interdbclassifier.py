from __future__ import print_function
from sklearn import svm
from sklearn.preprocessing import label_binarize
from plot_roc_curve import plot_roc_curve
import joblib
import idiap_classifier, casia_classifier, msu_mfsd_classifier, msu_ussa_classifier

tested_on = 2

classifier_name = 'classifier_tested_on' + str(tested_on) + '.pkl'
classifier_path = '../classifiers/'+classifier_name

load_classifier = False

(idiap_train_features, idiap_train_labels) = idiap_classifier.get_train_features_and_labels(True)
print('Loaded idiap training features')
(casia_train_features, casia_train_labels) = casia_classifier.get_train_features_and_labels(True)
print('Loaded casia training features')
(mfsd_train_features, mfsd_train_labels) = msu_mfsd_classifier.get_train_features_and_labels(True)
print('Loaded msu mfsd training features')
(ussa_real_features, ussa_spoof_features_per_dir, ussa_real_labels, ussa_spoof_labels_per_dir) = \
    msu_ussa_classifier.get_features_and_labels(True, None, False)
print('Loaded msu ussa training features')

ussa_features = ussa_real_features
ussa_labels = ussa_real_labels
for i in range(len(ussa_spoof_features_per_dir)):
    ussa_features.extend(ussa_spoof_features_per_dir[i])
    ussa_labels.extend(ussa_spoof_labels_per_dir[i])

data = [idiap_train_features, casia_train_features, mfsd_train_features, ussa_features]
labels = [idiap_train_labels, casia_train_labels, mfsd_train_labels, ussa_labels]

if load_classifier:
    clf = joblib.load(classifier_path)
    print('Loaded classifier from ' + classifier_path)
else:
    clf = svm.SVC(verbose=True, probability=True, C=0.001, kernel='linear', class_weight='balanced')
    training_data = []
    training_labels = []
    for i in range(len(data)):
        if i == tested_on:
            continue
        training_data.extend(data[i])
        training_labels.extend(labels[i])

    print('Started classifier training')
    clf.fit(training_data, training_labels)
    print('Classifier trained')
    joblib.dump(clf, classifier_path)

test_data = data[tested_on]
test_labels = labels[tested_on]


test_labels_bin = label_binarize(test_labels, classes=[-1,1])

print('Starting classification of test data')
pred_labels = clf.predict(test_data)
pred_confidences = clf.predict_proba(test_data)

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
