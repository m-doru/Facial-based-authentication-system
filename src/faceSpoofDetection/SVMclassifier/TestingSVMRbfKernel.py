from sklearn import svm
from plot_roc_curve import plot_roc_curve
from sklearn.preprocessing import label_binarize
import random



clf = svm.SVC(verbose=True, probability=True, C=0.001, kernel='rbf', gamma=0.001, class_weight='balanced')

train_data = [(random.uniform(30, 70), random.uniform(-50, -10), random.uniform(-60, -30)) for _ in range(1000)] + \
             [(random.uniform(-70, -30), random.uniform(10, 50), random.uniform(20, 60)) for _ in range(1000)]

train_labels = [1 for _ in range(1000)] + [-1 for _ in range(1000)]

clf.fit(train_data, train_labels)

test_data = [(random.uniform(30, 70), random.uniform(-50, -10), random.uniform(-60, -30)) for _ in range(500)] + \
             [(random.uniform(-70, -30), random.uniform(10, 50), random.uniform(20, 60)) for _ in range(500)]

test_labels = [-1 for _ in range(500)] + [1 for _ in range(500)]

test_labels_bin = label_binarize(test_labels, classes=[1, -1])

pred_conf = clf.predict_proba(test_data)

plot_roc_curve(test_labels_bin, pred_conf)
