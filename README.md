# 💄 Boutique Cosmétique – Application de gestion

Application de gestion complète pour une boutique de cosmétiques, développée en **Python** avec **Kivy** et **KivyMD**.

## Fonctionnalités

- **Connexion** sécurisée (utilisateur par défaut : `admin` / `admin123`)
- **Tableau de bord** avec statistiques en temps réel :
  - Nombre de produits
  - Alertes de stock bas
  - Nombre de clients
  - Chiffre d'affaires du jour
- **Gestion des produits** (CRUD) :
  - Nom, marque, catégorie, prix, stock, stock minimum, code-barres, description
  - Recherche en direct
  - Alertes de stock bas
- **Point de vente (POS)** :
  - Recherche de produits
  - Panier dynamique
  - Mise à jour automatique du stock
- **Gestion des clients** (ajout, modification, suppression, recherche)
- **Historique des ventes**

## Prérequis

- Python 3.9+
- pip

## Installation

```bash
# Créer un environnement virtuel (recommandé)
python -m venv venv
source venv/bin/activate          # Linux / macOS
# ou
venv\Scripts\activate             # Windows

# Installer les dépendances
pip install -r requirements.txt
```

## Lancement

```bash
python main.py
```

## Structure du projet

```
cosmetic_shop/
├── main.py              # Application principale (UI + logique)
├── database.py          # Couche base de données SQLite
├── requirements.txt
├── README.md
└── data/
    └── boutique.db      # Base de données (créée automatiquement)
```

## Identifiants par défaut

| Champ           | Valeur     |
|-----------------|------------|
| Nom d'utilisateur | `admin`   |
| Mot de passe      | `admin123`|

## Technologies

- **Kivy 2.3+** – Framework multi-plateforme
- **KivyMD 2.0** – Material Design 3
- **SQLite** – Base de données locale

## Notes

- L'application fonctionne sur Windows, Linux et macOS.
- La base de données est créée automatiquement au premier lancement avec des produits d'exemple.
- Les mots de passe sont stockés en clair (pour simplifier la démonstration). En production, utilisez un hachage (bcrypt, argon2…).

---
Développé avec ❤️ pour la gestion de boutiques cosmétiques.
