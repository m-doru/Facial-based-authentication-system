import sys
import os
fileDir = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.join(fileDir, '..'))

import cv2
import argparse
import time
import openface
import numpy as np
from os import walk

modelDir = os.path.join(fileDir,'..', 'models')
dlibModelDir = os.path.join(modelDir, 'dlib')
openfaceModelDir = os.path.join(modelDir, 'openface')

start = time.time()
parser = argparse.ArgumentParser()

parser.add_argument('--dlibFacePredictor', type=str, help="Path to dlib's face predictor.",
                    default=os.path.join(dlibModelDir, "shape_predictor_68_face_landmarks.dat"))
parser.add_argument('--networkModel', type=str, help="Path to Torch network model.",
                    default=os.path.join(openfaceModelDir, 'nn4.small2.v1.t7'))
parser.add_argument('--imgDim', type=int,
                    help="Default image dimension.", default=96)
parser.add_argument('--verbose', action='store_true')
parser.add_argument('--scale', type=float, default=0.5, help='The scale with which the webcam frames will be '
                                                             'resized')
parser.add_argument('--webcam', type=int, default=0, help='Specify which camera to be used for input(0 = webcam, '
                                                          '1 = usb')
parser.add_argument('--knownFacesDir', type=str, default='../knownfaces')
parser.add_argument('--threshold', type=float, default=1.1)
args = parser.parse_args()

if args.verbose:
    print("Argument parsing and loading libraries took {} seconds.".format(
        time.time() - start))

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


def loadKnownFaces(path):
    startTimeLoadingKnownFaces = time.time()
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

    if args.verbose:
        print('Loading known faces representations took {}'.format(time.time() - startTimeLoadingKnownFaces))


    return knownFacesRep



def main():
    cameraFeed = cv2.VideoCapture(args.webcam)

    knownFacesRep = loadKnownFaces(args.knownFacesDir)

    while True:
        startFrameProcessing = time.time()

        ret, origFrame = cameraFeed.read()

        if ret == False:
            break
        start = time.time()

        frame = cv2.resize(origFrame,(0,0), fx=args.scale, fy = args.scale)

        bbs = align.getAllFaceBoundingBoxes(frame)

        if args.verbose:
            print('Detecting faces took {}'.format(time.time() - start))
        if bbs is None:
            continue

        start = time.time()

        alignedFaces = []
        for bb in bbs:
            alignedFaces.append(align.align(
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


            face = alignedFaces[i]

            faceRep = net.forward(face)

            recognized = False

            for knownFaceRep, name in knownFacesRep:
                diff = knownFaceRep - faceRep
                d = np.dot(diff, diff)
                if d < args.threshold:
                    cv2.rectangle(origFrame, ll, ur, color=(0,255,0),thickness=3)
                    cv2.putText(origFrame, name, ll, cv2.FONT_HERSHEY_PLAIN, 2, color=(255,0,0), thickness=3)
                    recognized = True
                    break

            if recognized == False:
                cv2.rectangle(origFrame, ll, ur, color=(0, 255, 0), thickness=3)

        if args.verbose:
            print('Identifying faces took {}'.format(time.time() - start))

        cv2.imshow('', origFrame)

        if args.verbose:
            print('Processing a frame took {}'.format(time.time() - startFrameProcessing))

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

if __name__ == '__main__':
    main()