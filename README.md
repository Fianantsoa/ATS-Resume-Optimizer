# ATS-Resume-Optimizer

## Description du projet
ATS-Resume-Optimizer est une application Streamlit qui compare un CV avec une description de poste pour évaluer l’alignement ATS (Applicant Tracking System). Elle calcule un score et met en évidence les mots-clés manquants. Elle propose aussi des suggestions d’amélioration et génère une version optimisée du CV.

## Fonctionnalités
- Importer un CV en PDF ou TXT
- Extraire les mots-clés d’une description de poste
- Calculer un score ATS (/100)
- Lister les mots-clés manquants
- Proposer des suggestions d’amélioration
- Générer un CV optimisé en ajoutant des mots-clés pertinents

## Prérequis
- Python 3.x
- pip

## Installation
1. (Optionnel) Créer un environnement virtuel :
   - `python -m venv .venv`
   - `source .venv/bin/activate` (Linux/macOS) ou `./.venv/Scripts/activate` (Windows)
2. Installer les dépendances :
   - `pip install -r requirements.txt`

## Lancer l’application
- `streamlit run app.py`
- Ouvrir l’URL affichée par Streamlit dans votre navigateur.

## Tester le projet
- `python -m unittest discover -s tests`
