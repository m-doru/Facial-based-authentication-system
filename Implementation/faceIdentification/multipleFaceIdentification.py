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
parser.add_argument('--scale', type=float, default=1, help='The scale with which the webcam frames will be '
                                                             'resized')
parser.add_argument('--webcam', type=int, default=0, help='Specify which camera to be used for input(0 = webcam, '
                                                          '1 = usb')
parser.add_argument('--knownFacesDir', type=str, default='../knownfaces')
parser.add_argument('--threshold', type=float, default=0.8)
parser.add_argument('--newKnownReps', action='store_true')

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

def main():
    #cameraFeed = cv2.VideoCapture(0)
    cameraFeed = cv2.VideoCapture('/home/doru/Desktop/Licenta/Implementation/databases/cbsr_antispoofing/test_release'
                                  '/13/1.avi')

    knownFacesRep = loadKnownFaces(args.knownFacesDir)

    while True:
        startFrameProcessing = time.time()

        ret, origFrame = cameraFeed.read()

        print("Dimmension of the frame is {}".format(origFrame.shape))
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

            face_rep_start = time.time()
            faceRep = net.forward(face)
            print("Passing through the network takes {}".format(time.time() - face_rep_start))

            recognized = False

            min_dist_name = (5, "")

            for knownFaceRep, name in knownFacesRep:
                diff = knownFaceRep - faceRep
                d = np.dot(diff, diff)
                if d < min_dist_name[0]:
                    min_dist_name = (d, name)

            if min_dist_name[0] < args.threshold:
                cv2.rectangle(origFrame, ll, ur, color=(0,255,0),thickness=3)
                cv2.putText(origFrame, min_dist_name[1], ll, cv2.FONT_HERSHEY_PLAIN, 2, color=(255,0,0), thickness=2)
                recognized = True
                break

            if recognized == False:
                cv2.rectangle(origFrame, ll, ur, color=(0, 0, 255), thickness=3)

        if args.verbose:
            print('Identifying faces took {}'.format(time.time() - start))

        cv2.imshow('id', origFrame)

        if args.verbose:
            print('Processing a frame took {}'.format(time.time() - startFrameProcessing))

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

if __name__ == '__main__':
    main()
