import os
import json
import shutil


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.abspath(os.path.join(BASE_DIR, '..', 'data'))
INPUT_FILE = os.path.join(DATA_DIR, 'resultats.json')
TRASH_FOLDER = os.path.join(DATA_DIR, 'imgTrash')

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
    tags = load_tags(INPUT_FILE)
    move_images(tags, TRASH_FOLDER)

if __name__ == "__main__":
    main()