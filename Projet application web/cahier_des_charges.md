# Diozik - Cahier des Charges

### Consigne :

Vous réaliserez une application web sur le thème de votre choix.
Vous réaliserez ce projet seul ou à deux.
Vous avez 4 semaines pour le réaliser à compter de la rentrée des vacances d’hiver.

Ce projet devra comporter :
Au moins un fichier html
Au moins un fichier css
Au moins un fichier js
Au moins une classe Python
Ce projet devra :
Utiliser le module Flask
Utiliser une base SQlite
Comporter au moins un algorithme de parcours d’arbres
Utiliser au moins une fonction Python récursive

Vous devrez donc rendre au moins un fichier html, un fichier css, un fichier js, des fichiers py, un fichier sql.
Chaque élève rendra également un document (doc, odt, pdf…) dans lequel vous décrirez la répartition des tâches au sein de votre groupe (si vous êtes en binôme), vous expliquerez précisément en quoi vous avez respecté le cahier des charges ci-dessus et vous décrirez les difficultés rencontrées.

### Barème :
| Technologie | Points |
| ------- | --- |
| HTML | 2 |
| CSS | 2 | 
| JS | 2 | 
| POO | 2 | 
| Flask | 2 | 
| BDD | 2 | 
| Parcours d’arbres | 2 | 
| Fonction récursive | 2 | 
| Intérêt du contenu | 2 | 
| Esthétique | 2 | 
| Bonus : utilisation de gitlab, github pour versionner le projet | 2 | 


## Site et barème :

	Le projet est de réaliser un site de streaming de musique avec des comptes personnels, avec un système d’abonnement premium qui aurait plus de liberté, avec des fonctions supplémentaires comme une boutique de crédits. Possibilité de s’abonner à un artiste (achat de crédit) ayant accès à certaines choses supplémentaires sur cet artiste. C’est l’artiste qui définit ce qu’il donne en plus quand qq paye. Le site fonctionne avec des crédits qu’il est possible d’acheter. Un utilisateur premium reçoit chaque mois un certain nombre de crédits qui permet de s’abonner à beaucoup d’artistes. Il est possible de noter les différentes musiques pour augmenter le référencement.

> HTML: Création d’une page web classique 
> <br/> CSS : Mise en forme esthétique de la page
> <br/> JS : Animation, fluidité
> <br/> POO : Utilisateur = un objet
> <br/> Flask : Relation élément de la page et base de données avec SQLITE et système de paiement.
> <br/> BDD : Base de données des utilisateurs avec python
> <br/> Parcours d’arbres : Différentes page web
> <br/> Fonction récursive : Algorithme de tri pour le référencement des musiques..
> <br/> Intérêt du contenu : Musique déposé par utilisateur …
> <br/> Esthétique : Optimisation de la page web avec le css et le js.
> <br/> Bonus : Utiliser GitHub pour versionner le projet.


## Arborescence du site : Objectif 13 pages

+ A/ Accueil (index.html) → écoutes récentes, nouveautés, top actuel…
  + B// Connexion (login.html) → Page de connexion
  + C// Créer un compte (register.html) → Page d'inscription
  + D// Profil (user.html) → Photo/nom, abonnements, best musiques…
    + Si le profil est celui de l’utilisateur :
    + E/// Édition de profil (user_edit.html) → modifier les infos user
    + F/// Abonnements (user_sub.html) → Abonnements (payants) user
    + G/// Suivis (user_follow.html) → Artistes suivis (gratuit) user
    + H/// Notes de l’user (user_rating.html) → Liste musiques préférées en fonction des notes effectuées
    + I/// Musiques publiées (user_tracks.html) → Listes des musiques publiées par l’utilisateur.
  + J// Boutique (boutique.html) → Achat premium et crédits
  + K// A propos (about.html) → Page à propos de nous
  + L// CGU & CGV + Privacy (terms.html) → Conditions générales d’utilisations, de ventes + politique de confidentialité
  + M// Contact (contact.html) → Page de contact


#### Schéma SALE :

![](https://github.com/Matthis-Emilien/Projet-application-web/blob/main/Projet%20application%20web/Arborescence.png)
(https://github.com/Matthis-Emilien/Projet-application-web/blob/main/Projet%20application%20web/Arborescence.png)

----------IDÉES POUR LE PROJET----------

système de notation

système d'inscription

a propos "farfelu" (Steve Jobs collaborateur, Elon Musk investisseur, Jeff Bezos a des actions chez Diozik, Bill Gates a dit “Le futur d’internet”)

chatbox

++ interaction

site de vente

site de streaming avec compte premium / artiste / basique

cookies pour rester enregistrer

sorte de spotify avec possibilité d'ajouter musique grâce à un compte artiste

offre boutiques /crédit utilisateur pour écouter des musiques

premium fictif

nom == "Diozik"
