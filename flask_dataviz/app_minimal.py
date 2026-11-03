"""Étape 1 : la plus petite application Flask possible.

Lancer :  python app_minimal.py   puis ouvrir http://127.0.0.1:5000
"""

from flask import Flask

app = Flask(__name__)


@app.route("/")            # quand on visite l'adresse "/"…
def accueil():
    return "<h1>Bonjour !</h1><p>Ma première application Flask.</p>"   # …on renvoie cette page


@app.route("/bonjour/<prenom>")    # une partie de l'adresse devient un paramètre
def bonjour(prenom):
    return f"<h1>Bonjour {prenom} !</h1>"


if __name__ == "__main__":
    app.run(debug=True)    # debug=True : la page se recharge quand on modifie le code
