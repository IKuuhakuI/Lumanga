from flask import Flask, render_template

app = Flask(__name__)

@app.route ("/")
def inicial ():
	return render_template ("inicio.html")

@app.route("/entrar")
def login():
	return render_template ("entrar.html")

@app.route("/consultas")
def consultas():
	return render_template ("consultas.html")

@app.route("/eventos")
def eventos():
	return render_template ("eventos.html")


if __name__ == "__main__":
	app.run (debug=True)