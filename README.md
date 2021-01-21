# TD_LOG_X_PEP 2020
Mai-Linh Duong 
Juliette Collins 
Antoine Franceschi
Arnaud Rubin 

##### Objectif

Ce projet a pour but de développer une application web pour la gestion de la junior entreprise. Il regroupe plusieurs fonctionnalité essentielle à une bonne gestion de la Junior. 


#### Lancement du site
#         - Execution via docker: 
aller dans l'invite de commande (ou le terminal) est effectuer les commandes suivante: 
- "make build" (prend environ 10min)
- "make run" (prend environ 1min)
Le site va pas apparaître sur localhost:5000. Il faut aller voir l'ip du host docker(accessible avec `make print_ip`) remarque: Il est préférable de bind sur http 80/https 443 port au lieu de 5000 pour un usage plus poussé


#         - Execution sur python:
Exécuter le fichier `site.py`. Puis se rendre à l'adresse indiquer du type de "http://127.0.0.1:5000/"



##### Technologies utilisées
- **front** : `html`, `javascript`, `css`
- **back** :  `python`, `flask`,`sqlite`

##### ##################################### Construction de site.py ####################################

site.py rassemble l'integralité du backend du site web. 

ligne 1-25: importation de tous les modules 

ligne 25-235: creation de toutes les bases de données. Ces bases de données sont codées en tant que classe. Chaque classe possède ses propres methodes utiles pour la gestion de la base de données .

ligne 235-253: creation de la page d'acceuil du site web. cette page est accessible uniquement si l'utilisateur a passé la page de login 

ligne 255-282: creation de la page de login. Des que l'utilisateur execute le fichier 'site.py' et qu'il se rend à l'adresse indiquée. Il va alors tomber directement sur cette page de login. 

ligne 282-383: creation de la fonctionnalité tresorerie. cette page permet l'enregistrement/modification/supression de factures. elle indique via un code couleur si la facture est arrivé à echeance ou non. 

ligne 383-437: creation de la fonctionnalité weekly. Pendant notre mandat au seins de la junior entreprise, nous realisons regulierement des reunions pour faire un point sur les differentes etudes. Pour garder une trace ecrire de ces reunions, chaque membre de la junior entreprise rempli un tableau indiquant ses avancés et ses projets. La page web que nous avons créé permet à chaque membre de la junior entreprise de remplir un tableau (avec ses projets/ avancés) et nous pouvons telecharger le tableau au format csv. Cela nous permet de garder une trace ecrite de ses reunions. 

ligne 437-628: creation de la fonctionnalité agenda. Chaque membre de la junior entreprise peut ecrire ses rendez-vous client/reunion en cliquant simplement sur un jour de la semaine. 

ligne 630-689: creation de la fonctionnalité information personnelle. Chaque membre de la junior entreprise peut modifier NOM/adresse mail/mot de passe d'identification. Cette page est la même pour chaque membre de la junior entreprise sauf le DSI (directeur des systemes informatiques). En effet le DSI est la seul personne à avoir accès à l'ensemble des informations des membres de la junior entreprise. Le DSI peut ajouter/supprimer des utilisateurs. Il peut aussi nomer une personne DSI. Il peut y avoir plusieurs personne DSI. Cependant un DSI ne peut pas s'enlever l'autorisation DSI. Seul un autre DSI peut le faire. Cela permet d'avoir en permanence un DSI qui a acces à toutes les informations. 

NB: lorsqu'une personne modifie ses données personnelles celle ci doit automatiquement se re-identifier. 

ligne 689-785: creation de la fonctionnalité 'pep_recrute'. Lorsqu'une entreprise nous demande une missions, nous demandons, via l'envoie d'un mail, à l'ensemble des eleves de 1A/2A/3A s'ils sont interessés par l'etude en question. Cette fonctionnalité "pep_recrute" permet l'envoie de ce mail. 

ligne 786-831: creation de la fonctionnalité mail. Cette fonctionnalité permet l'envoie de mail de prospection. Le mail-type est rempli/enoyé  automatiquement en fonction des données renseignées dans le formulaire. 

ligne 832-857: creation de la fonctionnalité statistique. Cette fonctionnalité permet de suivre l'activité de la junior entreprise et d'en extraire quelques indicateurs de performance: Nombre de mail envoyé par jour, nombre de mail envoyé par secteur,...





