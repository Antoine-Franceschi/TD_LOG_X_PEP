from flask import Flask, render_template, request
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, FloatField, SelectField, DateField

app = Flask(__name__, template_folder= "/Users/christinevescovali-franceschi/Documents/Projet_TD_LOG/TD_LOG_X_PEP/templates", static_folder= "/Users/christinevescovali-franceschi/Documents/Projet_TD_LOG/TD_LOG_X_PEP/static")
app.config['SECRET_KEY']= 'secretkey'

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

@app.route('/',methods=["GET","POST"])
def index12():
    if request.method == "POST":
        Factures.append([request.form['Numero'],request.form['Type'],request.form['Client'],request.form['Montant'],request.form['Etat'],request.form['Date_echeance'],request.form['Date_paiement']])
        print(Factures)
    return render_template('Tresorier.html', Factures = Factures, template_form=factureForm())


if __name__ == "__main__":
    app.run()