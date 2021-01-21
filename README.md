# TD_LOG_X_PEP 2020
Mai-Linh Duong 
Juliette Collin 
Antoine Franceschi
Arnaud Rubin 

##### Objectif

Ce projet a pour but de développer une application web pour la gestion de la junior entreprise. Il regroupe plusieurs fonctionnalité essentielle à une bonne gestion de la Junior. 


#### Lancement du site
#         - Execution via docker: 
aller dans l'invite de commande (ou le terminal) est effectuer les commandes suivante: 
- "make build" (prend environ 10min)
- "make run" (prend environ 1min)
Le site ne va pas apparaître sur localhost:5000. Il faut aller voir l'ip du host docker(accessible avec `make print_ip`) remarque: Il est préférable de bind sur http 80/https 443 port au lieu de 5000 pour un usage plus poussé


#         - Execution sur python:
Exécuter le fichier `site.py`. Puis se rendre à l'adresse indiquée du type de "http://127.0.0.1:5000/"



##### Technologies utilisées
- **front** : `html`, `javascript`, `css`
- **back** :  `python`, `flask`,`sqlite`

##### ##################################### Construction de site.py ####################################

site.py rassemble l'integralité du backend du site web. 

ligne 1-25: importation de tous les modules 

ligne 25-235: création de toutes les bases de données. Ces bases de données sont codées en tant que classe. Chaque classe possède ses propres méthodes utiles pour la gestion de la base de données.

ligne 235-253: création de la page d'acceuil du site web. cette page est accessible uniquement si l'utilisateur a passé la page de login 

ligne 255-282: création de la page de login. Dès que l'utilisateur exécute le fichier 'site.py' et qu'il se rend à l'adresse indiquée. Il va alors tomber directement sur cette page de login. 

ligne 282-383: création de la fonctionnalité trésorerie. Cette page permet l'enregistrement/modification/supression de factures. Elle indique via un code couleur si la facture est arrivée à echéance ou non. 

ligne 383-437: création de la fonctionnalité weekly. Pendant notre mandat au sein de la junior entreprise, nous réalisons régulierement des réunions pour faire un point sur les différentes études. Pour garder une trace écrite de ces réunions, chaque membre de la junior entreprise rempli un tableau indiquant ses avancées et ses projets. La page web que nous avons créé permet à chaque membre de la junior entreprise de remplir un tableau (avec ses projets/ avancées). Nous pouvons télécharger le tableau au format csv. Cela nous permet de garder une trace écrite de ces réunions. 

ligne 437-628: création de la fonctionnalité agenda. Chaque membre de la junior entreprise peut écrire ses rendez-vous client/réunion en cliquant simplement sur un jour de la semaine. 

ligne 630-689: création de la fonctionnalité information personnelle. Chaque membre de la junior entreprise peut modifier NOM/adresse mail/mot de passe d'identification. Cette page est la même pour chaque membre de la junior entreprise sauf le DSI (directeur des systèmes informatiques). En effet le DSI est la seul personne à avoir accès à l'ensemble des informations des membres de la junior entreprise. Le DSI peut ajouter/supprimer des utilisateurs. Il peut aussi nomer une personne DSI. Il peut y avoir plusieurs personne DSI. Cependant un DSI ne peut pas s'enlever l'autorisation DSI. Seul un autre DSI peut le faire. Cela permet d'avoir en permanence un DSI qui a accès à toutes les informations. Chaque nouvel utilisateur doit être rajouté par le DSI. 

NB: lorsqu'une personne modifie ses données personnelles celle ci doit automatiquement se re-identifier. 

ligne 689-785: création de la fonctionnalité 'pep_recrute'. Lorsqu'une entreprise nous demande une mission, nous demandons, via l'envoi d'un mail, à l'ensemble des élèves de 1A/2A/3A s'ils sont interessés par l'étude en question. Cette fonctionnalité "pep_recrute" permet l'envoi de ce mail. Il génère le template en fonction des données entrées et l'envoie à l'adresse spécifiée.

ligne 786-831: création de la fonctionnalité mail. Cette fonctionnalité permet l'envoi de mails de prospection. Le mail-type est rempli/envoyé automatiquement en fonction des données renseignées dans le formulaire. 

ligne 832-857: création de la fonctionnalité statistique. Cette fonctionnalité permet de suivre l'activité de la junior entreprise et d'en extraire quelques indicateurs de performance: Nombre de mail envoyé par jour, nombre de mail envoyé par secteur,...







