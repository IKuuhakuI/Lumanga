from flask import Flask, render_template, request, redirect, url_for, session, flash
from datetime import timedelta
from flask_sqlalchemy import SQLAlchemy

# Inicia o app
app = Flask(__name__)
app.secret_key = "teste"

# Conexao com o banco de dados
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.sqlite3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Deixa o User conectado por 30 minutos
app.permanent_session_lifetime = timedelta(minutes=30)

db = SQLAlchemy(app)

# Classe para usuario do db
class Users (db.Model):
	# Colunas
	_id = db.Column (db.Integer, primary_key=True)
	name = db.Column ("name", db.String (100))
	email = db.Column ("email", db.String (100), unique=True)
	password = db.Column ("password", db.String (60))

	def __init__ (self, name, email, password):
		self.name = name
		self.email = email
		self.password = password

db.create_all()

# Checa se o user esta logado
def checarTipoLogin():
	if (session.get("logged_in") == None):
		return False

	elif (session["logged_in"]):
		return True
	return False

# Pagina Inicial
@app.route ("/")
def inicial ():
	# Caso logado
	if "email" in session:
		logado = True
		email = session["email"]
		session['logged_in'] = True

	return render_template ("inicio.html", logado=checarTipoLogin())

# Pagina de Login
@app.route("/entrar", methods=["POST", "GET"])
def entrar():
	if request.method == "POST":

		userEmail = request.form ["email"]
		userPass = request.form ["password"]

		usuario = Users.query.filter_by(email=userEmail).first()

		# Caso usuario exista
		if (usuario):
			# Senha valida
			if usuario.password == userPass:
				session.permanent = True
				session["email"] = userEmail

				return redirect (url_for ("inicial"))

			else:
				flash ("Senha incorreta", "warning")

		# Caso nao exista
		else:
			flash ("User nao existe", "warning")

		return redirect (url_for ("entrar"))
		

	else:
		# Caso ja esteja logado
		if "email" in session:
			flash ("Ja esta logado")
			return redirect(url_for("user"))
		return render_template ("entrar.html", logado=checarTipoLogin())

# Pagina de usuario
@app.route("/user")
def user ():
	flash ("Consulta 'X' pendente!")
	return render_template("perfil.html", logado=checarTipoLogin())

# Pagina de consultas
@app.route("/consultas")
def consultas():
	return render_template ("consultas.html", logado=checarTipoLogin())

# Pagina de eventos
@app.route("/eventos")
def eventos():
	return render_template ("eventos.html", logado=checarTipoLogin())

# Pagina de videos
@app.route("/videos")
def videos():
	return render_template ("videos.html", logado=checarTipoLogin())

# Pagina agendar
@app.route("/agendar")
def agendar():
	return render_template ("agendar.html", logado=checarTipoLogin())

# Sair do usuario
@app.route("/sair")
def logout():
	# Caso esteja logado
	if "email" in session:
		user = session["email"]
		flash (f"{user}, saiu", "info")
	
	# Desconecta o usuario
	session['logged_in']=False
	session.pop("email", None)


	return redirect( url_for ("inicial"))

# Pagina registrar
@app.route("/registrar", methods=["POST", "GET"])
def registrar():
	valNome = ""

	if request.method == "POST":
		# Dados do User
		dataName = request.form.get('name', valNome)
		dataEmail = request.form.get('email', valNome)
		dataPass = request.form.get('password', valNome)
		dataConfirm = request.form.get('confirmPassword', valNome)
		
		# Caso senha e confirmacao sejam iguais
		if dataPass == dataConfirm:
			# Verifica se o email ja existe
			if Users.query.filter_by(email=dataEmail).first():
				flash ("email ja cadastrado")
				return redirect (url_for ("registrar"))

			else:
				# Cria o novo user
				usuario = Users (dataName, dataEmail, dataPass)

				db.session.add(usuario)
				db.session.commit()

				flash ("User criado")

				return redirect (url_for ("registrar"))

		else:
			flash ("email nao cadastrado")
			return redirect (url_for ("registrar"))
			flash ("True")

		return redirect (url_for ("user"))


	return render_template ("registrar.html", logado=checarTipoLogin())

# PROPOSITO DE DEBUG APENAS (VER TODOS OS USERS E SENHAS)
@app.route ("/view")
def view ():
	return render_template ("view.html", values=Users.query.all())

if __name__ == "__main__":
	app.run (debug=True)