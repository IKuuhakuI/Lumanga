from flask import Flask, render_template, request, redirect, url_for, session, flash
from datetime import timedelta
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.secret_key = "teste"

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.sqlite3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

app.permanent_session_lifetime = timedelta(minutes=30)

db = SQLAlchemy(app)

class Users (db.Model):
	_id = db.Column ("id", db.Integer, primary_key=True)
	name = db.Column ("name", db.String (100))
	email = db.Column ("email", db.String (100), primary_key=True)
	password = db.Column ("password", db.String (60))

	def __init__ (self, name, email, password):
		self.name = name
		self.email = email
		self.password = password
		

def checarTipoLogin():
	if (session.get("logged_in") == None):
		return False

	elif (session["logged_in"]):
		return True
	return False

@app.route ("/")
def inicial ():
	return render_template ("inicio.html", logado=checarTipoLogin())

@app.route("/entrar", methods=["POST", "GET"])
def entrar():
	if request.method == "POST":
		session.permanent = True
		userEmail = request.form ["email"]
		session["email"] = userEmail

		flash ("Entrou", "info")

		return redirect (url_for ("user"))

	else:
		if "email" in session:
			flash ("Ja esta logado")
			return redirect(url_for("user"))
		return render_template ("entrar.html", logado=checarTipoLogin())

@app.route("/user")
def user ():

	flash ("Exame 'X' pendente!")
	if "email" in session:
		logado = True
		email = session["email"]
		session['logged_in'] = True

		return render_template("perfil.html", user=email, logado=checarTipoLogin())

	else:
		return redirect (url_for ("entrar"))

@app.route("/consultas")
def consultas():
	return render_template ("consultas.html", logado=checarTipoLogin())

@app.route("/eventos")
def eventos():
	return render_template ("eventos.html", logado=checarTipoLogin())

@app.route("/videos")
def videos():
	return render_template ("videos.html", logado=checarTipoLogin())

@app.route("/agendar")
def agendar():
	return render_template ("agendar.html", logado=checarTipoLogin())

@app.route("/sair")
def logout():
	if "email" in session:
		user = session["email"]
		flash (f"{user}, saiu", "info")
	
	session['logged_in']=False
	session.pop("email", None)


	return redirect( url_for ("inicial"))

@app.route("/registrar", methods=["POST", "GET"])
def registrar():
	valNome = ""

	if request.method == "POST":
		# session.permanent = True
		# userEmail = request.form ["email"]
		# session["email"] = userEmail

		dataName = request.form.get('name', valNome)
		dataEmail = request.form.get('email', valNome)
		dataPass = request.form.get('password', valNome)
		dataConfirm = request.form.get('confirmPassword', valNome)

		if dataPass == dataConfirm:
			flash ("True")

			session.permanent = True
		else:
			flash ("False")

		return redirect (url_for ("user"))


	

	return render_template ("registrar.html", logado=checarTipoLogin())
	'''
	user = User (name=..., email=..., password=...)
	return render_template ("registrar.html", logado=checarTipoLogin())
	'''
if __name__ == "__main__":
	app.run (debug=True)