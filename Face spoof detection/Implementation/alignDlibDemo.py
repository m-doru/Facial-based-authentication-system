import cv2
import openface
import os
import time
import features

fileDir = os.path.dirname(os.path.realpath(__file__))
modelDir = os.path.join(fileDir, 'models')
dlibModelDir = os.path.join(modelDir, 'dlib')
openfaceModelDir = os.path.join(modelDir, 'openface')

align = openface.AlignDlib(os.path.join(dlibModelDir, "shape_predictor_68_face_landmarks.dat"))

cameraFeed = cv2.VideoCapture(0)

mlbp = features.MultiScaleLocalBinaryPatterns((8,1), (24,3), (40, 5))
scale = 0.5
dsift = features.DSIFT()

while True:
    startFrameProcess = time.time()
    ret, origFrame = cameraFeed.read()

    if ret == False:
        break
    start = time.time()



    frame = cv2.resize(origFrame,(0,0), fx=scale, fy = scale)

    bbs = align.getAllFaceBoundingBoxes(frame)

    print('Detecting faces took {}'.format(time.time() - start))
    if bbs is None:
        continue


    alignedFaces = []
    for bb in bbs:
        alignedFaces.append(align.align(
            144,
            frame,
            bb,
            landmarkIndices=openface.AlignDlib.OUTER_EYES_AND_NOSE
        ))

    lbpFeatures = []
    siftFeatures = []
    for i,bb in enumerate(bbs):
        ll = (int(round(bb.left()/scale)),int(round(bb.bottom()/scale)))
        ur = (int(round(bb.right()/scale)), int(round(bb.top()/scale)))
        cv2.rectangle(origFrame, ll, ur, color=(0, 255, 0),thickness=3)

        cv2.imshow('face'+str(i), alignedFaces[i])

        #face = origFrame[ur[1]:ll[1]+1, ll[0]:ur[0]+1, :]
        face = alignedFaces[i]

        redFace = alignedFaces[i][:,:,0]
        #redFace = face[:,:,0]

        startSift = time.time()

        step = 8
        size = 16

        kp, desc = dsift.compute(redFace, step, size)
        print('sift took {}'.format(time.time() - startSift))
        siftFeatures.append(desc)

        if siftFeatures[0] is not None:
            print('sift feature length ', len(desc[0]))

        img = cv2.drawKeypoints(face, kp, cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)
        cv2.imshow('kp', img)

        startMLBP = time.time()
        lbpFeatures.append(mlbp.computeFeaturePatchWise(redFace))
        print('mlbp took{}'.format(time.time() - startMLBP))

        print('lbp features length ', len(lbpFeatures[0]))

        #img = cv2.drawKeypoints(alignedFaces[])


    cv2.imshow('', origFrame)

    print('Processing a frame took {}'.format(time.time() - start))

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
