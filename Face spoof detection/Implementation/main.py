from __future__ import print_function

import argparse
import os
import time

import cv2

import numpy as np
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


def processFrame(bgrImage, args):
    align = openface.AlignDlib(args.dlibFacePredictor)

    start = time.time()

    if bgrImage is None:
        raise Exception("Unable to load image/frame")

    rgbImg = cv2.cvtColor(bgrImage, cv2.COLOR_BGR2RGB)

    if args.verbose:
        print("  + Original size: {}".format(bgrImage.shape))
    if args.verbose:
        print("Loading the image took {} seconds.".format(time.time() - start))

    start = time.time()

    # Get all bounding boxes

    bb = align.getAllFaceBoundingBoxes(rgbImg)

    if bb is None:
        return None
    if args.verbose:
        print("Face detection took {} seconds".format(time.time() - start))

    start = time.time()

    alignedFaces = []

    for box in bb:
        alignedFaces.append(align.align(
            args.imgDim,
            rgbImg,
            box,
            landmarkIndices=openface.AlignDlib.OUTER_EYES_AND_NOSE))

    if alignedFaces is None:
        raise Exception("Unable to align the frame")
    if args.verbose:
        print("Alignment took {} seconds".format(time.time() - start))

    start = time.time()

    lbp = features.LocalBinaryPatterns(8, 1)

    for alignedFace in alignedFaces:
        cv2.imshow('face', alignedFace)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    if args.verbose:
        print("Processing aligned faces took {} seconds".format(time.time() - start))


def main():
    parser = initializeParser()
    args = parser.parse_args()


    video_capture = cv2.VideoCapture('output.avi')
    video_capture.set(3, args.width)
    video_capture.set(4, args.height)

    frameNr = 0
    while True:
        ret, frame = video_capture.read()

        print("Processing frame number {}".format(frameNr))
        frameNr += 1

        if ret == False:
            print("No more input from video data source")
            break

        facesWithValidation = processFrame(frame, args)

    video_capture.release()
    cv2.destroyAllWindows()

if __name__ == '__main__':
    main()
