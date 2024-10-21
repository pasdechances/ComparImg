import os
import json
import shutil



INPUT_FILE = 'resultats.json'
IMG_FOLDER = './img'
ARCHIVE_FOLDER = './archive'
TRASH_FOLDER = './imgTrash'

def load_tags(json_file):
    with open(json_file, 'r') as f:
        data = json.load(f)
    tags = []
    for key, value in data.items():
        for item in value:
            tags.append(item)
    return tags

def move_images(tags, img_dir, archive_dir, trash_dir):
    os.makedirs(archive_dir, exist_ok=True)
    os.makedirs(trash_dir, exist_ok=True)
    
    for tag_info in tags:
        img_path = tag_info['image_path']
        tag = tag_info['tag']
        
        try:
            if tag == 'keep':
                destination = os.path.join(archive_dir, os.path.basename(img_path))
                shutil.move(img_path, destination)
                print(f"Moved {img_path} to {archive_dir}")
            elif tag == 'trash':
                destination = os.path.join(trash_dir, os.path.basename(img_path))
                shutil.move(img_path, destination)
                print(f"Moved {img_path} to {trash_dir}")
            else:
                print(f"Unknown tag '{tag}' for image {img_path}")
        except Exception as e:
            print(f"Error moving image {img_path}: {e}")

def main():   
    tags = load_tags(INPUT_FILE)
    move_images(tags, IMG_FOLDER, ARCHIVE_FOLDER, TRASH_FOLDER)

if __name__ == "__main__":
    main()