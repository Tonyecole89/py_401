# Visualisation de données avec Flask

## Installer

```bash
pip install flask pandas
```

## Étape 1 — La plus petite application Flask

```bash
python app_minimal.py
```

Ouvrir http://127.0.0.1:5000, puis http://127.0.0.1:5000/bonjour/Lina

## Étape 2 — Le tableau de bord des ventes

```bash
python app.py
```

Ouvrir http://127.0.0.1:5000 : chiffres clés, 3 graphiques et un menu pour choisir le magasin.
Les mêmes chiffres en JSON : http://127.0.0.1:5000/api/ca-par-mois?magasin=Lyon

Arrêter le serveur : **Ctrl + C** dans le terminal.

## Comment ça marche

1. `app.py` lit `data/ventes.csv` avec Pandas et calcule les totaux (comme dans le notebook 03).
2. Flask envoie ces chiffres au fichier `templates/index.html`.
3. Dans la page, la bibliothèque JavaScript Chart.js dessine les graphiques.

## Exercices en binôme

1. **Niveau 1** : changez les couleurs des graphiques et le titre de la page.
2. **Niveau 2** : ajoutez un 4ᵉ graphique « Top 5 des produits par CA ».
   - Dans `app.py` : `top = df.groupby("produit")["montant"].sum().nlargest(5)`, puis passez `top.index.tolist()` et `top.round(2).tolist()` au template.
   - Dans `index.html` : ajoutez une carte avec un `<canvas id="graphTop">` et un `new Chart(...)` de type `"bar"`.
3. **Niveau 3** : ajoutez une route `/api/ca-par-magasin` qui renvoie le CA de chaque magasin en JSON.
