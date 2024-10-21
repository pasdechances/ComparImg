# ComparImg

ComparImg analyse des images et détecte les doublons.
Le programme identifie les images identiques, légèrement modifiées, ou retournées et génère un fichier JSON listant les chemins des images en double.

Les images peuvent avoir différentes tailles et résolutions.
Les images peuvent être en formats BMP, JPG, JPEG, ou PNG.
Certain doublons d'images peuvent être de tailles différentes ou retournées et doivent donc être reconnues comme des doublons.

## Fonctions serveur actuelles

- Detecte les doublons exacte
- Detecte les doublons possible (variation de luminosité, changement mineur) soumis au faux positif.
- Visualisateur de doublons
- Tri les images en fonction des choix réalisé (WIP)

## Améliorations possibles
### front
- Selection des images a conserver
- Ergonomie

### back
- Lancer les jobs via api
- Consulter l'etat des job via api
- Parametrer les jobs via api
- Intégrer des modèles de machine learning pour l'analyse d'image
- Mettre la possibilité de traiter les images via les modeles
- Mettre la possibilité de traiter les images via hash puis traiter le résulta des Hash via modèle

### général

- Facilité le déploiement pour arriver au "one click"


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

Placer des dossiers d'images ou images dans le répertoire img
Lancer le job de détection detect.py

    py ./server/detect.py

RDV sur http://localhost:5000/

