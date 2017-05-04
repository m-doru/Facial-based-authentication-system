import os
import openface
import cv2
import time
import numpy as np

class Face:
    fileDir = os.path.dirname(os.path.realpath(__file__))
    modelDir = os.path.join(fileDir,'..', 'models')
    dlibModelDir = os.path.join(modelDir, 'dlib')
    openfaceModelDir = os.path.join(modelDir, 'openface')
    dlipFacePredictor = os.path.join(dlibModelDir, "shape_predictor_68_face_landmarks.dat")
    networkModel = os.path.join(openfaceModelDir, 'nn4.small2.v1.t7')
    aligner = openface.AlignDlib(dlipFacePredictor)
    imgDim = 96
    net = openface.TorchNeuralNet(networkModel, imgDim)

    def __init__(self,id, representation, filepath = None):
        self.id = id
        self.representation = representation
        self.filepath = filepath



    def compute_distance(self, other_rep):
        diff = self.representation - other_rep
        return np.dot(diff, diff)

    # Class methods
    @classmethod
    def fromImagePath(cls, filepath):
        id = cls._compute_id(filepath)
        representation = cls.getNetRep(filepath, False, cls.imgDim)
        return cls(id, representation, filepath)

    @classmethod
    def fromImage(cls, id, image):
        representation = cls.getNetRep(None, False, cls.imgDim, image)
        return cls(id, representation)

    @classmethod
    def _compute_id(cls,filepath):
        filename = filepath.split(os.pathsep)[-1].split('.')[0]
        return filename.split('_')[0]

    @classmethod
    def getNetRep(cls, imgPath, verbose, imgDim, image=None):
        if imgPath is not None:
            if verbose:
                print("Processing {}.".format(imgPath))
            bgrImg = cv2.imread(imgPath)
            if bgrImg is None:
                raise Exception("Unable to load image: {}".format(imgPath))
        elif image is not None:
            bgrImg = image
        else:
            raise Exception("No path or image given to compute network representation")
        rgbImg = cv2.cvtColor(bgrImg, cv2.COLOR_BGR2RGB)

        if verbose:
            print("  + Original size: {}".format(rgbImg.shape))

        start = time.time()
        bbs = Face.aligner.getAllFaceBoundingBoxes(rgbImg)
        if bbs is None:
            raise Exception("Unable to find a face: {}".format(imgPath))
        elif len(bbs) > 1:
            raise Exception("Found more than a face in: {}".format(imgPath))
        if verbose:
            print("  + Face detection took {} seconds.".format(time.time() - start))

        bb = bbs[0]

        start = time.time()
        alignedFace = Face.aligner.align(imgDim, rgbImg, bb,
                                         landmarkIndices=openface.AlignDlib.OUTER_EYES_AND_NOSE)
        if alignedFace is None:
            raise Exception("Unable to align image: {}".format(imgPath))
        if verbose:
            print("  + Face alignment took {} seconds.".format(time.time() - start))

        start = time.time()
        rep = Face.net.forward(alignedFace)
        if verbose:
            print("  + OpenFace forward pass took {} seconds.".format(time.time() - start))
            print("Representation:")
            print(rep)
            print("-----\n")
        return rep
