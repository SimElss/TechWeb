# Explications de l'application

Notre application gère une bibliothèque de livres stockés dans un dictionnaire. On peut ajouter, supprimer, modifier, lister et récupèrer le nombre de livres dans le dictionnaires à l'aide des différentes fonctions définies dans le fichier book.py du dossier services. Ces différentes fonctionalités sont accessibles depuis des pages html interractives. Elles peuvent également être testées via la route "/docs". En cas d'erreur l'utilisateur est redirigée vers une page dédiée contenant la description et le code d'erreur. Toutes les pages sont accessibles depuis la route "/liste" ou via l'url.

Lorsque l'on démarre l'application nous tombons sur la page de login : il existe un compte de base dont l'adresse mail est admin@juice-sh.op dont le mot de passe est Admin!123.
Si l'on veut s'enregistrer en tant qu'administrateur il faut se faire grader par un autre admin ou le faire à l main en modifiant l'attribut groupe de la liste des users dans le fichier database.py

## Routes

-"/" - pas de @get - redirige vers /liste
-"/login" - la première page sur laquelle on tombe on peut soit se connecter et arriver sur "/liste" soit cliquer sur s'enregistrer et arriver sur "/register"
-"/register - page pour s'enregistrer. Nous enregistre par défaut en tant que client
-"/save" - page de création de livres. Accesible seulement par les admins
-"/modify" - page de modification de livre. Accessible seulement par les admins
-"/liste" - page principale regroupe les redirections vers les autres pages (si admin) et liste les livres
-"/error" page d'erreur
-"/delete" - seulement en @post - supprime un livre
-"/tmp" - page temporaire vide servant de page de redirection vers "/liste" ou "/login" en fonction de si l'on s'est déjà connecté ou non
-"/administration" - accessible depuis un utilisateur administrateur on peut voir les utilisateurs, dégrader/regrader et bloqué/débloquer

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
