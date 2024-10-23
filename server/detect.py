import os
import csv
import json
import argparse
from PIL import Image, UnidentifiedImageError
import imagehash
import pandas as pd
from collections import defaultdict


HASH_SIZE = 16
TOLERANCE = 90
error_log = []
hash_dict = {}


def calculate_image_hash(image_path):
    global HASH_SIZE
    try:
        with Image.open(image_path) as img:
            try:
                img = img.resize((256, 256)).convert('L')  # le 'L' c'est pour la conversion en niveau de gris
                return imagehash.phash(img, hash_size=HASH_SIZE)
            except OSError as e:
                print(f"Erreur lors du chargement de l'image {image_path}: {e}")
            except Exception as e:
                print(f"Erreur imprévue pour l'image {image_path}: {e}")
            
    except UnidentifiedImageError:
        error_log.append({"file": image_path, "error": "Unsupported image format"})
        return None


def analyze_images(image_dir, csv_file):
    image_id = 1
    with open(csv_file, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(['image_id', 'image_path', 'image_hash'])

        for root, dirs, files in os.walk(image_dir):
            for file_name in files:
                if file_name.lower().endswith(('.jpg', '.jpeg', '.png', '.bmp')):
                    image_path = os.path.join(root, file_name)
                    image_hash = calculate_image_hash(image_path)

                    if image_hash:
                        writer.writerow([image_id, image_path, str(image_hash)])
                        image_id += 1

def read_csv_with_utf8(csv_file):
    try:
        df = pd.read_csv(csv_file, encoding='utf-8')
        return df
    except UnicodeDecodeError:
        print(f"Erreur d'encodage lors de la lecture de {csv_file}.")
        # Réessayer avec un autre encodage
        df = pd.read_csv(csv_file, encoding='latin-1')
        return df

def find_duplicates(csv_file, results_file):
    global TOLERANCE
    group_id = 0
    duplicate_groups = []
    seen_images = set()  
    duplicates = defaultdict(list)
    
    df = read_csv_with_utf8(csv_file)

    for i, row in df.iterrows():
        image_id = row['image_id']
        image_path = row['image_path']
        image_hash = row['image_hash']

        if image_id in seen_images:
            continue

        for j, other_row in df.iterrows():
            if i != j:
                other_image_id = other_row['image_id']
                other_image_path = other_row['image_path']

                if other_image_id in seen_images:
                    continue

                hamming_distance = imagehash.hex_to_hash(image_hash) - imagehash.hex_to_hash(other_row['image_hash'])
                if hamming_distance <= TOLERANCE:
                    duplicates[group_id].append({
                        "image_id": other_image_id,
                        "image_path": other_image_path,
                        "tag": "waiting",
                        "hamming_distance": hamming_distance
                    })
                    seen_images.add(other_image_id)

        if duplicates[group_id]:
            seen_images.add(image_id)
            duplicates[group_id].append({
                "image_id": image_id,
                "image_path": image_path,
                "tag": "waiting",
                "hamming_distance": "reference"
            })
            duplicate_groups.append({
                "group_id": group_id,
                "images": duplicates[group_id]
            })
            group_id += 1


    with open(results_file, 'w') as file:
        json.dump(duplicates, file, indent=4)

def write_error_log(error_file):
    with open(error_file, 'w') as file:
        json.dump(error_log, file, indent=4)

def main():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    data_dir = os.path.abspath(os.path.join(base_dir, '..', 'data'))
    csv_file = os.path.join(data_dir, 'image_hashes.csv')
    error_file = os.path.join(data_dir, 'error.json')
    results_file = os.path.join(data_dir, 'resultats.json')

    parser = argparse.ArgumentParser(description='detect.py arguments')
    parser.add_argument('-i', '--image_dir', type=str, help="Répertoire d'images à analyser. Valeur par defaut : ../data/img", default=os.path.join(data_dir, 'img'))
    parser.add_argument('-s', '--hsize', type=int, help='Taille pour le hachage perceptuel, plus grand = plus de détail. Valeur par defaut : 16', default=16)
    parser.add_argument('-t', '--tolerance', type=int, help="Tolérance en bits pour les différences, l'augmentation permet de détecter des images plus modifiées, mais peut générer plus de faux positifs. Valeur par defaut : 90", default=90)
    args = parser.parse_args()

    global HASH_SIZE, TOLERANCE
    HASH_SIZE = args.hsize
    TOLERANCE = args.tolerance
           
    analyze_images(args.image_dir, csv_file)
    find_duplicates(csv_file, results_file)
    write_error_log(error_file)
    print(f"Analyse terminée. Résultats dans {results_file} et erreurs dans {error_file}")

if __name__ == '__main__':
    main()


