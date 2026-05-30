# Diagnostic du Cancer du Sein — Modélisation Prédictive

Cette application web interactive est conçue pour prédire si une tumeur mammaire est maligne ou bénigne à partir de métriques cliniques issues de mesures nucléaires d'aspiration à l'aiguille fine (FNA). Elle s'appuie sur un modèle de machine learning de Régression Logistique entraîné sur le jeu de données WBCD (Wisconsin Breast Cancer Database).

## Fonctionnalités

* **Classification en temps réel** : Analyse instantanée des mesures des caractéristiques cellulaires saisies par l'utilisateur pour prédire la nature de la tumeur.
* **Graphique Radar Interactif** : Représentation visuelle normalisée des métriques cliniques comparant les valeurs moyennes, l'erreur standard et les pires valeurs pour guider l'interprétation.
* **Interface Premium** : Design de niveau clinique fondé sur le thème **Slate-Light** (polices *Plus Jakarta Sans*, conteneurs blancs avec ombres douces et dégradés épurés), complètement exempt d'émojis de type IA.
* **Correction d'inversion diagnostique** : Correction du bug critique de l'interface qui inversait les prédictions malignes/bénignes et intervertissait leurs probabilités associées.
* **Portabilité complète** : Remplacement des chemins d'accès système absolus par des références dynamiques portables, permettant l'exécution sur n'importe quelle machine sans modification de code.

## Architecture Clinique & Modèle

Le pipeline clinique suit la structure suivante :
1. **Entraînement (`cancer.py`)** : Extraction des données depuis `data.csv`, nettoyage des colonnes d'index inutiles, normalisation des variables prédictives via `StandardScaler` et entraînement d'un classificateur par **Régression Logistique** avec Scikit-Learn. Le modèle et le scaler sont exportés via `pickle`.
2. **Dashboard de Diagnostic (`index.py`)** : Chargement dynamique du modèle et du scaler pré-entraînés, normalisation des valeurs saisies via la barre latérale, génération du radar Scatterpolar Plotly et prédiction finale.

## Installation

### Prérequis

* Python 3.10 ou supérieur

### Étapes d'installation

1. Accédez au répertoire du projet :
   ```bash
   cd projects/cancer_du_sein_predict
   ```

2. Créez un environnement virtuel et activez-le :
   ```bash
   python -m venv venv
   # Sur Windows :
   venv\Scripts\activate
   # Sur macOS/Linux :
   source venv/bin/activate
   ```

3. Installez les paquets requis :
   ```bash
   pip install streamlit pandas numpy scikit-learn plotly
   ```

4. Entraînez le modèle localement pour générer les fichiers sérialisés :
   ```bash
   python cancer.py
   ```

## Utilisation

Lancez l'application Streamlit :

```bash
streamlit run index.py
```

L'application sera accessible dans votre navigateur à l'adresse `http://localhost:8501`.

### Guide d'utilisation

1. **Saisie des paramètres** : Modifiez les mesures nucléaires à l'aide des curseurs de la barre latérale.
2. **Visualisation Radar** : Observez en temps réel le graphique Scatterpolar qui illustre l'écart entre la moyenne de la tumeur, l'erreur type et la pire valeur.
3. **Analyse de la Prédiction** : La carte de diagnostic s'affiche en rouge en cas de tumeur maligne et en vert en cas de tumeur bénigne, avec leurs probabilités mathématiques respectives.

## Avertissement Légal

Cette console d'analyse est un outil de démonstration technologique à vocation éducative et d'aide à la modélisation prédictive. Les prédictions générées par le modèle mathématique ne constituent pas un diagnostic médical professionnel et ne se substituent aucunement à l'avis d'un oncologue ou d'un praticien de santé agréé.
