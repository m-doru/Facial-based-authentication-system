from vlfeat import vl_dsift
import cv2
import numpy as np
img = cv2.imread('data/face.jpg')
img = cv2.resize(img, (640, 480))

gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)

gray = gray.astype('float32')

print type(gray)
print gray.shape
import time
start = time.time()
frame, desc = vl_dsift(gray, 8, 16, fast = True, verbose = True)
print 'Computin the dsift of the full image took {}'.format(time.time() - start)

import numpy as np

a = np.transpose(desc)

print a.shape[0]*a.shape[1]
