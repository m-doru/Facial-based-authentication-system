from __future__ import print_function

import argparse
import os
import time

import cv2

import openface

fileDir = os.path.dirname(os.path.realpath(__file__))
modelDir = os.path.join(fileDir, '..', 'models')
dlibModelDir = os.path.join(modelDir, 'dlib')
openfaceModelDir = os.path.join(modelDir, 'openface')

class FaceDetector:
    def __init__(self, face_dim=144, image_downsampling_factors = (0.5, 0.5), verbose=False):
        self.face_dim = face_dim
        self.image_downsampling_factors = image_downsampling_factors
        self.verbose = verbose
        self.dlib_face_predictor = os.path.join(dlibModelDir,"shape_predictor_68_face_landmarks.dat")
        self.align = openface.AlignDlib(self.dlib_face_predictor)


    def get_faces_in_frame(self, rgb_image):
        if rgb_image is None:
            raise Exception("Unable to load image/frame")


        if self.verbose:
            print("  + Original size: {}".format(rgb_image.shape))

        rgb_image = cv2.resize(rgb_image, (0,0), fx=self.image_downsampling_factors[0],
                               fy=self.image_downsampling_factors[1])

        start = time.time()

        # Get all bounding boxes
        bb = self.align.getAllFaceBoundingBoxes(rgb_image)

        if bb is None:
            return None
        if self.verbose:
            print("Face detection took {} seconds".format(time.time() - start))

        start = time.time()

        #Get detected faces aligned
        aligned_faces = []

        for box in bb:
            if box.top() > 0 and box.bottom() > 0 and box.left() > 0 and box.right() > 0:
                aligned_faces.append(rgb_image[box.top():box.bottom(), box.left():box.right()].copy())

        if aligned_faces is None:
            raise Exception("Unable to crop faces")
        if self.verbose:
            print("Cropping took {} seconds".format(time.time() - start))

        return aligned_faces

    def get_aligned_faces_in_frame(self, rgb_image):
        if rgb_image is None:
            raise Exception("Unable to load image/frame")


        if self.verbose:
            print("  + Original size: {}".format(rgb_image.shape))

        rgb_image = cv2.resize(rgb_image, (0,0), fx=self.image_downsampling_factors[0],
                               fy=self.image_downsampling_factors[1])

        start = time.time()

        # Get all bounding boxes
        bb = self.align.getAllFaceBoundingBoxes(rgb_image)

        if bb is None:
            return None
        if self.verbose:
            print("Face detection took {} seconds".format(time.time() - start))

        start = time.time()

        #Get detected faces aligned
        aligned_faces = []

        for box in bb:
            aligned_faces.append(self.align.align(
                self.face_dim,
                rgb_image,
                box,
                landmarkIndices=openface.AlignDlib.OUTER_EYES_AND_NOSE))

        if aligned_faces is None:
            raise Exception("Unable to align the frame")
        if self.verbose:
            print("Alignment took {} seconds".format(time.time() - start))

        return aligned_faces
