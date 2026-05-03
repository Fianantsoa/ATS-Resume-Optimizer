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
- ''Python 3.9+''
- ''pip''

## Installation
1. (Optionnel) Créer un environnement virtuel :

```bash
  python -m venv .venv
```
(Linux/macOS)
```bash
  source .venv/bin/activate
```
 ou (Windows)
```bash
  ./.venv/Scripts/activate
```

3. Installer les dépendances :
```bash
  pip install -r requirements.txt
```

## Lancer l’application
```bash
  streamlit run app.py
```
- Ouvrir l’URL affichée par Streamlit dans votre navigateur.

## Tester le projet
```python -m unittest discover -s tests```
