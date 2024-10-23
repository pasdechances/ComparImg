import os
import json
import shutil
import argparse


def load_tags(json_file):
    with open(json_file, 'r') as f:
        data = json.load(f)
    tags = []
    for key, value in data.items():
        for item in value:
            tags.append(item)
    return tags

def move_images(tags, trash_dir):
    os.makedirs(trash_dir, exist_ok=True)
    trash = 0
    error = 0
    
    for tag_info in tags:
        img_path = tag_info['image_path']
        tag = tag_info['tag']
        
        try:
            if tag == 'trash':
                destination = os.path.join(trash_dir, os.path.basename(img_path))
                shutil.move(img_path, destination)
                print(f"Moved {img_path} to {trash_dir}")
                trash += 1
        except Exception as e:
            print(f"Error moving image {img_path}: {e}")
            error += 1

    print(f"{trash} moved in trash, {error} errors encountred")

def main():   
    base_dir = os.path.dirname(os.path.abspath(__file__))
    data_dir = os.path.abspath(os.path.join(base_dir, '..', 'data'))
    input_file = os.path.join(data_dir, 'resultats.json')

    parser = argparse.ArgumentParser(description='sorter.py arguments')
    parser.add_argument('-t', '--trash_folder', type=str, help="Répertoire d'images non retenue. Valeur par defaut : ../data/imgTrash", default=os.path.join(data_dir, 'imgTrash'))
    args = parser.parse_args()

    tags = load_tags(input_file)
    move_images(tags, args.trash_folder)

if __name__ == "__main__":
    main()