#site pep
from flask import Flask,render_template,url_for,request, redirect, flash,session
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, FloatField, SelectField, DateField
from datetime import timedelta

app = Flask(__name__)
Utilisateur=[("antoine@pep.com","pep"),("arnaud@pep.com","pep"),("juliette@pep.com","pep"),("mai-linh@pep.com","pep")]
app.secret_key = '2d9-E2.)f&é,A$p@fpùsgh+dSU03ê9_'
app.permanent_session_lifetime = timedelta(minutes=5)
Factures =[[1,2,3,4,5,6,7]]

class factureForm(FlaskForm):
    Numero = StringField("Numero")
    Type = StringField("Type")
    Client = StringField("Client")
    Montant = FloatField("Montant")
    Etat = SelectField("Etat", choices=["Emise","Payé"])
    Date_echeance = DateField("Date d'échéance")
    Date_paiement = StringField("Date de paiement")
    submit= SubmitField("Ajouter Facture")

############################## page d'acceuil ##########################
@app.route('/home/<name>')
def home(name):
    if "utilisateur"in session:
        return render_template("Front_pep_copie.html", username=name)
    else:
        return redirect(url_for('login.copie.html'))


############################## page de login ##########################
@app.route('/',methods= ['GET','POST'])
@app.route('/login',methods= ['GET','POST'])
def identification():
    if request.method =="POST":
        
        session.permanent = True
        utilisateur = (request.form['_username'], request.form['_password'])
        session['utilisateur']=utilisateur[1]

        if utilisateur in Utilisateur:
            return redirect(url_for("home",name=utilisateur[1]))
        else:
            flash(u"Erreur d'authentification!")
            return render_template("login_copie.html")
    else:
        if 'utilisateur'in session:
            name=session['utilisateur']
            return redirect(url_for("home",name=name))
        return render_template("login_copie.html")
        
############################## page trésorerie ##########################
@app.route('/tresorerie/<name>',methods=["GET","POST"])
def index12(name):
    if request.method == "POST":
        Factures.append([request.form['Numero'],request.form['Type'],request.form['Client'],request.form['Montant'],request.form['Etat'],request.form['Date_echeance'],request.form['Date_paiement']])
        print(Factures)
    return render_template('Tresorier.html', name=name, Factures = Factures, template_form=factureForm())





if __name__ == "__main__":

    app.run()