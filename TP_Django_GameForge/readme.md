# 🎮 GameForge - Générateur de jeux vidéo par IA

## 📋 Description du Projet

GameForge est une plateforme web complète développée avec Django permettant aux utilisateurs de créer des concepts de jeux vidéo originaux à l'aide de modèles d'intelligence artificielle via Hugging Face.

## 🎯 Objectifs Principaux

L'application génère automatiquement :
- **Un univers de jeu cohérent** (type, ambiance, style graphique)
- **Une histoire principale immersive** (scénario structuré en 3 actes)
- **Une galerie de personnages** (rôles, capacités, motivations)
- **Des illustrations conceptuelles** (visuels des environnements et personnages)
- **Une fiche de présentation du jeu** (pitch deck complet)

## 🧩 Fonctionnalités Principales

### 1. Formulaire de Création Guidée
L'utilisateur renseigne :
- Genre du jeu (RPG, FPS, Metroidvania, Visual Novel...)
- Ambiance visuelle et narrative (Post-apo, onirique, cyberpunk, dark fantasy...)
- Mots-clés thématiques (boucle temporelle, vengeance, IA rebelle...)
- Références culturelles optionnelles (Zelda, Hollow Knight, Disco Elysium...)

### 2. Génération Assistée par IA
- Génération structurée de l'univers
- Création d'un scénario en 3 actes avec retournement narratif
- Élaboration de 2 à 4 personnages (nom, classe, rôle narratif, background, gameplay)
- Création de lieux emblématiques avec descriptions immersives

### 3. Génération d'Images Conceptuelles
- Utilisation d'un modèle text-to-image (Stable Diffusion)
- Génération de visuels stylisés pour personnages et environnements

### 4. Mode "Exploration Libre"
- Génération complète aléatoire sans formulaire pour inspiration

## 📄 Pages de l'Application

### Pages Obligatoires
- **Page d'inscription** - Création de compte utilisateur
- **Page de connexion** - Authentification
- **Page d'accueil** - Affichage de tous les jeux générés par les utilisateurs (avec pseudo du créateur)
- **Tableau de bord** - Tous les jeux générés par l'utilisateur connecté
- **Page de détail** - Vue détaillée de chaque jeu
- **Page favoris** - Liste des jeux mis en favoris
- **Barre de navigation** - Navigation globale du site

## 🔐 Authentification & Sécurité

- Système d'authentification complet (connexion, inscription, déconnexion)
- Protection des projets (accès uniquement pour l'auteur)
- Toggle Public/Privé pour chaque projet
- Limitation d'usage API par utilisateur (anti-spam)

## 🎁 Fonctionnalités Bonus (Exemples)

- 📖 Système de narration dynamique (scénario évolutif selon les choix)
- 📦 Export PDF stylisé (fiche jeu auto-maquettée style Steam/itch.io)
- 🧙 Système de "favoris" ou "like"
- 🔍 Barre de recherche pour filtrer les jeux (nom, type, date...)
- ⚙️ Page de paramètres de compte
- 💬 Pop-ups de chargement pendant la génération
- 👾 GDD complet (Game Design Document)

## 🛠️ Stack Technique

### Backend
- **Framework** : Django 4.x
- **Base de données** : SQLite (développement) / PostgreSQL (production)
- **API IA** : Hugging Face API
  - Modèles de génération de texte (GPT-2, BLOOM, etc.)
  - Modèles text-to-image (Stable Diffusion)

### Frontend
- **Templates** : Django Templates
- **CSS Framework** : Bootstrap 5 / Tailwind CSS
- **JavaScript** : Vanilla JS / Alpine.js

## 📁 Structure du Projet

```
gameforge/
│
├── gameforge/              # Configuration Django principale
│   ├── settings.py
│   ├── urls.py
│   ├── wsgi.py
│   └── asgi.py
│
├── accounts/               # Application gestion utilisateurs
│   ├── models.py          # User model
│   ├── views.py           # Login, signup, profile
│   ├── forms.py
│   └── urls.py
│
├── games/                  # Application principale
│   ├── models.py          # Game, Character, Location, etc.
│   ├── views.py           # CRUD jeux, génération IA
│   ├── forms.py           # Formulaire de création
│   ├── services/
│   │   ├── ai_text_generator.py
│   │   └── ai_image_generator.py
│   └── urls.py
│
├── static/                 # Fichiers statiques
│   ├── css/
│   ├── js/
│   └── images/
│
├── media/                  # Fichiers uploadés/générés
│   └── generated_images/
│
├── templates/              # Templates Django
│   ├── base.html
│   ├── accounts/
│   ├── games/
│   └── partials/
│
├── requirements.txt        # Dépendances Python
├── .env.example           # Variables d'environnement
├── .gitignore
└── README.md
```

## 🗄️ Schéma de Base de Données

### Modèles Principaux

```python
User (Django built-in)
├── username
├── email
├── password
└── date_joined

Game
├── id (PK)
├── title
├── genre
├── theme
├── keywords
├── references
├── creator (FK -> User)
├── is_public (Boolean)
├── created_at
├── updated_at
├── universe_description
├── story_act1
├── story_act2
├── story_act3
└── main_image

Character
├── id (PK)
├── game (FK -> Game)
├── name
├── character_class
├── role
├── background
├── gameplay_description
└── image

Location
├── id (PK)
├── game (FK -> Game)
├── name
├── description
└── image

Favorite
├── id (PK)
├── user (FK -> User)
├── game (FK -> Game)
└── created_at
```

## 🔄 Flux de Données

### Processus de Génération de Jeu

```
1. Utilisateur remplit le formulaire
   ↓
2. Django reçoit les données (genre, thème, mots-clés)
   ↓
3. Service AI Text Generator
   - Appel API Hugging Face pour générer :
     * Univers
     * Histoire (3 actes)
     * Personnages (2-4)
     * Lieux
   ↓
4. Service AI Image Generator
   - Génération d'images pour :
     * Personnage principal
     * Environnement principal
   ↓
5. Sauvegarde en base de données
   - Création de l'objet Game
   - Création des objets Character
   - Création des objets Location
   ↓
6. Redirection vers la page de détail du jeu
```

## 🚀 Installation et Configuration

### Prérequis
- Python 3.10+
- pip
- virtualenv
- Compte Hugging Face (pour API token)

### Installation

```bash
# Cloner le repository
git clone https://github.com/votre-username/gameforge.git
cd gameforge

# Créer un environnement virtuel
python -m venv venv

# Activer l'environnement virtuel
# Windows
venv\Scripts\activate
# Linux/Mac
source venv/bin/activate

# Installer les dépendances
pip install -r requirements.txt

# Copier le fichier d'environnement
cp .env.example .env

# Modifier .env avec vos configurations
# HUGGINGFACE_API_KEY=votre_clé_api
# SECRET_KEY=votre_secret_key_django

# Créer la base de données
python manage.py makemigrations
python manage.py migrate

# Créer un superuser
python manage.py createsuperuser

# Collecter les fichiers statiques
python manage.py collectstatic

# Lancer le serveur de développement
python manage.py runserver
```

### Variables d'Environnement (.env)

```env
# Django
SECRET_KEY=votre_secret_key_django
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

# Database
DATABASE_URL=sqlite:///db.sqlite3

# Hugging Face
HUGGINGFACE_API_KEY=votre_clé_api_huggingface

# Media
MEDIA_URL=/media/
MEDIA_ROOT=media/
```

## 🔑 Configuration API Hugging Face

1. Créer un compte sur [Hugging Face](https://huggingface.co/)
2. Générer un token d'accès dans Settings > Access Tokens
3. Ajouter le token dans `.env`

### Modèles Recommandés

**Pour la génération de texte :**
- `mistralai/Mistral-7B-Instruct-v0.2`
- `facebook/opt-1.3b`
- `gpt2` (plus léger)

**Pour la génération d'images :**
- `stabilityai/stable-diffusion-2-1`
- `runwayml/stable-diffusion-v1-5`
- `CompVis/stable-diffusion-v1-4`

## 🧪 Tests

```bash
# Lancer tous les tests
python manage.py test

# Tests d'une application spécifique
python manage.py test games

# Tests avec coverage
coverage run --source='.' manage.py test
coverage report
```

## 📦 Dépendances Principales

```
Django>=4.2
python-dotenv>=1.0.0
Pillow>=10.0.0
requests>=2.31.0
huggingface-hub>=0.17.0
```

---

**Note** : Ce projet est réalisé dans le cadre d'un TP académique.