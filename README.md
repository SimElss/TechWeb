![Python](https://img.shields.io/badge/Python-%20?logo=python&logoColor=white&labelColor=3776AB&color=FFD43B)    ![HTML](https://img.shields.io/badge/HTML-%20?logo=html5&logoColor=white&labelColor=E34F26&color=1572B6)    ![+ Geek](https://img.shields.io/badge/%F0%9F%8D%BA-%2B%20Geek-yellow)
# BuyBeer - Le site n°1 de vente de bière pour geek et geekette

## Quesako ?
Ce dépôt contient le code du site ‘BuyBeer’, conçut dans le cadre du cours INFOB238 de l’UNamur.

Mais qu’est-ce que c’est, BuyBeer ?
Un site d’achat en ligne de bières pour geek et geekette !

Son fonctionnement, ainsi que sa mise en place, sont très simple.
## Mise en place
Une fois que le dépôt GitHub a été cloné, il suffit d’ouvrir le dossier dans un IDE moderne, comme [Visual Studio Code](https://code.visualstudio.com/) ou [WebStorm](https://www.jetbrains.com/fr-fr/webstorm/). 

Ouvrez ensuite un terminal, où vous entrerez dans l’ordre ces commandes :

1. Créer l'environnement virtuel : `python -m venv ./my-env`
2. Activer l'environnement :
	1. Sous Linux et MacOS : `source ./my-env/bin/activate`
	2. Sous Windows : `./my-env/Scripts/activate`
3. Installer les librairies : `pip install -r requirements.txt`
4. Démarrer l'application : `python main.py`

Si tout se passe bien, ceci devrait s’afficher dans le terminal :
![[Pasted image 20240526133321.png|500]]

Ouvrez alors un navigateur, et copier-coller le lien (ou alors, plus simple, maintenant `CTRL + Clic droit` pour directement ouvrir la page).

Apparaîtra alors le menu de connexion. De là, deux choix s’ouvrent à vous qui sont détaillés ci-dessous.
## Utilisateur
Vous êtes un utilisateur classique qui se rend sur BuyBeer pour faire des achats.
### Connexion
Si vous n’avez pas encore de compte, il vous faudra d’abord en créer un avant de pouvoir accéder au site.

Pour cela, vous devez cliquer sur l’option [“Incrivez-vous”](http://127.0.0.1:8000/register), où il vous sera demandé de renseigner :
- Un nom d’utilisateur, qui doit être unique
- Votre nom et prénom
- Votre adresse e-mail, où seront envoyés les mails de confirmation de vos commandes
- Un mot de passe <u>qui doit contenir au moins une majuscule, un nombre, un caractère spécial et faire plus de 8 caractères</u>

Une fois cela fait, il ne vous restera plus qu’à vous connecter sur la page d’accueil en renseignant l’adresse e-mail utilisée pour créer le compte ainsi que votre mot de passe.

### Achats
L’intérêt principal du site est bien sûr l’achat de bières. Depuis la page principale, une liste de bières est disponible.

Y sont indiqués : 
- Le nom de la bière
- Une brève description de celle-ci
- Son prix, en euros
- Une illustration de celle-ci
- Le stock de bières (si celui-ci est à 0, cela signifie que la bière est en rupture de stock)

Exemple avec la bière “Stark Stout” :
![[Pasted image 20240526140958.png|500]]

Une fois que le bouton “Acheter” est utilisée, la bière sera ajoutée dans le panier en cours (cela sera indiqué par le compteur se trouvant dans le coin droit de la bannière).

Attention, cela ne représente pas le nombre de bières achetées, uniquement le nombre de bières différentes.
### Panier
Le panier est accessible via la bannière supérieure, en cliquant sur le texte “Bonjour Mr/Mlle \[Prénom]”.

Un menu déroulant est alors disponible, avec le [panier](http://127.0.0.1:8000/panier) et [l’historique de commande](http://127.0.0.1:8000/order).

Dans le panier, il est possible de :
- choisir la quantité de bières à acheter
- supprimer une bière du panier
- payer le panier

Un bouton (🔄️) est disponible à droite de la quantité de bières à acheter. 
Il permet d’actualiser la quantité de bières par rapport au nombre réellement disponible en stock.
Il est donc nécessaire d’utiliser le bouton une fois que la quantité finale a été choisie, pour que le stock soit correctement mis à jour.

Une fois qu’une commande est finalisée, et payée, un mail de confirmation sera envoyé sur votre adresse mail.
### Historique de commande
Dans l’historique de commande, vous retrouverez toutes vos commandes. 

Il est possible de n’afficher que leur date et leur prix, ou en cliquant sur le bouton “Détails des commandes” situé en-dessous, d’afficher la composition précise de chaque commande.
### Profil
La dernière page importante du site est votre [profil](http://127.0.0.1:8000/order).

Vous y retrouverez votre profil client, où vous pouvez modifier vos différentes infos (sauf l’adresse mail, qui est liée à votre compte).

Il est également possible de modifier votre mot de passe, vous devrez alors indiquer votre ancien mot de passe avant de confirmer le nouveau.
## Admin
Vous êtes un administrateur du site web.

Pour accéder à la partie ‘Admin’ du site, vous devrez indiquer ces identifiants dans la page de connexion :
- Adresse mail : `admin@juice-sh.op`
- Mot de passe : `Admin!123`

Si dessous seront détaillées les pages où des différences existent par rapport à la version ‘Utilisateur’.
### Achats
Sur la page principale, il est possible de modifier les informations liées à une bière via le bouton $\leftrightarrow$.

Il est possible de modifier :
- le nom
- la brasserie
- le prix (en euros)
- le stock restant (si une nouvelle commande vient d’arriver, ou alors qu’il reste moins de bières que prévues)
- la description

Il est également possible d’ajouter une nouvelle bière. Les informations à renseigner sont les mêmes que pour la modification d’une bière.

### Page admin
Sur cette page, il est possible de gérer les utilisateurs :
- Promouvoir au rang d’administateur
- Rétrograder un administrateur (attention à ne pas rétrograder tout les admins, auquel cas plus aucun admin n’aurait accès au site)
- Bloquer un utilisateur, qui l’empêche d’accéder au site

## Dépannage

### Mon mail de confirmation n’apparaît pas !

Pas de panique, vérifiez le dossier ‘Spam’ de votre boîte mail.
Le mail s’y trouve certainement.

### J’ai perdu mon mot de passe, que faire ?

Il vous suffit de le [réinitialiser](http://127.0.0.1:8000/new_mdp) via la page de connexion en indiquant votre e-mail, lié au mot de passe, ainsi que l’ancien et nouveau mot de passe.

### J’ai ajouté une bière à ma liste de commandes, mais je ne peux pas valider le panier ?!

Vérifiez bien le stock disponible pour la bière en question, il est plus que probable que celle-ci soit en rupture de stock.

### J’ai des erreurs au moment de l’initialisation, des packages sont manquants

Avez-vous bien utilisé la commande `pip install -r requirements.txt` ?

Cette commande permet d’installer, en un coup, l’entièreté des packages nécessaires. 
Si celle-ci ne fonctionne pas, vous pouvez essayer de les installer manuellement.

Vérifiez également que ‘pip’ est bien à jour avec la commande `python.exe -m pip install --upgrade pip` qui mettra à jour ‘pip’.

Enfin, si tout cela ne fonctionne pas ou que vous avez une erreur vous indiquant que Python ou Pip n’est pas installé, renseignez-vous via cet [article](https://www.geeksforgeeks.org/how-to-install-pip-on-windows/).