import os
import json


def main():
    # for f_name in os.listdir('/data/home/liranhal/code/data/train/images'):
    #     print(f_name, 'intra2_' + f_name)
    #     os.rename(f'/data/home/liranhal/code/data/train/images/{f_name}',
    #               f'/data/home/liranhal/code/data/images/intra3_{f_name}')

    json_file_path = '/data/home/liranhal/code/data/train/annotations/instances_default.json'
    with open(json_file_path, encoding='utf-8') as f:
        data = json.load(f)
        print(data['images'])
        images_list = data['images']
        for i, img_dict in enumerate(data['images']):
            file_name = img_dict['file_name']
            images_list[i]['file_name'] = f'intra3_frame{file_name[-7:]}'
        data['images'] = images_list
        print(images_list)

    with open('/data/home/liranhal/code/data/train/annotations/instances_default.json', 'w') as f:
        json.dump(data, f)

if __name__ == '__main__':
    main()