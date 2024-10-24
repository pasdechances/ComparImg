# ComparImg

ComparImg analyse des images et detecte les doublons.
Le programme identifie les images identiques, legerement modifiees ou retournees et genere un fichier JSON listant les chemins des images en double.

Les images peuvent avoir differentes tailles et resolutions.
Les images peuvent être en formats BMP, JPG, JPEG, ou PNG.
Certain doublons d'images peuvent être de tailles differentes ou retournees et doivent donc être reconnues comme des doublons.

## Fonctions actuelles

- Detecte les doublons exacte
- Detecte les doublons possible (variation de luminosite, changement mineur) soumis au faux positif.
- Administration et choix du sort final des images detectes comme double
- Tri les images en fonction des choix realise
- Lancer les jobs via api
- Consulter l'etat des job via api
- Parametrer les jobs via api

## Information

- Le hsize est la laille pour le hachage perceptuel, plus grand = plus de détail.
- La tolérance est une valeur en bits pour le nombre de différences percue, l'augmentation permet de détecter des images plus modifiées, mais peut générer plus de faux positifs.

## Ameliorations possibles
### front
- Ergonomie

### back
- Ergonomie
- Integrer des modeles de machine learning pour l'analyse d'image
- Mettre la possibilite de traiter les images via les modeles
- Mettre la possibilite de traiter les images via hash puis traiter le resulta des Hash via modele

### general

- Facilite le deploiement pour arriver au "one click"


## Prerequis

Installer python.

### Modules
Traitement

    pip install pillow imagehash pandas 

API

    pip install flask flask_cors


## Fonctionnement

Lancer le serveur "api.py"

    py ./server/api.py

Deux option sont disponible pour la suite : 

1. Via IHM

RDV sur http://localhost:5000/, dans l'encart "Detector" clickez sur custom, placez le chemin du dossier contenant les images (recursif : inspectera les sous dossier).
Reglez les differents parametres et clickez sur "launch" pour lancer le job
Le resultat s'affichera a la fin du job.

2. Via script 

Placer des dossiers d'images ou des images dans le repertoire img puis lancer le job de detection detect.py

    py ./server/detect.py

une aide est disponible avec 

    py ./server/detect.py -h

enfin pour visualiser le resultat RDV sur http://localhost:5000/

