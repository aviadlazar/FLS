import cv2
import os
import time


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


def generate_frames(video_dir, save_dir):
    for file_path in os.listdir(video_dir):
        s = time.time()
        name = os.path.splitext(file_path)[0]
        vid = VideoHandler(os.path.join(video_dir, file_path), name=name)
        save_path = os.path.join(save_dir, name)
        os.mkdir(save_path)
        vid.sample_from_vid(save_dir=save_path)
        e = time.time()
        print("completed video:", name, "in", e - s, "seconds")


def generate_YOLO_labels(data_dir, labels_dir, save_path):
    new_lines = []
    for file_path in os.listdir(labels_dir):
        with open(os.path.join(labels_dir, file_path), 'r') as label_f:
            img_path = os.path.join(data_dir, os.path.splitext(file_path)[0]+".jpg")
            annotations = [img_path]
            for line in label_f:
                class_label = line.split()[0]
                coordinates = line.split()[1:]
                object_annot = ','.join(coordinates) + ',' + class_label
                annotations.append(object_annot)
            new_lines.append(' '.join(annotations) + '\n')
    with open(save_path, 'w') as out_file:
        out_file.writelines(new_lines)


if __name__ == '__main__':
    data_dir = '/data/home/liranhal/code/data/data_APAS/cross_valid/images'
    labels_dir = '/data/home/liranhal/code/data/data_APAS/cross_valid/labels_main_head'
    save_path = '/data/home/liranhal/code/data/ASAP_main_annotations.txt'
    generate_YOLO_labels(data_dir, labels_dir, save_path)