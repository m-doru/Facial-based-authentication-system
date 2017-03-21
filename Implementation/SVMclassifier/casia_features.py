from sklearn import svm
from sklearn.externals import joblib
import dbfeatures

saved_classifier_filename = 'casia.pkl'

real_features = dbfeatures.compute_realface_features_casia()
spoof_features = dbfeatures.compute_spoofface_features_casia()

labels_real = [1 for _ in range(len(real_features))]
labels_spoof = [0 for _ in range(len(spoof_features))]

features = real_features + spoof_features
labels = labels_real + labels_spoof

clf = svm.SVC()
clf.fit(features, labels)

joblib.dump(clf, saved_classifier_filename)