from sklearn.metrics import roc_curve, accuracy_score,confusion_matrix, roc_auc_score, auc
import numpy as np
import time
import matplotlib.pyplot as plt

def plot_roc_curve(y_test, y_score):
    n_classes = y_test.shape[1]
    fpr = dict()
    tpr = dict()
    roc_auc = dict()
    for i in range(n_classes):
        fpr[i], tpr[i], _ = roc_curve(y_test, y_score[:,i])
        roc_auc[i] = auc(fpr[i], tpr[i])

    fpr['micro'], tpr['micro'], _ = roc_curve(np.append(y_test.ravel(), y_test.ravel()), y_score.ravel())
    roc_auc['micro'] = auc(fpr['micro'], tpr['micro'])

    for i in range(n_classes):
        plt.figure()
        plt.plot(fpr[i], tpr[i], label='ROC curve (area = %0.2f)' % roc_auc[i])
        plt.plot([0, 1], [0, 1], 'k--')
        plt.xlim([0.0, 1.0])
        plt.ylim([0.0, 1.05])
        plt.xlabel('False Positive Rate')
        plt.ylabel('True Positive Rate')
        plt.title('Receiver operating characteristic example')
        plt.legend(loc="lower right")
        plt.show()

