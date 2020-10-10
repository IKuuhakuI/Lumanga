from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)
app.secret_key = "hello"

@app.route ("/")
def inicial ():
	flash ("O jogo")
	return render_template ("inicio.html")

@app.route("/entrar", methods=["POST", "GET"])
def login():
	if request.method == "POST":
		user = request.form ["email"]

		return redirect (url_for ("user", usr=user))

	else:	
		return render_template ("entrar.html")

@app.route("/<usr>")
def user (usr):
	return f"<h1>{usr}</h1>"

@app.route("/consultas")
def consultas():
	return render_template ("consultas.html")

@app.route("/eventos")
def eventos():
	return render_template ("eventos.html")

if __name__ == "__main__":
	app.run (debug=True)