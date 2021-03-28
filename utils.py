import cv2
import os


class VideoHandler:
    def __init__(self, path, name=""):
        self.path = path
        self.name = name

    def play_video(self):
        capture = cv2.VideoCapture(self.path)
        capture.set(cv2.CAP_PROP_POS_FRAMES, 0)
        ret = True
        while ret:
            ret, frame = capture.read()
            if ret:
                cv2.imshow(self.name, frame)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        capture.release()
        cv2.destroyAllWindows()

    def sample_from_vid(self, save_dir=None, step=-1):
        capture = cv2.VideoCapture(self.path)
        capture.set(cv2.CAP_PROP_POS_FRAMES, 0)
        frame_count = 0
        frame_id = 1
        if step <= 0:
            step = round(capture.get(cv2.CAP_PROP_FPS))

        if save_dir:
            save_path = os.path.join(save_dir, self.name)
        else:
            save_path = self.name

        ret = True
        while ret:
            ret, frame = capture.read()
            if ret:
                if frame_count % step == 0:
                    cv2.imwrite(save_path + "_" + str(frame_id) + ".jpg", frame)
                    frame_id += 1
                frame_count += 1

        capture.release()
