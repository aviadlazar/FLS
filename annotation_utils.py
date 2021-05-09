import os


def generate_yolov4_label_file(data_dir, labels_dir, save_path):
    """
    This function takes YOLOv3 format and creates a label file that fits YOLOv4 pytorch implementation fromat.
    :param data_dir: Path to the directory at which the images are stored
    :param labels_dir: Path to the directory at which label text files are stored
    :param save_path: Path to save the new file
    :return:
    """
    new_lines = []
    for file_path in os.listdir(labels_dir):  # iterate over label files
        with open(os.path.join(labels_dir, file_path), 'r') as label_f:
            # full path to the image
            img_path = os.path.join(data_dir, os.path.splitext(file_path)[0]+".jpg")
            annotations = [img_path]
            # generate the annotation line
            for line in label_f:
                class_label = line.split()[0]
                coordinates = line.split()[1:]
                object_annot = ','.join(coordinates) + ',' + class_label
                annotations.append(object_annot)
            new_lines.append(' '.join(annotations) + '\n') # add to the list of all annotation lines
    # finally, write everything to the new file
    with open(save_path, 'w') as out_file:
        out_file.writelines(new_lines)


def switch_bbox_yolo_to_coco_fromat(tab_line, image_size):
    """
    This function takes a label in YOLO bbox format and turns it to COCO bbox format
    :param tab_line: an annotation line
    :param image_size: the size of the image you want to train on
    :return: a new annotation in COCO format
    """
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


def switch_file_yolo_to_coco(original_file, image_size, save_path):
    """
    This function receives a file where the bbox format is YOLO and changes them to COCO for a given image size.
    :param original_file: the file to read the current annotations from
    :param image_size: the size you want ot train your images on
    :param save_path: path to save the new annotation file
    """
    coords = []
    with open(original_file, "r") as f:
        for line in f:
            tab_line = line.split(" ")
            coord = []
            for i, txt in enumerate(tab_line):
                if i == 0:
                    coord.append(txt)
                else:
                    coord.append(switch_bbox_yolo_to_coco_fromat(txt, image_size))
            coords.append(' '.join(coord))

    with open(save_path, "w") as final_file:
        final_file.writelines(coords[:-1])


def switch_bbox_coordinates_size(line, old_size, new_size):
    """
    This function takes a label in COCO bbox format and fits it to a different image size
    :param line:  an annotation line
    :param old_size: the size of image the bbox is currently set for
    :param new_size: the new size of image the bbox should be converted to
    :return: the upstaed annotation line
    """
    line = line.split(",")
    id_ = line[4]
    x1 = str(round(new_size*float(line[0])/old_size))
    x2 = str(round(new_size*float(line[1])/old_size))
    x3 = str(round(new_size*float(line[2])/old_size))
    x4 = str(round(new_size*float(line[3])/old_size))

    return x1 + "," + x2 + "," + x3 + "," + x4 + "," + id_


def switch_file_coordintes_size(original_file, old_size, new_size, save_path):
    """
       This function receives a file where the bbox format is COCO for a given image size and changes them to COCO for
       a new image size.
       :param original_file: the file to read the current annotations from.
       :param old_size: the size ythe annotation file is currently set for.
       :param new_size: the size you want ot train your images on.
       :param save_path: path to save the new annotation file.
       """
    coords = []
    with open(original_file, "r") as f:
        for line in f:
            tab_line = line.split(" ")
            coord = []
            for i, txt in enumerate(tab_line):
                if i == 0:
                    coord.append(txt)
                else:
                    coord.append(switch_bbox_coordinates_size(txt, old_size, new_size))
            coords.append(' '.join(coord))

    with open(save_path, "w") as final_file:
        final_file.writelines(coords[:-1])