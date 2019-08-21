import cv2
import argparse
import os

parser = argparse.ArgumentParser()

parser.add_argument("--saveDir", type=str, default="../knownfaces")

args = parser.parse_args()


def saveImage(img):
    fileName = raw_input("Filename:")
    fileName += ".jpg"

    fileDir = os.path.dirname(os.path.realpath(__file__))

    savePath = os.path.join(fileDir, args.saveDir, fileName)

    cv2.imwrite(savePath, img)


def main():
    cameraFeed = cv2.VideoCapture(0)

    ret = True

    while ret:
        ret, frame = cameraFeed.read()
        cv2.imshow("webcamfeed", frame)

        pressedKey = cv2.waitKey(1)

        if pressedKey & 0xFF == ord("s"):
            saveImage(frame)
        if pressedKey & 0xFF == ord("q"):
            break

    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
