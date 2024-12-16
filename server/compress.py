import argparse
import os
from PIL import Image


def parse_arguments():
    """Parse les arguments de la ligne de commande."""
    parser = argparse.ArgumentParser(description="Compresser des fichiers PNG, JPG ou JPEG.")
    parser.add_argument("-p","--directory", type=str, help="Chemin du dossier contenant les images à traiter.")
    parser.add_argument("-r","--recursive", action="store_true", help="Traiter les sous-dossiers de manière récursive.")
    parser.add_argument("files", nargs="*", help="Chemin(s) vers les fichiers spécifiques à compresser (optionnel si --directory est utilisé).")
    parser.add_argument("-m","--modify-source", action="store_true", help="Modifie le fichier source après compression.")
    parser.add_argument("-d","--delete-source", action="store_true", help="Supprime le fichier source après compression.")
    parser.add_argument("-c","--compression", type=int, help="Pourcentage de compression de 1 à 100, 100 est la qualité optimal.", default=100)
    parser.add_argument("-x","--resolution", type=str, help="Nouvelle résolution, format: largeurxhauteur (ex: 800x600).",  default="1920x1080")
    parser.add_argument("-n","--no-ratio", action="store_true", help="Ne conserve pas le ratio hauteur/largeur en cas de redimensionnement.")
    parser.add_argument("-s","--size-threshold", type=float, help="Seuil en MB pour traiter le fichier.", default=1)
    return parser.parse_args()

def get_image_files(directory, recursive):
    """Récupère les fichiers images dans un dossier, avec ou sans récursivité."""
    valid_extensions = {".png", ".jpg", ".jpeg"}
    image_files = []

    if recursive:
        for root, _, files in os.walk(directory):
            for file in files:
                if os.path.splitext(file.lower())[1] in valid_extensions:
                    image_files.append(os.path.join(root, file))
    else:
        for file in os.listdir(directory):
            if os.path.isfile(os.path.join(directory, file)) and os.path.splitext(file.lower())[1] in valid_extensions:
                image_files.append(os.path.join(directory, file))

    return image_files

def compress_image(file_path, output_path, compression=100, resolution="1920x1080", no_ratio=False):
    """
    Compresse une image avec un pourcentage ou une nouvelle résolution.

    :param file_path: Chemin de l'image source.
    :param output_path: Chemin où sauvegarder l'image compressée.
    :param compression: Niveau de compression en pourcentage (1-100), optionnel.
    :param resolution: Résolution cible sous forme "largeurxhauteur" (ex: "800x600"), optionnel.
    :param no_ratio: Ne conserve pas le ratio hauteur/largeur lors du redimensionnement, par défaut True.
    """
    try:
        with Image.open(file_path) as img:
            if resolution:
                max_width, max_height = map(int, resolution.split("x"))
                orig_width, orig_height = img.size
                
                # Calculer la nouvelle taille tout en respectant le ratio
                if no_ratio:
                    img = img.resize((max_width, max_height))
                else:
                    ratio = min(max_width / orig_width, max_height / orig_height)
                    new_width = int(orig_width * ratio)
                    new_height = int(orig_height * ratio)
                    img = img.resize((new_width, new_height), Image.Resampling.LANCZOS)

            if compression:
                img.save(output_path, quality=compression, optimize=True)
            else:
                img.save(output_path, optimize=True)
    except Exception as e:
        print(f"Erreur lors de la compression de {file_path}: {e}")

def delete_image(file_path):
    """
    Supprime un fichier image de manière sécurisée.

    :param file_path: Chemin du fichier à supprimer.
    """
    try:
        if os.path.exists(file_path):
            os.remove(file_path)
            print(f"Fichier supprimé : {file_path}")
        else:
            print(f"Fichier non trouvé : {file_path}")
    except Exception as e:
        print(f"Erreur lors de la suppression de {file_path} : {e}")

def process_files(args):
    """Récupère les fichiers à traiter selon les options fournies."""
    files_to_process = []
    if args.directory:
        files_to_process = get_image_files(args.directory, args.recursive)
    files_to_process.extend(args.files)

    if not files_to_process:
        print("Aucun fichier à traiter.")
    else:
        print(f"Fichiers à traiter ({len(files_to_process)}):")
        for file in files_to_process:
            print(f" - {file}")

    return files_to_process

def handle_compression_and_deletion(files, args):
    """Gère la compression et la suppression des fichiers selon les arguments."""
    for file_path in files:

        if args.size_threshold:
            file_size_mb = os.path.getsize(file_path) / (1024 * 1024)
            if file_size_mb < args.size_threshold:
                print(f"Fichier ignoré (taille inférieure au seuil) : {file_path}")
                continue
        
        if args.modify_source:
            output_path = file_path
        else:
            base, ext = os.path.splitext(file_path)
            output_path = f"{base}_resize{ext}"

        compress_image(
            file_path = file_path,
            output_path = output_path,
            compression = args.compression,
            resolution = args.resolution,
            no_ratio = args.no_ratio
        )

        if args.delete_source and not args.modify_source :
            delete_image(file_path)

def main():
    args = parse_arguments()
    files_to_process = process_files(args)
    handle_compression_and_deletion(files_to_process, args)


if __name__ == "__main__":
    main()