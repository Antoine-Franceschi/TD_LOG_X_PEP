#site pep
from flask import Flask,render_template,url_for,request, redirect, flash,session
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, FloatField, SelectField, DateField
from datetime import timedelta
from flask_sqlalchemy import SQLAlchemy
import datetime
import sqlite3
import csv

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








############################## page d'acceuil ##########################
@app.route('/home/<name>')
def home(name):
    
    if "name" in session:
        return render_template("Front_pep_copie.html", username=session["name"])
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
        if "name" in session:
            return redirect(url_for("home",name=session["name"]))
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
    con = sqlite3.connect("users_copie.sqlite3")
    outfile = open('bdd_weekly.csv', 'w')
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




if __name__ == "__main__":
    db.create_all()
    app.run()