# Explications de l'application

Notre application gère une bibliothèque de livres stockés dans une base de données On peut ajouter, supprimer, modifier, lister et récupèrer le nombre de livres dans la base de données à l'aide des différentes fonctions définies dans le fichier book.py ou users.py du dossier services. Ces différentes fonctionalités sont accessibles depuis des pages html interractives. Elles peuvent également être testées via la route "/docs". En cas d'erreur l'utilisateur est redirigée vers une page dédiée contenant la description et le code d'erreur. Toutes les pages sont accessibles depuis la route "/liste" ou via l'url. L'utilisateur peut également acheter des livres ou consulter son profil où il pourra y modifier au besoin ses informations personelles. Un utilisateur non-cnnecté peut seulement consulter les livres.

Lorsque l'on démarre l'application nous tombons sur la page de login : il existe un compte de base dont l'adresse mail est admin@juice-sh.op dont le mot de passe est Admin!123. Pour se connecter en tant qu'utilisater : email = user@gmail.com et mot de passe = Password!123
Si l'on veut s'enregistrer en tant qu'administrateur il faut se faire grader par un autre admin ou le faire à la main en modifiant l'attribut groupe de l'utilisateur dans le fichier database.py.

## Routes

-"/" - pas de @get - redirige vers /liste
-"/login" - la première page sur laquelle on tombe on peut soit se connecter et arriver sur "/liste" soit cliquer sur s'enregistrer et arriver sur "/register" soit ne pas se connecter et arriver sur /liste
-"/register - page pour s'enregistrer. Nous enregistre par défaut en tant que client
-"/save" - page de création de livres. Accesible seulement par un utilisateur connecté | si un utilisateur rajoute un livre il en devient propriétaire
-"/modify/id" - page de modification de livre. Accessible seulement par les admins ou le propriétaire du livre d'id : id
-"/liste" - page principale regroupe les redirections vers les autres pages (si admin ou utilisateur connecté (profile)) et liste les livres
-"/error/description/url" page d'erreur avec la description et la page de redirection associée
-"/delete/id" - seulement en @post - supprime un livre d'id : id
-"/tmp" - page temporaire vide servant de page de redirection vers "/liste" ou "/login" en fonction de si l'on s'est déjà connecté ou non
-"/administration" - accessible depuis un utilisateur administrateur on peut voir les utilisateurs, dégrader/regrader et bloqué/débloquer
-"/buy/id" - achète le livre d'id : id | un propriétaire ne peut pas acheter son propre livre
-"/logout" - seulement en POST - déconnecte l'utilisateur actuel
-"/new_mdp" - page de changement de mot de passe pour un utilisateur et besoin de l'email si l'utilisateur n'est pas connecté | accessible depuis /login ou /profile
-"/profile" - affiche le profil de l'utilisateur. Affiche ses livres en vente ou vendus. Possibilité de changer ses infos personnelles depuis cette page ou encore d'ajouter un livre ou de changer son mot de passe.

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

python main.py
