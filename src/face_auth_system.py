import sys
import os
from faceSpoofDetection import faceSpoofValidation
from faceSpoofDetection import features

fileDir = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.join(fileDir, '..'))

import cv2
import argparse
import time
import openface
import numpy as np
from os import walk

modelDir = os.path.join(fileDir, 'models')
dlibModelDir = os.path.join(modelDir, 'dlib')
openfaceModelDir = os.path.join(modelDir, 'openface')


def initialize_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument('--verbose', action='store_true', default=False)
    parser.add_argument(
        '--captureDevice',
        type=int,
        default=0,
        help='Capture device. 0 for latop webcam and 1 for usb webcam')
    parser.add_argument('--width', type=int, default=640)
    parser.add_argument('--height', type=int, default=480)

    parser.add_argument('--imgDim', type=int,
                        help="Default image dimension.", default=96)

    parser.add_argument('--scaleX', type=float, help="Scale to resize the feed image for faster processing",
                        default=1)
    parser.add_argument('--scaleY', type=float, help="Scale to resize the feed image for faster processing",
                        default=1)
    parser.add_argument('--dlibFacePredictor', type=str, help="Path to dlib's face predictor.",
                        default=os.path.join(dlibModelDir, "shape_predictor_68_face_landmarks.dat"))
    parser.add_argument('--networkModel', type=str, help="Path to Torch network model.",
                        default=os.path.join(openfaceModelDir, 'nn4.small2.v1.t7'))
    parser.add_argument('--scale', type=float, default=0.5, help='The scale with which the webcam frames will be '
                                                               'resized')
    parser.add_argument('--webcam', type=int, default=0, help='Specify which camera to be used for input(0 = webcam, '
                                                              '1 = usb')
    parser.add_argument('--knownFacesDir', type=str, default='knownfaces')
    parser.add_argument('--threshold', type=float, default=0.8)
    parser.add_argument('--newKnownReps', action='store_true')

    return parser

parser = initialize_parser()
args = parser.parse_args()

start = time.time()
align = openface.AlignDlib(args.dlibFacePredictor)
net = openface.TorchNeuralNet(args.networkModel, args.imgDim)
if args.verbose:
    print("Loading the dlib and OpenFace models took {} seconds.".format(
        time.time() - start))

def getRep(imgPath, args):
    if args.verbose:
        print("Processing {}.".format(imgPath))
    bgrImg = cv2.imread(imgPath)
    if bgrImg is None:
        raise Exception("Unable to load image: {}".format(imgPath))
    rgbImg = cv2.cvtColor(bgrImg, cv2.COLOR_BGR2RGB)

    if args.verbose:
        print("  + Original size: {}".format(rgbImg.shape))

    start = time.time()
    bb = align.getLargestFaceBoundingBox(rgbImg)
    if bb is None:
        raise Exception("Unable to find a face: {}".format(imgPath))
    if args.verbose:
        print("  + Face detection took {} seconds.".format(time.time() - start))

    start = time.time()
    alignedFace = align.align(args.imgDim, rgbImg, bb,
                              landmarkIndices=openface.AlignDlib.OUTER_EYES_AND_NOSE)
    if alignedFace is None:
        raise Exception("Unable to align image: {}".format(imgPath))
    if args.verbose:
        print("  + Face alignment took {} seconds.".format(time.time() - start))

    start = time.time()
    rep = net.forward(alignedFace)
    if args.verbose:
        print("  + OpenFace forward pass took {} seconds.".format(time.time() - start))
        print("Representation:")
        print(rep)
        print("-----\n")
    return rep

def getNames(fullFileName):
    filename = fullFileName.split('.')[0]

    names = filename.split('-')

    return names

def computeKnownFacesRepresentation(path):
    knownFacesRep = []

    facesFiles = []
    dirpath = []
    for(root, _, filenames) in walk(path):
        facesFiles.extend(filenames)
        dirpath = root
        break

    knownFaces = []

    for i,facesFile in enumerate(facesFiles):
        image = cv2.imread(os.path.join(dirpath, facesFile))

        image = cv2.resize(image, (0,0), fx=0.5, fy=0.5)

        bbs = align.getAllFaceBoundingBoxes(image)

        if bbs is None:
            continue


        alignedFaces = []
        for bb in bbs:
            alignedFaces.append(align.align(
                args.imgDim,
                image,
                bb,
                landmarkIndices=openface.AlignDlib.OUTER_EYES_AND_NOSE
            ))

        names = getNames(facesFile)

        for i,face in enumerate(alignedFaces):
            if i < len(names):
                knownFaces.append((face, names[i]))
            else:
                knownFaces.append((face, 'noname'))

    for (face, name) in knownFaces:
        faceRep = net.forward(face)

        knownFacesRep.append((faceRep, name))


    return knownFacesRep


def loadKnownFaces(path):
    startTimeLoadingKnownFaces = time.time()
    path = os.path.join(fileDir, path)

    picklePath = os.path.join(path, 'reps.pk')
    '''
    if os.path.isfile(picklePath) and not args.newKnownReps:
        with open(picklePath, 'r') as inputF:
            knownRepresentations = np.load(inputF)
    else:
    '''
    knownRepresentations = computeKnownFacesRepresentation(path)
    #np.save(picklePath, knownRepresentations)

    if args.verbose:
        print('Loading known faces representations took {}'.format(time.time() - startTimeLoadingKnownFaces))

    return knownRepresentations


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

    #Get detected faces aligned
    aligned_faces = []

    for box in bb:
        aligned_faces.append(rgb_image[box.left():box.right(), box.top():box.bottom()].copy())

    if aligned_faces is None:
        raise Exception("Unable to align the frame")
    if args.verbose:
        print("Alignment took {} seconds".format(time.time() - start))

    start = time.time()
    # Validate each detected face

    facesWithValidation= []

    for i, alignedFace in enumerate(aligned_faces):
        face_validation_start = time.time()
        face_validity = faceSpoofValidator.validate_face(alignedFace)
        print("Face validation took {}".format(time.time() - face_validation_start))
        if face_validity:
            facesWithValidation.append((alignedFace, bb[i], 1))
        else:
            facesWithValidation.append((alignedFace, bb[i], 0))

    return facesWithValidation

def identify_face(face, knwon_faces_rep, orig_frame, ll, ur):
    face_rep_start = time.time()
    face_rep = net.forward(face)
    print("Passing through the network takes {}".format(time.time() - face_rep_start))

    recognized = False

    for known_face_rep, name in knwon_faces_rep:
        diff = known_face_rep - face_rep
        d = np.dot(diff, diff)
        if d < args.threshold:
            cv2.rectangle(orig_frame, ll, ur, color=(0, 255, 0), thickness=3)
            cv2.putText(orig_frame, name, ll, cv2.FONT_HERSHEY_PLAIN, 2, color=(255, 0, 0), thickness=2)
            recognized = True
            break

    if recognized == False:
        cv2.rectangle(orig_frame, ll, ur, color=(255, 0, 0), thickness=3)

def main():
    #cameraFeed = cv2.VideoCapture(0)
    cameraFeed = cv2.VideoCapture(args.captureDevice)

    known_faces_rep = loadKnownFaces(args.knownFacesDir)

    face_spoof_validator = faceSpoofValidation.FaceSpoofValidator(
        features.MultiScaleLocalBinaryPatterns((8,1), (8,2), (16,2)),
        'faceSpoofDetection/classifiers/powerful_classifier.pkl')

    while True:
        start_frame_processing = time.time()

        ret, orig_frame = cameraFeed.read()

        print("Dimmension of the frame is {}".format(orig_frame.shape))
        if ret == False:
            break
        start = time.time()

        frame = cv2.resize(orig_frame,(0,0), fx=args.scale, fy = args.scale)

        bbs = align.getAllFaceBoundingBoxes(frame)

        if args.verbose:
            print('Detecting faces took {}'.format(time.time() - start))
        if bbs is None:
            continue

        start = time.time()

        aligned_faces = []
        for bb in bbs:
            aligned_faces.append(align.align(
                args.imgDim,
                frame,
                bb,
                landmarkIndices=openface.AlignDlib.OUTER_EYES_AND_NOSE
            ))

        if args.verbose:
            print('Aligning faces took {}'.format(time.time() - start))

        start = time.time()

        for i,bb in enumerate(bbs):
            # move these 3 lines after you find the corresponding face
            ll = (int(round(bb.left()/args.scale)),int(round(bb.bottom()/args.scale)))
            ur = (int(round(bb.right()/args.scale)), int(round(bb.top()/args.scale)))


            face = aligned_faces[i]

            if not face_spoof_validator.validate_face(face):
                identify_face(face, known_faces_rep, orig_frame, ll, ur)
            else:
                cv2.rectangle(orig_frame, ll, ur, color=(0, 0, 255), thickness=3)

        if args.verbose:
            print('Identifying faces took {}'.format(time.time() - start))

        cv2.imshow('id', orig_frame)

        if args.verbose:
            print('Processing a frame took {}'.format(time.time() - start_frame_processing))

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

if __name__ == '__main__':
    main()
