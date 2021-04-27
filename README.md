![Screenshot](image-readme/yellow_icon.ico) ![Screenshot](image-readme/white_icon.ico) ![Screenshot](image-readme/blue_icon.ico)
# Diozik

### _Bienvenue sur Diozik._
[Diozik](https://diozik.herokuapp.com/) est un service de streaming numérique qui propose de la musique, des podcasts...

Les fonctionnalités sont les suivantes :
- écouter de la musique
- mettre des musiques en ligne
- consulter les profils d'utilisateurs, intéragir, rechercher

## Démarrer l'application

### _Démarrer à l'application en ligne_

**Il y a plusieurs manières de procéder afin d'accéder à l'application.**

- Premièrement, on peut naviguer sur celle-ci via le lien suivant ramenant au site héberger à l'aide de Heroku :

    **ICI** (https://diozik.herokuapp.com)
    
    _Heroku, l'hébergeur, ne peut pas écrire dans les fichiers GitHub. Cela signifie que toute intérection avec des fichiers tel que la base de donnée ne sera pas enregistrée. Ainsi, les modifications que vous effectuerez seront éffacées dès lors qu'une mise à jour du site sera déployée par Heroku ou que les caches de votre navigateur seront effacé. Pour que vos modifications soient enregistrées, il faut ouvrir l'application en local comme décris lors de la seconde méthode._

### _Démarrer à l'application en local_

_Prérequis : [Python 3](https://docs.python.org/3/index.html)_

- Deuxièmement, pour démarrer l'application via le code source, voici la procédure :

   1. ***Installer [Flask](https://flask.palletsprojects.com/en/1.1.x/)***
      
      Pour utiliser l'application, il est nécessaire d'installer [Flask](https://flask.palletsprojects.com/en/1.1.x/).
      
      Commencez par créer un dossier qui contiendra l'application web.
      Pour installer [Flask](https://flask.palletsprojects.com/en/1.1.x/), il est nécessaire de créer un environnement virtuel `venv`. Cet environnement virtuel python se trouvera dans le dossier du projet.
      
      Pour créer cet environnement virtuel, ouvrer le terminal (Linux) ou l'invité de commande (Windows). Il est possible que votre session nécessite les droits d'administrateur. Accéder grâce à votre terminal au chemin de votre dossier. Pour cela, utilisez la commande `cd` (Windows & Linux) :
      
      ```
      $ cd Path\Folder\
      ```
      
      Ensuite, Python 3 permet de créer l'environnement virtuel. Sous Linux, utilisez cette commande :
      ```
      $ python3 -m venv venv
      ```
      Sous Windows, utilisez cette commande :
      ```
      > py -3 -m venv venv
      ```
      
      Désormais, l'environnement virtuel est créé. Il faut maintenant l'activé. Pour ce faire, utilisez sous Linux cette commande :
      ```
      $ . venv/bin/activate
      ```
      Utilisez sous Windows cette commande :
      ```
      > venv\Scripts\activate
      ```
      Une fois ces étapes passées, il est possible d'installer [Flask](https://flask.palletsprojects.com/en/1.1.x/) pour ce faire, il suffit d'utilisez dans le terminal la commande suivante (Windows & Linux) :
      ```
      $ pip install Flask
      ```
      Bravo ! Vous venez d'installer le module [Flask](https://flask.palletsprojects.com/en/1.1.x/) ! Si vous souhaitez travaillez avec la toute dernière version de flask, vous pouvez utiliser cette dernière commande (Windows & Linux) :
      ```
      $ pip install -U https://github.com/pallets/flask/archive/master.tar.gz
      ```
      Pour plus d'informations à propos de l'installation de [Flask](https://flask.palletsprojects.com/en/1.1.x/), vous pouvez consultez la documentation ici : https://flask.palletsprojects.com/en/1.1.x/installation/#install-flask

   2. ***Télécharger l'application***
      
      Une fois [Flask](https://flask.palletsprojects.com/en/1.1.x/) installé, vous pouvez télécharger le code source de l'application. **Attention !** Le code source utilisable en local n'est pas exactement le même que le code source hébergé sur https://diozik.herokuapp.com/. Pour une utilisation optimale, quelques modifications ont été apporté auc fichiers utilisés par Heroku. De plus, certains fichiers sont nécessaire pour l'hébergement, mais ne sont d'aucune utilités pour une un démarrage en local. Ainsi, les fichiers à télécharger sont ceux du dossier `sourcecode`.
      
      Téléchargez l'ensemble des fichers du dossier `sourcecode` que vous placerez dans le dossier créer précédemment. Si toutes les étapes on été réalisées avec succès, vous êtes prêt pour démarrez l'application.
      
   3. ***Démarrer l'application***
      
      Pour démarrer l'application il est nécessaire que l'environnement virtuel soit activé ! Certains environnements de développements (IDE) permettent une activation automatique de l'environnement de développement, mais si vous n'en utilisez pas, ou que vous ne savez pas si le votre l'active, veillez à le faire manuellement comme précédemment lors de l'installation de Fask. Pour ce faire, accèdez grâce à votre terminal (Linux) ou invité de commande (Windows) au chemin de votre dossier. Pour cela, utilisez la commande `cd` (Windows & Linux) :
      
      ```
      $ cd Path\Folder\
      ```
      Ensuite, activez votre environnement virtuel. Pour ce faire, utilisez sous Linux cette commande :
      ```
      $ . venv/bin/activate
      ```
      Utilisez sous Windows cette commande :
      ```
      > venv\Scripts\activate
      ```
      Une fois cela effectuer, vous pouvez démarrer l'application en exécutez le fichier `app.py`.  Pour ce faire, en restant dans le même terminal, effectuez la commande suivante (Windows & Linux) :
      ```
      $ python3 app.py
      ```
      Si vous possedez un IDE, vous pouvez aussi exécuter le fihcier à partir de celui-ci.
      
      Si le démarrage c'est bien effectué, vous devriez être capable de lire un message similaire à celui-ci sur votre terminal :    
      

      ![Screenshot](image-readme/launcher.jpg)

      Si c'est le cas, bravo ! Vous êtes prêt à utiliser l'application ! Vous pouvez y accéder avec le lien qui s'affiche dans votre teminale sur la forme suivante :
      ```
      * Running on http://127.0.0.1:5000/ (Press CTRL+C to quit)
      ```
      Si le réponse est différente, suivez les informations d'erreur pour essayer de résoudre le problème. Il est possible que votre port `5000` soit utilisé par une autre application. Dans ce cas, vous pouvez modifier à votre guise les deux dernières lignes du programme `app.py` :
      ```py
      if __name__ == '__main__':
       app.run(host='localhost', port=8000, debug=True)
      ```
      _Ceci est un exemple, vous pouvez modifier les valeurs de `host` et `port`._

      Si le problème perssiste, vous pouvez nous contacter sur https://diozik.herokuapp.com/contact.

## A notifier

La boutique est juste esthétique étant donner qu'elle ne changera rien lors d'un achat sur Diozik.
