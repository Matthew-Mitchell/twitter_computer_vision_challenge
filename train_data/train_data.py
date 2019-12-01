import os
import json
import cv2


DATA_DIR = '../raw'
IMG_DIR = os.path.join(DATA_DIR, 'images')
ANNO_DIR = os.path.join(DATA_DIR, 'annotation')


def png2jpg(folder):
    paths = [os.path.join(folder, fn) for fn in os.listdir(folder) if os.path.isfile(os.path.join(folder, fn))]

    for path in paths:
        img = cv2.imread(path)
        base, ext = os.path.splitext(path)

        print(path)

        if ext.lower() != '.jpg':
            jpg_path = f"{base}.jpg"
            cv2.imwrite(jpg_path, img)

            os.remove(path)


def via_anno2json(via_anno_file):
    with open(via_anno_file, 'r') as jp:
        anno_info_list = json.load(jp)

    _via_img_metadata = anno_info_list['_via_img_metadata']
    for key in list(_via_img_metadata.keys()):
        anno_info = _via_img_metadata[key]
        img_file_name = anno_info['filename']
        objects = []
        for region in anno_info['regions']:
            objects.append({
                'name': 'following_button',
                'bndbox': {
                    'xmin': region['shape_attributes']['x'],
                    'ymin': region['shape_attributes']['y'],
                    'xmax': region['shape_attributes']['x'] + region['shape_attributes']['width'],
                    'ymax': region['shape_attributes']['y'] + region['shape_attributes']['height']

                }
            })

        anno_file_name = os.path.join(ANNO_DIR, os.path.splitext(img_file_name)[0] + ".json")
        img = cv2.imread(os.path.join(IMG_DIR, os.path.splitext(img_file_name)[0] + '.jpg'))
        with open(anno_file_name, 'w') as jp:
            anno_info = {
                'filename': os.path.splitext(img_file_name)[0] + '.jpg',
                'size': {
                    'width': img.shape[1],
                    'height': img.shape[0]
                },
                'object': objects
            }
            json.dump(anno_info, jp)


if __name__ == '__main__':

    # png2jpg(folder=IMG_DIR)
    via_anno2json(os.path.join(DATA_DIR, 'via_project_1Dec2019_13h8m.json'))
