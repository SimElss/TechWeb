# Explications de l'application

Notre application gère une bibliothèque de livres stockés dans un dictionnaire. On peut ajouter, supprimer, modifier, lister et récupèrer le nombre de livres dans le dictionnaires à l'aide des différentes fonctions définies dans le fichier book.py du dossier services. Ces différentes fonctionalités sont accessibles depuis des pages html interractive. Elles peuvent également être testées via la route "/docs". En cas d'erreur l'utilisateur est redirigée vers une page dédiée contenant la description et le code d'erreur. Toutes les pages sont accessibles depuis la route "/liste" ou via l'url.

## Routes

-"/" - pas de @get - redirige vers /liste
-"/save" page de création de livres
-"/modify" page de modification de livre
-"/liste" page principale regroupe les redirections vers les autres pages et lite les livres
-"/error" page d'erreur
-"/delete" - seulement en @post - supprime un livre

## Installation en ligne de commande

-Créer l'environnement virtuel : python -m venv ./my-env

### Activer l'environnement

### Sous Linux et MacOS :

source ./my-env/bin/activate

### Sous Windows :

./my-env/Scripts/activate

### Installer les librairies

pip install -r requirements.txt

### Démarrer l'application

python Main.py
