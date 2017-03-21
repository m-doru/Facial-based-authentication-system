import numpy as np
from skimage import feature
from vlfeat import vl_dsift


class LocalBinaryPatterns:
    def __init__(self, numPoints, radius, method='uniform'):
        self.numPoints = numPoints
        self.radius = radius
        self.binsRange = np.arange(0, self.numPoints+3)
        self.method = method

    def compute(self, image, eps=1e-7):
        #compute the local binary pattern representation
        lbp = feature.local_binary_pattern(image, self.numPoints,
                                           self.radius, method=self.method)
        # uniform method means that we are making the histogrm from uniform patterns (values that have only one
        # change like 10000000 or 00100000) and all the non-uniform patterns that appear are assigned to a single bin
        # In the idea that we will use Multi-scale LBP, using other method like default is not suitable given the
        # large maximum value that such a method would give. For example for P = 40

        (hist, bins) = np.histogram(lbp,
                                    #normed=True,
                                    bins=self.binsRange,
                                    #defines the edges of the bins including the rightmost one
                                    range=(0, self.numPoints+2)
                                    #defines the lower and upper range of the bins
                                    )

        return hist, bins, lbp



class MultiScaleLocalBinaryPatterns:
    def __init__(self, *scales):
        self.lbps = []
        for i in range(0, len(scales)):
            lbp = LocalBinaryPatterns(scales[i][0], scales[i][1])
            self.lbps.append(lbp)

    def computeFeaturePatchWise(self, matrix):
        lbpFeature = []
        for lbpIndex in range(0, len(self.lbps)):
            for i in xrange(0, matrix.shape[0]-33, 32):
                for j in xrange(0, matrix.shape[1] - 33, 16):
                    patch = matrix[i:i+32, j:j+32]
                    (lbpPatchFeature, _, _) = self.lbps[lbpIndex].compute(patch)
                    lbpFeature = lbpFeature + lbpPatchFeature.tolist()

        return lbpFeature

    def computeFeatureImageWise(self, matrix):
        lbpFeature = []

        for lbpIndex in range(0, len(self.lbps)):
            lbp = self.lbps[lbpIndex]
            (_, _, lbpRep) = lbp.compute(matrix)

            for i in xrange(0, lbpRep.shape[0]-33, 32):
                for j in xrange(0, lbpRep.shape[1]-33, 16):
                    patch = lbpRep[i:i+32, j:j+32]
                    (hist, _) = np.histogram(patch,
                                             #normed=True,
                                             bins=lbp.binsRange,
                                             range = (0, lbp.numPoints+2))
                    lbpFeature = lbpFeature + hist.tolist()

        return lbpFeature



class DSIFT:
    def compute(self, image, step, size):
        kp, desc = vl_dsift(image, step = step, size = size, fast=True)

        return kp, desc
