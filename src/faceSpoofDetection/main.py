from __future__ import print_function

import argparse
import os
import time

import cv2

from . import faceSpoofValidation
from . import features
from . import openface

fileDir = os.path.dirname(os.path.realpath(__file__))
modelDir = os.path.join(fileDir, "..", "models")
dlibModelDir = os.path.join(modelDir, "dlib")
openfaceModelDir = os.path.join(modelDir, "openface")


def initializeParser():
    parser = argparse.ArgumentParser()
    parser.add_argument("--verbose", action="store_true")
    parser.add_argument(
        "--dlibFacePredictor",
        type=str,
        help="Path to dlib's face predictor.",
        default=os.path.join(dlibModelDir, "shape_predictor_68_face_landmarks.dat"),
    )
    parser.add_argument(
        "--captureDevice",
        type=int,
        default=0,
        help="Capture device. 0 for latop webcam and 1 for usb webcam",
    )
    parser.add_argument("--width", type=int, default=640)
    parser.add_argument("--height", type=int, default=480)

    parser.add_argument(
        "--imgDim", type=int, help="Default image dimension.", default=144
    )

    parser.add_argument(
        "--scaleX",
        type=float,
        help="Scale to resize the feed image for faster processing",
        default=1,
    )
    parser.add_argument(
        "--scaleY",
        type=float,
        help="Scale to resize the feed image for faster processing",
        default=1,
    )
    return parser


def processFrame(rgb_image, align, faceSpoofValidator, args):
    start = time.time()

    if rgb_image is None:
        raise Exception("Unable to load image/frame")

    if args.verbose:
        print("  + Original size: {}".format(rgb_image.shape))
    if args.verbose:
        print("Loading the image took {} seconds.".format(time.time() - start))

    originalRGBImage = rgb_image
    rgb_image = cv2.resize(rgb_image, (0, 0), fx=args.scaleX, fy=args.scaleY)

    start = time.time()

    # Get all bounding boxes
    face_detection_start = time.time()
    bb = align.getAllFaceBoundingBoxes(rgb_image)
    print("Face detection took {}".format(time.time() - face_detection_start))

    if bb is None:
        return None
    if args.verbose:
        print("Face detection took {} seconds".format(time.time() - start))

    start = time.time()

    # Get detected faces aligned
    alignedFaces = []

    #!!! TRY HERE WITHOUT ALIGNING THE FACE FIRST

    for box in bb:
        alignedFaces.append(
            rgb_image[box.left() : box.right(), box.top() : box.bottom()].copy()
        )

    if alignedFaces is None:
        raise Exception("Unable to align the frame")
    if args.verbose:
        print("Alignment took {} seconds".format(time.time() - start))

    start = time.time()
    # Validate each detected face

    facesWithValidation = []

    for i, alignedFace in enumerate(alignedFaces):
        face_validation_start = time.time()
        face_validity = faceSpoofValidator.validate_face(alignedFace)
        print("Face validation took {}".format(time.time() - face_validation_start))
        if face_validity:
            facesWithValidation.append((alignedFace, bb[i], 1))
        else:
            facesWithValidation.append((alignedFace, bb[i], 0))

    return facesWithValidation


def main():
    parser = initializeParser()
    args = parser.parse_args()

    video_capture = cv2.VideoCapture(
        "/home/doru/Desktop/Licenta/Implementation/databases/cbsr_antispoofing"
        "/test_release/13/3.avi"
    )

    # video_capture = cv2.VideoCapture(0)
    video_capture.set(3, args.width)
    video_capture.set(4, args.height)

    frameNr = 0

    align = openface.AlignDlib(args.dlibFacePredictor)
    faceSpoofValidator = faceSpoofValidation.FaceSpoofValidator(
        features.MultiScaleLocalBinaryPatterns((8, 1), (8, 2), (16, 2)),
        "classifiers/classifier_tested_on1.pkl",
    )
    while True:
        ret, frame = video_capture.read()

        # cv2.imshow('cameraFeed', frame)
        print("Processing frame number {}".format(frameNr))
        print("With size {}".format(frame.shape))
        frameNr += 1

        if ret == False:
            print("No more input from video data source")
            break

        start = time.time()

        # Get the faces in the frame that are not spoof
        facesWithValidation = processFrame(frame, align, faceSpoofValidator, args)

        # Process here faces having their validation
        for faceWithValidation in facesWithValidation:
            bb = faceWithValidation[1]

            ll = (
                int(round(bb.left() / args.scaleX)),
                int(round(bb.bottom() / args.scaleY)),
            )
            ur = (
                int(round(bb.right() / args.scaleX)),
                int(round(bb.top() / args.scaleY)),
            )

            if faceWithValidation[2] == 1:
                cv2.rectangle(frame, ll, ur, color=(0, 255, 0), thickness=3)
            else:
                cv2.rectangle(frame, ll, ur, color=(0, 0, 255), thickness=3)
        cv2.imshow("face", frame)
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break
        print("Entire processing of a frame took {}".format(time.time() - start))

    video_capture.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
