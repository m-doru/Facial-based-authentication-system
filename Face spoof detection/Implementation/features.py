from skimage import feature
import numpy as np

class LocalBinaryPatterns:
    def __init__(self, numPoints, radius):
        self.numPoints = numPoints
        self.radius = radius

    def compute(self, image, eps=1e-7):
        #compute the local binary pattern representation
        #and maybe use it to compute the histogram
        lbp = feature.local_binary_pattern(image, self.numPoints,
                                           self.radius, method="default")
        #(hist, bins) = np.histogram(lbp.ravel(), bins=np.arange(0, self.numPoints+3),
        #                        range=(0, self.numPoints+2))
        (hist, bins) = np.histogram(lbp, normed=True, bins='auto')
        #hist = hist.astype("float")
        #hist /= (hist.sum() + eps)

        return hist, bins, lbp