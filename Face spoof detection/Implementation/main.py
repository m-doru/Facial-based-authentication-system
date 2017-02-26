from __future__ import print_function

import argparse
import os
import time

import cv2

import numpy as np
import matplotlib.pyplot as plt
import openface
import features

fileDir = os.path.dirname(os.path.realpath(__file__))
modelDir = os.path.join(fileDir, 'models')
dlibModelDir = os.path.join(modelDir, 'dlib')
openfaceModelDir = os.path.join(modelDir, 'openface')


def initializeParser():
    parser = argparse.ArgumentParser()
    parser.add_argument('--verbose', action='store_true')
    parser.add_argument(
        '--dlibFacePredictor',
        type=str,
        help="Path to dlib's face predictor.",
        default=os.path.join(
            dlibModelDir,
            "shape_predictor_68_face_landmarks.dat"))
    parser.add_argument(
        '--captureDevice',
        type=int,
        default=0,
        help='Capture device. 0 for latop webcam and 1 for usb webcam')
    parser.add_argument('--width', type=int, default=320)
    parser.add_argument('--height', type=int, default=240)

    parser.add_argument('--imgDim', type=int,
                        help="Default image dimension.", default=96)
    return parser

def validateFace(face, lbp):
    cv2.imshow('face', face)

    greyAlignedFace = cv2.cvtColor(face, cv2.COLOR_BGR2GRAY)

    hist, bins, lbpFV = lbp.compute(greyAlignedFace)

    cv2.imshow('LBP', lbpFV)

    print("Aligned face size {}".format(face.shape))


def processFrame(rgbImage, align, args):
    start = time.time()

    if rgbImage is None:
        raise Exception("Unable to load image/frame")


    if args.verbose:
        print("  + Original size: {}".format(rgbImage.shape))
    if args.verbose:
        print("Loading the image took {} seconds.".format(time.time() - start))

    start = time.time()

    # Get all bounding boxes
    bb = align.getAllFaceBoundingBoxes(rgbImage)

    if bb is None:
        return None
    if args.verbose:
        print("Face detection took {} seconds".format(time.time() - start))

    start = time.time()

    alignedFaces = []

    for box in bb:
        alignedFaces.append(align.align(
            args.imgDim,
            rgbImage,
            box,
            landmarkIndices=openface.AlignDlib.OUTER_EYES_AND_NOSE))

    if alignedFaces is None:
        raise Exception("Unable to align the frame")
    if args.verbose:
        print("Alignment took {} seconds".format(time.time() - start))

    start = time.time()

    lbp = features.LocalBinaryPatterns(8,1)

    realFaces = []

    for alignedFace in alignedFaces:
        if validateFace(align, lbp):
            realFaces.append(alignedFace)
            cv2.imshow('validFace', alignedFace)
            cv2.waitKey(0)
        else:
            cv2.imshow('invalidFace', alignedFace)
            cv2.waitKey(0)

    return realFaces

def main():
    parser = initializeParser()
    args = parser.parse_args()


    video_capture = cv2.VideoCapture(0)
    video_capture.set(3, args.width)
    video_capture.set(4, args.height)

    frameNr = 0

    align = openface.AlignDlib(args.dlibFacePredictor)
    while True:
        ret, frame = video_capture.read()

        cv2.imshow('cameraFeed', frame)
        print("Processing frame number {}".format(frameNr))
        frameNr += 1
        if ret == False:
            print("No more input from video data source")
            break

        start = time.time()
        facesWithValidation = processFrame(frame, align, args)

        print("Entire processing of a frame took {}".format(time.time() - start))

    video_capture.release()
    cv2.destroyAllWindows()

if __name__ == '__main__':
    main()
