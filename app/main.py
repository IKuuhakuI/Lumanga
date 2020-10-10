from flask import Flask, render_template, request, redirect, url_for, session
from datetime import timedate

app = Flask(__name__)
app.secret_key = "teste"
app.permanent_session_lifetime = timedelta(minutes=5)

@app.route ("/")
def inicial ():
	return render_template ("inicio.html")

@app.route("/entrar", methods=["POST", "GET"])
def login():
	if request.method == "POST":
		session.permanent = True
		userEmail = request.form ["email"]
		session["email"] = userEmail

		return redirect (url_for ("user"))

	else:
		if "email" in session:
			return redirect(url_for("user"))
		return render_template ("entrar.html")

@app.route("/user")
def user ():
	if "email" in session:
		email = session["email"]

		return f"<h1>{email}</h1>"

	else:
		return redirect (url_for ("login"))

@app.route("/consultas")
def consultas():
	return render_template ("consultas.html")

@app.route("/eventos")
def eventos():
	return render_template ("eventos.html")


@app.route("/sair")
def logout():
	session.pop("email", None)
	return redirect( url_for ("inicial"))

if __name__ == "__main__":
	app.run (debug=True)