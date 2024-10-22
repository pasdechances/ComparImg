# ComparImg

ComparImg analyse des images et detecte les doublons.
Le programme identifie les images identiques, legerement modifiees ou retournees et genere un fichier JSON listant les chemins des images en double.

Les images peuvent avoir differentes tailles et resolutions.
Les images peuvent être en formats BMP, JPG, JPEG, ou PNG.
Certain doublons d'images peuvent être de tailles differentes ou retournees et doivent donc être reconnues comme des doublons.

## Fonctions serveur actuelles

- Detecte les doublons exacte
- Detecte les doublons possible (variation de luminosite, changement mineur) soumis au faux positif.
- Visualisateur de doublons
- Tri les images en fonction des choix realise

## Ameliorations possibles
### front
- Ergonomie

### back
- Lancer les jobs via api
- Consulter l'etat des job via api
- Parametrer les jobs via api
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

Placer des dossiers d'images ou des images dans le repertoire img
Lancer le job de detection detect.py

    py ./server/detect.py

RDV sur http://localhost:5000/

