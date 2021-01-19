#site pep
from flask import Flask,render_template,url_for,request, redirect, flash,session
from wtforms import StringField, SubmitField, FloatField, SelectField, DateField
from datetime import timedelta
from flask_sqlalchemy import SQLAlchemy
import datetime
import sqlite3
import csv
import calendar
import os
import json

app = Flask(__name__)
app.config['STATIC_AUTO_RELOAD'] = True
app.config['TEMPLATES_AUTO_RELOAD' ] = True
app.secret_key = '2d9-E2.)f&é,A$p@fpùsgh+dSU03ê9_'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.sqlite3'
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"]=False
app.permanent_session_lifetime = timedelta(minutes=5)

db= SQLAlchemy(app)

class db_utilisateurs(db.Model):
    _id = db.Column("id", db.Integer, primary_key= True)
    name = db.Column(db.String(100))
    email = db.Column(db.String(100))
    mdp = db.Column(db.String(100))
    dsi = db.Column(db.Boolean)

    def __init__(self, name, email, mdp):
        self.name = name
        self.email = email 
        self.mdp = mdp


class db_factures(db.Model):
    _id = db.Column("id", db.Integer, primary_key= True)
    numero = db.Column(db.String(100))
    Type = db.Column(db.String(100))
    client = db.Column(db.String(100))
    montant= db.Column(db.Float)
    etat = db.Column(db.String(100))
    date_echeance = db.Column(db.String(100))
    date_paiement = db.Column(db.String(100))
    suiveur = db.Column(db.String(100))
    retard = db.Column(db.Boolean)
    def __init__(self, numero, Type, client,montant, etat, date_echeance, date_paiement, suiveur): 
        self.numero= numero 
        self.Type = Type 
        self.client = client 
        self.montant = montant 
        self.etat = etat 
        self.date_paiement= date_paiement
        self.date_echeance = date_echeance
        self.suiveur = suiveur

class db_weekly(db.Model):
    _id = db.Column("id", db.Integer, primary_key= True)
    name = db.Column(db.String(100))
    projet = db.Column(db.String(300))
    action = db.Column(db.String(300))
    echeance = db.Column(db.String(100))
    avancement = db.Column(db.String(100))
    travail_pep = db.Column(db.Integer)
    travail_gene = db.Column(db.Integer)
    prospection = db.Column(db.String(100))
    def __init__(self,name, projet, action, echeance, avancement, travail_pep, travail_gene,prospection):
        self.name= name
        self.projet = projet
        self.action = action 
        self.avancement = avancement
        self.echeance = echeance
        self.travail_pep = travail_pep
        self.travail_gene = travail_gene
        self.prospection = prospection

class db_pep_recrute(db.Model):
    _id = db.Column("id", db.Integer, primary_key= True)
    suiveur = db.Column(db.String(100))
    departement = db.Column(db.String(100))
    destinataire = db.Column(db.String(100))
    titre = db.Column(db.String(150))
    prix = db.Column(db.Integer)
    client = db.Column(db.String(100))
    corps_mail = db.Column(db.String(10000))

    def __init__(self, suiveur, departement, destinataire, titre, prix, client, corps_mail): 
        self.suiveur= suiveur 
        self.departement = departement 
        self.destinataire = destinataire 
        self.titre = titre 
        self.prix = prix 
        self.client = client
        self.corps_mail = corps_mail

class db_prospection(db.Model):
    _id = db.Column("id", db.Integer, primary_key= True)
    suiveur = db.Column(db.String(100))
    client_sexe = db.Column(db.String(100))
    client_nom = db.Column(db.String(100))
    client_prenom = db.Column(db.String(100))
    client_entreprise = db.Column(db.String(100))
    client_secteur= db.Column(db.String(100))
    client_poste = db.Column(db.String(100))
    client_promo = db.Column(db.Integer)
    client_telephone = db.Column(db.String(100))
    client_mail = db.Column(db.String(100))
    mode_contact = db.Column(db.String(100))
    date_envoi = db.Column(db.String(100))
    ancien_ponts = db.Column(db.Boolean)
    reponse = db.Column(db.Boolean)
    date_relance = db.Column(db.String(100))

    def __init__(self, suiveur, client_sexe, client_nom, client_prenom, client_entreprise, client_secteur,  client_poste, client_promo, client_telephone, client_mail, mode_contact, date_envoi, ancien_ponts, reponse, date_relance):
        self.suiveur = suiveur
        self.client_sexe = client_sexe
        self.client_nom = client_nom
        self.client_prenom = client_prenom
        self.client_entreprise = client_entreprise
        self.client_secteur=client_secteur
        self.client_poste = client_poste
        self.client_promo = client_promo
        self.client_telephone = client_telephone
        self.client_mail = client_mail
        self.mode_contact = mode_contact
        self.date_envoi = date_envoi
        self.ancien_ponts = ancien_ponts
        self.reponse = reponse
        self.date_relance = date_relance


    #fonctions pour les stats
    def annees_du_mandat(self):
        month=datetime.datetime.now().month
        year= datetime.datetime.now().year
        #on cherche ou on se situe dans le mandat pour prendre les mails du bon mandat
        #soit on est encore dans la partir mai-décembre (donc on n'a pas changé d'année)
        if month>=5:
            annee_debut_mandat=year
            annee_fin_mandat=year+1
        #soit on est dans la partie janvier_avril, donc on doit actualisé l'année en fonction de l'année actuelle
        if month<5:
            annee_debut_mandat=year-1
            annee_fin_mandat=year
        return annee_debut_mandat, annee_fin_mandat
    
    def mail_dans_le_mandat(self, mail):
        date= mail.date_envoi
        annee_mail= int(date[6:])
        mois_mail=int(date[3:5])
        annee_debut_mandat, annee_fin_mandat = self.annees_du_mandat(self)
        #on prend les mails depuis mai de debut de mandat jusque avril fin mandat (année d'après)
        if ( mois_mail>=5  and annee_mail== annee_debut_mandat) or (mois_mail<5 and annee_mail==annee_fin_mandat):
            return True
        else:
            return False

    def classement_prospecteur(self):
        mails_par_prospecteur=[]
        prospecteurs=[]
    
        for mail in self.query.all():
            if self.mail_dans_le_mandat(self, mail):     #erreur too many argument mais ca marche quand meme
                if mail.suiveur in prospecteurs:
                    indice=prospecteurs.index(mail.suiveur)
                    mails_par_prospecteur[indice]+= 1
                else:
                    prospecteurs.append(mail.suiveur)
                    mails_par_prospecteur.append(1)
        return mails_par_prospecteur, prospecteurs

    def mails_secteur(self, pourcentage=False):
        mails_par_secteur=[]
        secteur=[]
        nb=0
        for mail in self.query.all():
            if self.mail_dans_le_mandat(self, mail):
                nb+=1
                if mail.client_secteur in secteur:
                    indice=secteur.index(mail.client_secteur)
                    mails_par_secteur[indice]+= 1
                else:
                    secteur.append(mail.client_secteur)
                    mails_par_secteur.append(1)

        if pourcentage:
            for i in range(len(mails_par_secteur)):
                if nb!=0:
                    mails_par_secteur[i]= int(mails_par_secteur[i]*10000/nb)/100


        return mails_par_secteur, secteur

    #pourcentage des mails envoyés et réponses recues en fonction du jour de l'envoi du mail
    def envois_reponses_jour_semaine(self, pourcentage=False):
        #on commence par compter le nombre de mails
        nb=0
     
        jours=['Lundi', 'Mardi', 'Mercredi', 'Jeudi', 'Vendredi', 'Samedi', 'Dimanche']
        nombre_mails_jours=[0]*7
        reponses_jours= [0]*7
        for mail in self.query.all():
            if self.mail_dans_le_mandat(self, mail):
                nb+=1
       
                #forme de la date "YYYY-MM-DD"
                isodate= mail.date_envoi[6:]+ "-" + mail.date_envoi[3:5] +"-" + mail.date_envoi[0:2]
                jour_semaine=datetime.datetime.fromisoformat(isodate).isocalendar()[2] #ca prend le jour de la semaine associé a la date
                nombre_mails_jours[jour_semaine-1]+=1
                reponses_jours[jour_semaine-1]+=int(mail.reponse)
        if pourcentage: 
            for i in range (len(nombre_mails_jours)):
                if nombre_mails_jours[i]!=0:
                    reponses_jours[i]/= nombre_mails_jours[i]
                if nb!=0:
                    nombre_mails_jours[i]/=nb
                nombre_mails_jours[i]=int( nombre_mails_jours[i]*10000)/100 #pour avoir un pourcentage tronqué
                
                reponses_jours[i]=int(reponses_jours[i]*10000)/100 #pareil

        return jours, nombre_mails_jours, reponses_jours




        




############################## page d'acceuil ##########################
@app.route('/home/<name>')
def home(name):
    
    if "name" in session:
        return render_template("Front_pep_copie.html", username=session["name"], this_week=int(datetime.datetime.now().isocalendar()[1])+1)
    else:
        return redirect(url_for('identification'))


############################## page de login ##########################
@app.route('/',methods= ['GET','POST'])
@app.route('/login',methods= ['GET','POST'])
def identification():
    if request.method =="POST":

        session.permanent = True
        
        utilisateur = (request.form['_username'], request.form['_password'])
        found_utilisateur = db_utilisateurs.query.filter_by(email=utilisateur[0], mdp=utilisateur[1]).first()
        
        if found_utilisateur:
            session["name"]=found_utilisateur.name
            return redirect(url_for("home",name=found_utilisateur.name))

        else:
            flash(u"Erreur d'authentification!")
            return render_template("login_copie.html")
    else:
        #if "name" in session:
         #   return redirect(url_for("home",name=session["name"]))
            
        return render_template("login_copie.html")

@app.route('/logout')
def logout():
    session.pop('name', None)
    return redirect(url_for('identification'))
        
############################## page trésorerie ##########################
@app.route('/tresorerie/<name>',methods=["GET","POST"])
def index12(name):
    init_bd()
    
    return render_template('Tresorier.html', name=name, BDD_facture = db_factures.query.all())

def init_bd():
    
    for facture in db_factures.query.all():
        retard1 = init_retard(facture.date_echeance)
        facture.retard = retard1
        db.session.commit()
        

def init_retard(date):
    now = datetime.datetime.now()
    date_now = now.year*10000+now.month*100+now.day
    if int(date[0:2])<10:
        taille_date=1
    else:
        taille_date=2
    date_converti = int(date[0:2])
    month = date[taille_date+1:taille_date+4]
    year = int(date[taille_date+5::])
    L=['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec']
    for k in range(len(L)):
        if month == L[k]:
            date_converti+=(k+1)*100

    date_converti += year*10000
    if date_converti<=date_now:
        return True
        #je  suis  en retard
    #sinon je  ne suis pas   en retard
    return False


@app.route('/tresoreie/<name>/add_delete', methods=["GET","POST"])
def add(name):
    if request.method == "POST":
        date_echeance = str(request.form['_date_j']) + ' ' + str(request.form['_date_m']) + ' ' + str(request.form['_date_y'])
        date_paiement = str(request.form['_date_j_p']) + ' ' + str(request.form['_date_m_p']) + ' ' + str(request.form['_date_y_p'])
        facture= db_factures(request.form['_numero'],request.form['_type'],request.form['_client'],request.form['_montant'],request.form['_etat'],date_echeance, date_paiement, request.form['_suiveur'])
        db.session.add(facture)
        db.session.commit()
        
        
        
        return redirect(url_for('index12', name= name))
    return render_template('add_delete.html',name=name)

@app.route('/tresoreie/<name>/<int:id>/modify', methods=["GET","POST"])
def modify(name,id):
    facture = db_factures.query.get(id)
    date= facture.date_echeance
    if int(date[0:2])<10:
        taille_date=1
    else:
        taille_date=2
    jour_e = date[0:2]
    mois_e = date[taille_date+1:taille_date+4]
    annee_e = date[taille_date+5::]

    date= facture.date_paiement
    if "-" not in date:
        if int(date[0:2])<10:
            taille_date=1

        else:
            taille_date=2
        jour_p = date[0:2]
        mois_p = date[taille_date+1:taille_date+4]
        annee_p = date[taille_date+5::]
    else: 
        jour_p= "-"
        mois_p= "-"
        annee_p= "-"
    if request.method == "POST":
        date_echeance = str(request.form['_date_j']) + ' ' + str(request.form['_date_m']) + ' ' + str(request.form['_date_y'])
        date_paiement = str(request.form['_date_j_p']) + ' ' + str(request.form['_date_m_p']) + ' ' + str(request.form['_date_y_p'])
        
        facture.numero = request.form['_numero']
        facture.Type = request.form['_type']
        facture.client = request.form['_client']
        facture.montant = request.form['_montant']
        facture.etat = request.form['_etat']
        facture.date_paiement = date_paiement
        facture.date_echeance = date_echeance
        facture.suiveur = request.form['_suiveur']
        db.session.commit()
        return redirect(url_for('index12', name= name))
    return render_template('delete.html',name=name,facture=facture, jour_e=jour_e, mois_e=mois_e,annee_e=annee_e,jour_p=jour_p,mois_p=mois_p, annee_p=annee_p)

@app.route('/tresoreie/<name>/<int:id>/delete',methods=["GET","POST"])
def delete(name,id):
    delete= db_factures.query.filter_by(_id=id).first()
    db.session.delete(delete)
    db.session.commit()
    return redirect(url_for('index12', name= name))

#################### Weekly ##################################

@app.route('/weekly/<name>',methods=["GET","POST"])
def weekly(name):
    if True:

        con = sqlite3.connect("users.sqlite3")
        script_dir = os.path.dirname(__file__)
        rel_path = "/static/bdd_weekly1.csv'"
        abs_file_path = os.path.join(script_dir, rel_path)
        outfile = open("static/bdd_weekly.csv", 'w')
        
        outcsv = csv.writer(outfile)
        cursor = con.execute('select * from db_weekly')
        #dump column titles (optional)
        outcsv.writerow(x[0] for x in cursor.description)
        # dump rows
        outcsv.writerows(cursor.fetchall())
        outfile.close()
    return render_template("tableau_weekly-2.html", name=name, BDD_commentaire=db_weekly.query.all())

@app.route('/weekly/<name>/add',methods=["GET","POST"])
def add_commentaire(name):
    if request.method == "POST":
        
        commentaire= db_weekly(request.form['name'],request.form['projet'],request.form['action'],request.form['echeance'],request.form['avancement'],request.form['travail_pep'],request.form['travail_gene'],request.form['prospection'])
        db.session.add(commentaire)
        db.session.commit()
        return redirect(url_for('weekly', name= name))
    return render_template("weekly.html", name=name, BDD_utilisateur=db_utilisateurs.query.all())

@app.route('/weekly/<name>/<int:id>/modify_delete',methods=["GET","POST"])
def modify_weekly(name,id):
    commentaire = db_weekly.query.get(id)
    if request.method == "POST":
        commentaire.name = request.form['name']
        commentaire.projet = request.form['projet']
        commentaire.action = request.form['action']
        commentaire.avancement = request.form['echeance']
        commentaire.echeance = request.form['avancement']
        commentaire.prospection = request.form['prospection']
        commentaire.travail_pep = request.form['travail_pep']
        commentaire.travail_gene = request.form['travail_gene']
        db.session.commit()
        return redirect(url_for('weekly', name= name))
    return render_template("weekly_add_delete.html",name=name,commentaire=commentaire)

@app.route('/weekly/<name>/<int:id>/delete',methods=["GET","POST"])
def delete_weekly(name,id):
    delete= db_weekly.query.filter_by(_id=id).first()
    db.session.delete(delete)
    db.session.commit()
    return redirect(url_for('weekly', name= name))

####################" page agenda"############################################

class db_event(db.Model):
    _id=db.Column("id",db.Integer, primary_key=True)
    week = db.Column(db.Integer)
    day= db.Column(db.Integer)
    title=db.Column(db.String(200))
    debut = db.Column(db.String(20))
    fin= db.Column(db.String(20))
    heure_debut=db.Column(db.Float)
    heure_fin=db.Column(db.Float)
    duree=db.Column(db.Integer)

    def __init__(self, week, day, title, debut, fin, heure_debut, heure_fin, duree):
        self.week=week
        self.day=day
        self.title=title
        self.debut=debut
        self.fin=fin
        self.heure_debut=heure_debut
        self.heure_fin=heure_fin
        self.duree=duree
        
    def count(self, week):
        Nombre_evenements=[[0 for _ in range(7)] for _ in range(13*4)]
        evenement_week= self.query.filter_by(week=week) 
        for evenement in evenement_week:
            minutes_deb= (evenement.heure_debut-int(evenement.heure_debut))
            minutes_fin=(evenement.heure_fin-int(evenement.heure_fin))
            case_debut= int((int(evenement.heure_debut)-8)*4 + minutes_deb/0.25)
            case_fin= int((int(evenement.heure_fin)-8)*4+ minutes_fin/0.25)
            if minutes_fin==0 or minutes_fin==0.25 or minutes_fin==0.5 or minutes_fin==0.75:
                case_fin-=1
            for i in range (case_debut, case_fin+1):
                Nombre_evenements[i][evenement.day-1]+=1
        return Nombre_evenements

days=[1,2,3,4,5,6,7]
time=[8]
p=800

for k in range (0, 51):
    p+=25
    if p%100==0:
          time.append(int(p/100))
    else:
        time.append(p/100)


@app.route('/agenda/<name>/<week>/', methods=['POST', 'GET'])
def agenda(name, week):
    init_event_db()
    premier_jour, mois_premier_jour, annee_premier_jour, dernier_jour, mois_dernier_jour, annee_dernier_jour = info_week(week)
    init_event_db()
    previous_week=str((int(week)-1)%52)
    if previous_week=="0":
        previous_week="52"
    next_week=str((int(week)+1)%52)
    if next_week=="0":
        next_week="52"
    if request.method=="POST":
        title=request.form["event"]
        debut=request.form["horrairedeb"]
        fin=request.form["horrairefin"]
        day=request.form["day"]
        found_event= db_event.query.filter_by(day= day, week=int(week), title=title, debut=debut, fin=fin).first()
        if found_event:
            flash(u"Evènement déjà prévu!")
            return redirect(url_for("agenda", name=name, week=int(week)))
        if (debut[3:]!="00" and debut[3:]!="15" and  debut[3:]!="30" and  debut[3:]!="45" ) or (fin[3:]!="00" and fin[3:]!="15" and fin[3:]!="30" and fin[3:]!="45" ):
            flash(u"Format d'horraire incorrect")
            flash(u"Essayez avec des minutes du type \"00\",\"15\",\"30\" ou \"45\" ")
            return redirect(url_for("agenda", name=name, week=int(week)))
        else:
            heure_debut=(float_horaire(debut))
            heure_fin=(float_horaire(fin))
            duree= nombre_cases(heure_debut, heure_fin)
            evnt=db_event(week, day, title, debut, fin, heure_debut, heure_fin, duree)
            db.session.add(evnt)
            db.session.commit()
    return render_template("agenda.html", name=name, week=int(week), premier_jour=premier_jour, mois_premier_jour=nom_du_mois(mois_premier_jour), annee_premier_jour=annee_premier_jour, dernier_jour=dernier_jour, mois_dernier_jour=nom_du_mois(mois_dernier_jour), annee_dernier_jour=annee_dernier_jour, evenement=db_event.query.all() , previous_week=previous_week, next_week=next_week, Nombre_evenements=db_event.count(db_event, week=week), days=days, time=time)




def init_event_db():
    for _ in db_event.query.all():
        db.session.commit()

def info_week(w):
    w=int(w)
    ajd = datetime.datetime.now()
    cal = calendar.TextCalendar(firstweekday=0)
    calendrier = cal.yeardatescalendar(ajd.year, 1)
    year=[]
    for cal in calendrier:
        for month in cal:
            for week in month:
                if not inside(year, week):
                    year.append(week)
    premier_jour= year[w-1][0]
    dernier_jour= year[w-1][6]
    return (premier_jour.day, premier_jour.month, premier_jour.year , dernier_jour.day, dernier_jour.month, dernier_jour.year)

def inside(L,x):
    for element in L:
        if element==x:
            return True
    return False


"""
def actualise_semaine():
    date= datetime.datetime.now()
    week= date.isocalendar()[1]
    mois=date.month
    premier_jour=date.day - date.isoweekday() +1
    dernier_jour=date.day + (7-date.isoweekday())
    annee=date.year
    mois_premier_jour=mois
    mois_dernier_jour=mois
    annee_premier_jour=date.year
    annee_dernier_jour=date.year


    if date.day==31 and mois==12:
        annee_dernier_jour=annee+1
    if date.day==1 and mois==1:
        annee_premier_jour=annee-1
    if date.day==1:
        premier_jour= calendar.mdays[mois-1] - date.isoweekday()
        mois_premier_jour-=1
    elif date.day==calendar.mdays[mois]:
        dernier_jour=7-date.isoweekday()
        mois_dernier_jour+=1
        
    return (week, premier_jour, mois_premier_jour, annee_premier_jour, dernier_jour, mois_dernier_jour, annee_dernier_jour)

    """

def nom_du_mois(numero):
    if numero==1:
        return "Janvier"
    elif numero==2:
        return "Février"
    elif numero==3:
        return "Mars"
    elif numero==4:
        return "Avril"
    elif numero==5:
        return "Mai"
    elif numero==6:
        return "Juin"
    elif numero==7:
        return "Juillet"
    elif numero==8:
        return "Août"
    elif numero==9:
        return "Septembre"
    elif numero==10:
        return "Octobre"
    elif numero==11:
        return "Novembre"
    elif numero==12:
        return "Décembre"

def float_horaire(horaire):
    heure=int(horaire[:2])
    minutes=int(horaire[3:])
    heure+=minutes/60
    return heure

def nombre_cases(heure_debut, heure_fin):
    minutes_deb= (heure_debut-int(heure_debut))
    minutes_fin=(heure_fin-int(heure_fin))
    case_debut= int((int(heure_debut)-8)*4 + minutes_deb/0.25)
    case_fin= int((int(heure_fin)-8)*4+ minutes_fin/0.25)
    if minutes_fin==0 or minutes_fin==0.25 or minutes_fin==0.5 or minutes_fin==0.75:
            case_fin-=1
    return case_fin-case_debut +1



@app.route('/agenda/<name>/<week>/<int:id>/', methods=["POST", "GET"])
def supprimer(name, week, id):
   
    supp= db_event.query.filter_by(_id=id).first()
    db.session.delete(supp)
    db.session.commit()
    return redirect(url_for('agenda', name=name, week=week))

##################### page information #####################

@app.route('/information/<name>',methods=["POST", "GET"])

def information(name):
    utilisateur = db_utilisateurs.query.filter_by(name=name).first()
    utilisateur_name=utilisateur.name
    if request.method == "POST":
        utilisateur.name = request.form['_name']
        utilisateur.email = request.form['_mail']
        utilisateur.mdp = request.form['_mdp']
        db.session.commit()
        if utilisateur_name==utilisateur.name:
            flash(u"Données sauvegardées")
            return redirect(url_for('information', name= name))
        else:
            return redirect(url_for("logout"))
    
    utilisateur_name=utilisateur.name
    mail = utilisateur.email
    dsi = utilisateur.dsi
    mdp = utilisateur.mdp
    
    print(mail)
    return render_template("information.html",name=name,utilisateur_name=utilisateur_name,mdp=mdp,mail=mail,dsi=dsi, BDD_utilisateur=db_utilisateurs.query.all()) 

@app.route('/add_delete_information/<name>/<int:id>',methods=["POST", "GET"])
def add_delete_information(name,id):
    utilisateur= db_utilisateurs.query.filter_by(_id=id).first()
    utilisateur_name=utilisateur.name
    
    if request.method == "POST":
        utilisateur.name = request.form['_name_']
        utilisateur.email = request.form['_mail']
        utilisateur.mdp = request.form['_mdp']
        if name!=utilisateur_name:
            if request.form['_dsi']=='True':
                utilisateur.dsi = 1
            if request.form['_dsi']=='False':
                utilisateur.dsi = 0
        
        db.session.commit()
        if utilisateur_name==utilisateur.name:
            return redirect(url_for('information', name= name))
        else:
            return redirect(url_for("logout"))
    
    utilisateur_name=utilisateur.name
    mdp=utilisateur.mdp
    mail=utilisateur.email
    dsi =utilisateur.dsi
    return render_template("add_delete_information.html",name=name,_name=utilisateur_name,mdp=mdp,mail=mail,dsi=dsi, utilisateur=utilisateur)

@app.route('/information/<name>/<int:id>/delete',methods=["GET","POST"])
def delete_information(name,id):
    delete= db_utilisateurs.query.filter_by(_id=id).first()
    db.session.delete(delete)
    db.session.commit()
    return redirect(url_for('information', name= name))


##################### page pep recrute #####################
@app.route('/pep_recrute/<name>',methods=["GET","POST"])
def page_pep_recrute(name):
    return(render_template("pep_recrute.html", name=name))

def envoi_mail(mail_expediteur, expediteur_mdp, mail_destinataire, sujet, corps_mail, piece_jointe_nom, piece_jointe_chemin, template_chemin):
    Fromadd = mail_expediteur # sous la forme d'une chaine de caractère
    Toadd = mail_destinataire # sous la forme d'une chaine de caractère

    message = MIMEMultipart()    # Création de l'objet "message"
    message['From'] = Fromadd
    message['To'] = Toadd
    message['Subject'] = sujet # Objet du mail (pour les PEP recrute : "Ponts Etudes Projets - Junior Entreprise")
    msg = corps_mail # Message à envoyer

    message.attach(MIMEText(msg.encode('utf-8'), 'plain', 'utf-8'))    # Attache du message à l'objet "message", et encodage en UTF-8

    nom_fichier = piece_jointe_nom # Spécification du nom de la pièce jointe
    piece = open(piece_jointe_chemin, "rb") # Ouverture du fichier
    part = MIMEBase('application', 'octet-stream') # Encodage de la pièce jointe en Base64
    part.set_payload((piece).read())
    encoders.encode_base64(part)
    part.add_header('Content-Disposition', "piece; filename= %s" % nom_fichier)
    message.attach(part) # Attache de la pièce jointe à l'objet "message" 

    f = open(template_chemin)

    html = f.read()
    part2 = MIMEText(html, 'html')
    message.attach(part2)

    serveur = smtplib.SMTP('smtp.gmail.com', 587) # Connexion au serveur sortant (en précisant son nom et son port)
    serveur.starttls() # Spécification de la sécurisation
    serveur.login(Fromadd, expediteur_mdp) # Authentification
    texte= message.as_string().encode('utf-8') # Conversion de l'objet "message" en chaine de caractère et encodage en UTF-8
    serveur.sendmail(Fromadd, Toadd, texte) # Envoi du mail
    serveur.quit() # Déconnexion du serveur
    return 0

##################### page prospection #####################
@app.route('/prospection/<name>',methods=["GET","POST"])

def page_prospection(name):
    return(render_template("Email_front.html", name=name))

#################### statistiques ################################"

def liste_en_string(L):
    chaine="["
    for element in L[:len(L)-1]:
        chaine+="\'"+ str(element)+ "\'" + ","
    chaine+="\'" + str(L[len(L)-1]) + "\'"+"]"
    return chaine

@app.route('/statistiques/<name>')
def statistiques(name):
   
    classement_prospecteurs,  prospecteurs= db_prospection.classement_prospecteur(db_prospection)
    classement_prospecteurs.sort(reverse= True)


    mails_par_secteur , secteurs = db_prospection.mails_secteur(db_prospection)
    pourcentage_mails_par_secteur, secteurs= db_prospection.mails_secteur(db_prospection, True)
  

    jours, nombre_mails_jours, reponses_jours= db_prospection.envois_reponses_jour_semaine(db_prospection)
    jours, pourcentage_mails_jours, pourcentage_reponses_jours=db_prospection.envois_reponses_jour_semaine(db_prospection, True)

    
    return render_template('Statistiques.html', name=name, prospecteurs=prospecteurs, classement_prospecteurs=classement_prospecteurs, secteurs=secteurs, mails_par_secteur=mails_par_secteur, pourcentage_mails_par_secteur=pourcentage_mails_par_secteur,  jours=jours, nombre_mails_jours=nombre_mails_jours, pourcentage_mails_jours=pourcentage_mails_jours,  reponses_jours=reponses_jours, pourcentage_reponses_jours= pourcentage_reponses_jours, nombre_prospecteurs=len(prospecteurs) ,nombre_secteurs=len(secteurs))
    
if __name__ == "__main__":
    db.create_all()
    app.run(debug=True)