"""Étape 2 : un tableau de bord des ventes avec Flask + Pandas + Chart.js.

Lancer :  python app.py   puis ouvrir http://127.0.0.1:5000

Le principe :
1. Pandas lit et calcule les chiffres (comme dans le notebook 03).
2. Flask envoie ces chiffres à une page HTML.
3. La bibliothèque JavaScript Chart.js dessine les graphiques dans le navigateur.
"""

from pathlib import Path

import pandas as pd
from flask import Flask, jsonify, render_template, request

DATA = Path(__file__).resolve().parent.parent / "data" / "ventes.csv"

app = Flask(__name__)
app.json.sort_keys = False    # garder les mois dans l'ordre du calendrier dans le JSON


def charger_ventes() -> pd.DataFrame:
    """Charge et nettoie les ventes (même nettoyage que dans le notebook 03)."""
    df = pd.read_csv(DATA)
    df = df.dropna(subset=["quantite"]).drop_duplicates().copy()
    df["date"] = pd.to_datetime(df["date"])
    df["montant"] = df["quantite"] * df["prix_unitaire"]
    df["mois"] = df["date"].dt.month
    return df


VENTES = charger_ventes()     # chargé une seule fois, au démarrage
NOMS_MOIS = {1: "Janvier", 2: "Février", 3: "Mars", 4: "Avril", 5: "Mai", 6: "Juin"}


def filtrer(magasin: str) -> pd.DataFrame:
    if magasin == "Tous":
        return VENTES
    return VENTES[VENTES["magasin"] == magasin]


@app.route("/")
def tableau_de_bord():
    magasin = request.args.get("magasin", "Tous")     # lu dans l'adresse : /?magasin=Lyon
    df = filtrer(magasin)

    ca_mois = df.groupby("mois")["montant"].sum()
    ca_categorie = df.groupby("categorie")["montant"].sum().sort_values(ascending=False)
    ca_magasin = VENTES.groupby("magasin")["montant"].sum().sort_values(ascending=False)

    return render_template(
        "index.html",
        magasins=["Tous", *sorted(VENTES["magasin"].unique())],
        magasin_choisi=magasin,
        ca_total=round(df["montant"].sum(), 2),
        nb_ventes=len(df),
        panier_moyen=round(df["montant"].mean(), 2),
        mois_labels=[NOMS_MOIS[m] for m in ca_mois.index],
        mois_valeurs=ca_mois.round(2).tolist(),
        cat_labels=ca_categorie.index.tolist(),
        cat_valeurs=ca_categorie.round(2).tolist(),
        mag_labels=ca_magasin.index.tolist(),
        mag_valeurs=ca_magasin.round(2).tolist(),
    )


@app.route("/api/ca-par-mois")
def api_ca_par_mois():
    """Les mêmes chiffres en JSON : c'est ce qu'utiliserait une application mobile ou un autre site."""
    magasin = request.args.get("magasin", "Tous")
    ca_mois = filtrer(magasin).groupby("mois")["montant"].sum().round(2)
    return jsonify({NOMS_MOIS[m]: v for m, v in ca_mois.items()})


if __name__ == "__main__":
    app.run(debug=True)
