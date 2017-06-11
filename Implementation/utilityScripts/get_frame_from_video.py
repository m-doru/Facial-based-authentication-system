import cv2

def get_frames(video_path, number_of_frames = 1):
    video_feed = cv2.VideoCapture(video_path)

    frames = []

    ret = True
    for i in range(number_of_frames):
        ret, frame = video_feed.read()

        if ret:
            frames.append(frame)

    video_feed.release()
    return frames

def save_frames(video_path, save_path, number_of_frames = 1):
    video_feed = cv2.VideoCapture(video_path)

    frames = get_frames(video_path, number_of_frames)

    for i in range(len(frames)):
        frame = frames[i]
        cv2.imwrite(save_path + "img" + str(i) + ".jpg", frame)