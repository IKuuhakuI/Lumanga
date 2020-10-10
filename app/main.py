from flask import Flask, render_template, request, redirect, url_for, session, flash
from datetime import timedelta

app = Flask(__name__)
app.secret_key = "teste"
app.permanent_session_lifetime = timedelta(minutes=5)

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


@app.route("/sair")
def logout():
	if "email" in session:
		user = session["email"]
		flash (f"{user}, saiu", "info")
	
	session['logged_in']=False
	session.pop("email", None)


	return redirect( url_for ("inicial"))

if __name__ == "__main__":
	app.run (debug=True)