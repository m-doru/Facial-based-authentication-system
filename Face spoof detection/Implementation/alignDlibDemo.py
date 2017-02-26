import cv2
import openface
import os
import time

fileDir = os.path.dirname(os.path.realpath(__file__))
modelDir = os.path.join(fileDir, 'models')
dlibModelDir = os.path.join(modelDir, 'dlib')
openfaceModelDir = os.path.join(modelDir, 'openface')

align = openface.AlignDlib(os.path.join(dlibModelDir, "shape_predictor_68_face_landmarks.dat"))

cameraFeed = cv2.VideoCapture(0)

while True:
    startFrameProcess = time.time()
    ret, origFrame = cameraFeed.read()

    if ret == False:
        break
    start = time.time()

    scale = 0.5

    frame = cv2.resize(origFrame,(0,0), fx=scale, fy = scale)
    bbs = align.getAllFaceBoundingBoxes(frame)

    print('Detecting faces took {}'.format(time.time() - start))
    if bbs is None:
        continue


    alignedFaces = []
    for bb in bbs:
        alignedFaces.append(align.align(
            96,
            frame,
            bb,
            landmarkIndices=openface.AlignDlib.OUTER_EYES_AND_NOSE
        ))


    for i,bb in enumerate(bbs):
        ll = (int(round(bb.left()/scale)),int(round(bb.bottom()/scale)))
        ur = (int(round(bb.right()/scale)), int(round(bb.top()/scale)))
        cv2.rectangle(origFrame, ll, ur, color=(0, 255, 0),thickness=3)
        cv2.imshow('face'+str(i), alignedFaces[i])

    cv2.imshow('', origFrame)

    print('Processing a frame took {}'.format(time.time() - start))
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
