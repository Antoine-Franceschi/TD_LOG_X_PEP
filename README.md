# TD_LOG_X_PEP 2020
Juliette Collin 
Mai-Linh Duong 
Antoine Franceschi
Arnaud Rubin 

##### Objectif

Ce projet a pour but de développer une application web pour la gestion de la Junior Entreprise Ponts Études Projets. Il regroupe plusieurs fonctionnalités essentielles à une bonne gestion de la Junior. 


#### Lancement du site
#         - Execution via docker : 
Aller dans l'Invité de Commande (ou le Terminal) et effectuer les commandes suivantes : 
- "make build" (prend environ 10min)
- "make run" (prend environ 1min)
Le site ne va pas apparaître sur localhost:5000. Il faut aller voir l'adresse IP du host docker(accessible avec `make print_ip`). Remarque : Il est préférable de bind sur http 80/https 443 port au lieu de 5000 pour un usage plus poussé.


#         - Exécution sur python:
Exécuter le fichier `site.py`. Puis se rendre à l'adresse indiquée du type "http://127.0.0.1:5000/".



##### Technologies utilisées
- **front** : `html`, `javascript`, `css`
- **back** :  `python`, `flask`,`sqlite`

##### ##################################### Construction de site.py ####################################

site.py rassemble l'integralité du backend du site web. 

lignes 1-25: Importation de tous les modules 

lignes 25-235: Création de toutes les bases de données. Ces bases de données sont codées en tant que classes. Chaque classe possède ses propres méthodes utiles pour la gestion de la base de données.

lignes 235-253: Création de la page d'acceuil du site web. Cette page est accessible uniquement si l'utilisateur a passé la page de login.

lignes 255-282: Création de la page de login. Dès que l'utilisateur exécute le fichier 'site.py' et qu'il se rend à l'adresse indiquée, il va alors tomber directement sur cette page de login. 

lignes 282-383: Création de la fonctionnalité Trésorerie. Cette page permet l'enregistrement/modification/supression de factures. Elle indique via un code couleur si la facture est arrivée à échéance ou non. 

lignes 383-437: Création de la fonctionnalité weekly. Pendant notre mandat au sein de la Junior Entreprise, nous réalisons régulièrement des réunions pour faire un point sur les différentes études. Pour garder une trace écrite de ces réunions, chaque membre de la Junior Entreprise remplit un tableau indiquant ses avancées et ses projets. La page web que nous avons créé permet à chaque membre de la junior entreprise de remplir un tableau (avec ses projets/ avancées). Nous pouvons télécharger le tableau au format csv. Cela nous permet de garder une trace écrite de ces réunions. 

lignes 437-628: Création de la fonctionnalité agenda. Chaque membre de la Junior Entreprise peut écrire ses rendez-vous client et ses réunions en cliquant simplement sur un jour de la semaine. 

lignes 630-689: Création de la fonctionnalité information personnelle. Chaque membre de la Junior Entreprise peut modifier NOM/adresse mail/mot de passe d'identification. Cette page est la même pour chaque membre de la Junior Entreprise sauf le DSI (Directeur des Systèmes d'Informations). En effet le DSI est la seule personne à avoir accès à l'ensemble des informations des membres de la Junior Entreprise. Le DSI peut ajouter/supprimer des utilisateurs. Il peut aussi nommer une personne au poste de DSI. Il peut y avoir plusieurs personnes DSI. Cependant un DSI ne peut pas s'enlever l'autorisation DSI. Seul un autre DSI peut le faire. Cela permet d'avoir en permanence un DSI qui a accès à toutes les informations. Chaque nouvel utilisateur doit être ajouté par le DSI. 

NB: lorsqu'une personne modifie ses données personnelles celle ci doit automatiquement se re-identifier. 

lignes 689-785: Création de la fonctionnalité 'pep_recrute'. Lorsqu'une entreprise nous demande une mission, nous demandons, via l'envoi d'un mail, à l'ensemble des élèves de 1A/2A/3A s'ils sont interessés par l'étude en question. Cette fonctionnalité "pep_recrute" permet l'envoi de ce mail. Il génère le template en fonction des données entrées et l'envoie à l'adresse spécifiée.

lignes 786-831: Création de la fonctionnalité mail. Cette fonctionnalité permet l'envoi de mails de prospection. Le mail-type est rempli/envoyé automatiquement en fonction des données renseignées dans le formulaire. 

lignes 832-857: Création de la fonctionnalité statistiques. Cette fonctionnalité permet de suivre l'activité de la Junior Entreprise et d'en extraire quelques indicateurs de performance: Nombre de mails envoyés par jour, nombre de mails envoyés par secteur,...







