import cv2

def flip(path, path_out):
    cap = cv2.VideoCapture(path)

    # Define the codec and create VideoWriter object
    fourcc = cv2.VideoWriter_fourcc(*'MP4V')
    out = cv2.VideoWriter('/home/doru/Desktop/video.mp4', fourcc, 20.0, (720, 480))

    while (cap.isOpened()):
        ret, frame = cap.read()
        if ret == True:
            frame = cv2.flip(frame, 0)

            # write the flipped frame
            out.write(frame)

            cv2.imshow('frame', frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        else:
            break

    # Release everything if job is finished
    cap.release()
    out.release()
    cv2.destroyAllWindows()

def main():
    begin = '/home/doru/Desktop/Licenta/Implementation/databases/MSU_MFSD/MSU-MFSD/scene01/real/real_client0'
    end = '_android_SD_scene01.mp4'
    for i in [3,5,6,7,8,9]:
        path = begin + '0' + str(i) + end
        flip(path, begin+'9'+str(i)+end)

if __name__ == '__main__':
    main()
