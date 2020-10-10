from flask import Flask

app = Flask(__name__)

@app.route ("/")
def inicial ():
	return render_template ("inicio.html")

if __name__ == "__main__":
	app.run (debug=True)