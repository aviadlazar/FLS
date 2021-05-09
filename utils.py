
import cv2
import os
import time
import random
import sklearn.model_selection
import argparse

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


def YOLO_train_test_split(label_path, save_train, save_test, split):
    with open(label_path, 'r') as label_f:
        full_data = label_f.readlines()
        train = random.sample(full_data, round(split*len(full_data)))
        test = [t for t in full_data if t not in train]
        with open(save_train, 'w') as train_out:
            train_out.writelines(train)
        with open(save_test, 'w') as test_out:
            test_out.writelines(test)


def switch_yolo_to_coco(tab_line, image_size):
    tab_line = tab_line.split(",")
    id_ = tab_line[4]
    x_center = float(tab_line[0])
    y_center = float(tab_line[1])
    width = float(tab_line[2])
    height = float(tab_line[3])

    x1 = str(round((x_center - width / 2) * image_size))
    y1 = str(round((y_center - height / 2) * image_size))
    x2 = str(round((x_center + width / 2) * image_size))
    y2 = str(round((y_center + height / 2) * image_size))

    return x1 + "," + y1 + "," + x2 + "," + y2 + "," + id_


def switch_coordinates_size(line, old_size, new_size):
    line = line.split(",")
    id_ = line[4]
    x1 = str(round(new_size*float(line[0])/old_size))
    x2 = str(round(new_size*float(line[1])/old_size))
    x3 = str(round(new_size*float(line[2])/old_size))
    x4 = str(round(new_size*float(line[3])/old_size))

    return x1 + "," + x2 + "," + x3 + "," + x4 + "," + id_

def main():
    coords = []
    with open(FILE + "_old.txt", "r") as f:
        for line in f:
            tab_line = line.split(" ")
            coord = []
            for i, txt in enumerate(tab_line):
                if i == 0:
                    coord.append(txt)
                else:
                    coord.append(switch_coordinates_size(txt, 608, 416))
            coords.append(' '.join(coord))

    with open(FILE + ".txt", "w") as final_file:
        final_file.writelines(coords[:-1])


if __name__ == '__main__':
    FILE = '/data/home/liranhal/code/data/ASAP_main_annotations_train'
    main()
#     label_path = '/data/home/liranhal/code/data/ASAP_main_annotations.txt'
#     save_path_train = '/data/home/liranhal/code/data/ASAP_main_annotations_train.txt'
#     save_path_test = '/data/home/liranhal/code/data/ASAP_main_annotations_test.txt'
#     YOLO_train_test_split(label_path, save_path_train, save_path_test, 0.7)