# ComparImg

ComparImg analyse des images et détecte les doublons.
Le programme identifie les images identiques, légèrement modifiées, ou retournées et génére un fichier JSON listant les chemins des images en double.

Les images peuvent avoir différentes tailles et résolutions.
Les images peuvent être en formats BMP, JPG, JPEG, ou PNG.
Certain doublons d'images peuvent être de tailles différentes ou retournées et doivent donc être reconnues comme des doublons.



## Prerequis

    python

module 

    pip install pillow imagehash pandas
    pip install flask flask_cors

