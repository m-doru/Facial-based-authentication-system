from __future__ import print_function
import time

import cv2
import features
import openface

from utilityScripts import get_frame_from_video
import faceSpoofValidation

mlbp = features.MultiScaleLocalBinaryPatterns((8, 1), (8, 2),(16, 2))

faceSpoofValidator = faceSpoofValidation.FaceSpoofValidator(mlbp,'classifiers/casia.pkllinear')

faceFrames = get_frame_from_video.get_frames('/home/doru/Desktop/Licenta/Implementation/databases/'
                                          'cbsr_antispoofing/test_release/1/3.avi', 1000)



align = openface.AlignDlib("/home/doru/Desktop/Licenta/Implementation/models/dlib/shape_predictor_68_face_landmarks"
                           ".dat")


for frame in faceFrames:
    start = time.time()
    # Get all bounding boxes
    bbs = align.getAllFaceBoundingBoxes(frame)

    if bbs is None or len(bbs) == 0:
        raise Exception("No faces detected")


    alignedFaces = []

    for box in bbs:
        alignedFaces.append(align.align(
            260,
            frame,
            box,
            landmarkIndices=openface.AlignDlib.OUTER_EYES_AND_NOSE))

    if alignedFaces is None:
        continue

    red_channel = alignedFaces[0][:, :, 0]
    for bb in bbs:
        ll = (int(bb.left()), bb.bottom())
        ur = (int(bb.right()), bb.top())

        faceValidationStart = time.time()

        valid_face = faceSpoofValidator.validate_face(alignedFaces[0])

        print('Faces validation took {}'.format(time.time() - faceValidationStart))

        if valid_face:
            cv2.rectangle(frame, ll, ur, color=(0, 255, 0),thickness=3)
        else:
            cv2.rectangle(frame, ll, ur, color=(0, 0, 255), thickness=3)

    cv2.imshow('face', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
