from __future__ import print_function

import cv2
import matplotlib.pyplot as plt

import features
import openface

from utilityScripts import get_frame_from_video
import faceSpoofValidation

P = 8
R = 1

#mlbp = features.MultiScaleLocalBinaryPatterns((8, 1), (24, 3),(40, 5))
mlbp = features.LocalBinaryPatterns(P, R, method='default')

#faceImg = cv2.imread('../data/face2.jpg', cv2.IMREAD_COLOR)
#spoofFaceImg = cv2.imread('../data/spoofFace2.jpg', cv2.IMREAD_COLOR)
medium = 'Tablet_RearCamera'
faceImg = get_frame_from_video.get_frames('/home/doru/Desktop/Licenta/Implementation/databases'
                                          '/MSU_USSA/MSU_USSA_Public/LiveSubjectsImages/109.jpg')[0]
spoofFaceImg = get_frame_from_video.get_frames('/home/doru/Desktop/Licenta/Implementation/databases' +
                                          '/MSU_USSA/MSU_USSA_Public/SpoofSubjectImages/'+ medium +'/109.jpg')[0]

#faceImg = cv2.cvtColor(faceImg, cv2.COLOR_BGR2RGB)
#spoofFaceImg = cv2.cvtColor(spoofFaceImg, cv2.COLOR_BGR2RGB)

'''
start = time.time()

faceLBPHist = mlbp.computeFeature(cv2.cvtColor(faceImg, cv2.COLOR_RGB2GRAY))

print('Computing the lbp feature of the real face took {}'.format(time.time()-start))

start = time.time()
fastFaceLBPHist = mlbp.computeFeatureFaster(cv2.cvtColor(spoofFaceImg, cv2.COLOR_RGB2GRAY))
print('Computing the lbp feature in the fast way took {}'.format(time.time() - start))

fastFaceLBPHist = map(lambda x:-x, fastFaceLBPHist)
diff = np.add(faceLBPHist, fastFaceLBPHist)
diff = np.absolute(diff)
Visual representation of the components of the application
print(sum(diff))
'''


align = openface.AlignDlib("/home/doru/Desktop/Licenta/Implementation/models/dlib/shape_predictor_68_face_landmarks"
                           ".dat")

# Get all bounding boxes
bb = align.getAllFaceBoundingBoxes(faceImg)
bbs = align.getAllFaceBoundingBoxes(spoofFaceImg)

if bb is None or bbs is None or len(bb) == 0 or len(bbs) == 0:
    raise Exception("No faces detected")


alignedFaces = []

for box in bb:
    alignedFaces.append(align.align(
            260,
            faceImg,
            box,
            landmarkIndices=openface.AlignDlib.OUTER_EYES_AND_NOSE))

if alignedFaces is None:
        raise Exception("Unable to align the frame")

alignedSpoofFaces = []
for box in bbs:
    alignedSpoofFaces.append(align.align(
        260,
        spoofFaceImg,
        box,
        landmarkIndices=openface.AlignDlib.OUTER_EYES_AND_NOSE
    ))

if alignedSpoofFaces is None:
        raise Exception("Unable to align the frame")


realImgRedChannel = alignedFaces[0][:, :, 0]
spoofImgRedChannel = alignedSpoofFaces[0][:, :, 0]

realImgRedChannel = cv2.cvtColor(alignedFaces[0], cv2.COLOR_RGB2GRAY)
spoofImgRedChannel = cv2.cvtColor(alignedSpoofFaces[0], cv2.COLOR_RGB2GRAY)

if isinstance(mlbp, features.LocalBinaryPatterns):
    hist, bins, lbpFV = mlbp.compute(realImgRedChannel)
    bins = bins.astype('float')
    bins = bins + (bins[1] - bins[0])/2

    histSpoof, binsSpoof, lbpFVSpoof = mlbp.compute(spoofImgRedChannel)
    binsSpoof = binsSpoof.astype('float')
    binsSpoof = binsSpoof + (binsSpoof[1] - binsSpoof[0])/2

    f, ((ax1, ax2), (ax3, ax4), (ax5, ax6)) = plt.subplots(nrows=3, ncols=2, figsize=(9,6))

    ax1.imshow(alignedFaces[0])
    ax3.bar(bins[:-1], hist)
    ax5.hist(lbpFV.ravel(), normed=True)


    ax2.imshow(alignedSpoofFaces[0])
    ax4.bar(binsSpoof[:-1], histSpoof)
    ax6.hist(lbpFVSpoof.ravel(), normed=True)



    print(lbpFV.shape)

    plt.show()

    cv2.imwrite('/home/doru/Desktop/real.png', lbpFV)
    cv2.imwrite('/home/doru/Desktop/'+medium+'.png', lbpFVSpoof)

    cv2.imshow('face', alignedFaces[0])

    lbpFV = lbpFV.astype('uint8')
    cv2.imshow('lbp', lbpFV)

    cv2.imshow('spoofface', alignedSpoofFaces[0])
    lbpFVSpoof = lbpFVSpoof.astype('uint8')
    cv2.imshow('lbpspoof', lbpFVSpoof)
    while(1):
        if cv2.waitKey(0) & 0xFF == ord('q'):
            break

    cv2.destroyAllWindows()
else:
    hist = mlbp.compute(realImgRedChannel)
    histSpoof = mlbp.compute(spoofImgRedChannel)

    print(len(hist))
    print(len(histSpoof))


