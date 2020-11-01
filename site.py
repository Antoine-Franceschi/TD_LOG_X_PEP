from flask import Flask,render_template,url_for,request, redirect, flash

app = Flask(__name__, template_folder= "/Users/christinevescovali-franceschi/Desktop/TD-LOG-PEP/FRONT/templates", static_folder= "/Users/christinevescovali-franceschi/Desktop/TD-LOG-PEP/FRONT/static")

Utilisateur=[("antoine@pep.com","pep"),("arnaud@pep.com","pep"),("juliette@pep.com","pep"),("mai-linh@pep.com","pep")]
app.secret_key = '2d9-E2.)f&é,A$p@fpùsgh+dSU03ê9_'

@app.route('/home')
def home():
    return render_template("Front_pep_copie.html")


@app.route('/',methods= ['GET','POST'])
@app.route('/login',methods= ['GET','POST'])
def identification():
    if request.method =="GET":
        return render_template("login_copie.html")
    if request.method == "POST":
        utilisateur = (request.form["_username"], request.form["_password"])
        if utilisateur in Utilisateur:
            return redirect(url_for('home'))
        else:
            flash(u"Erreur d'authentification!")
            return render_template("login_copie.html")


if __name__ == "__main__":

    app.run()