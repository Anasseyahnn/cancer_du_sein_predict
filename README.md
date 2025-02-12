# Diagnostic du Cancer du Sein Predictor
## Description du Projet
L'application Diagnostic du Cancer du Sein Predictor est un outil convivial basé sur Streamlit qui permet aux utilisateurs de prédire le diagnostic d'une tumeur mammaire (maligne ou bénigne) en utilisant des données cliniques. Cette application s'appuie sur un modèle pré-entraîné de machine learning pour fournir des prédictions fiables et rapides.

## Fonctionnalités

***Interface Utilisateur Intuitive*** : L'application propose une interface utilisateur simple et intuitive, avec des curseurs pour saisir les valeurs des caractéristiques cliniques des cellules tumorales.

***Graphique Radar*** : Un graphique radar interactif est généré pour visualiser les valeurs moyennes, les erreurs standard et les pires valeurs des caractéristiques cliniques.

***Prédiction en Temps Réel*** : L'application fournit une prédiction en temps réel sur la nature de la tumeur (maligne ou bénigne) ainsi que les probabilités associées.

***Avertissement Médical*** : les résultats fournis ne remplacent pas l'avis médical professionnel.

## Structure du Code
1. Obtention et Nettoyage des Données
La fonction get_clean_data() charge les données à partir d'un fichier CSV, supprime les colonnes inutiles (id et Unnamed: 32), et recode la variable cible (diagnosis) en valeurs binaires (0 pour bénin, 1 pour malin).

2. Barre Latérale (Sidebar)
La fonction add_sidebar() crée une barre latérale avec des curseurs pour saisir les valeurs des caractéristiques cliniques. Les curseurs sont configurés pour accepter des valeurs comprises entre 0 et la valeur maximale de chaque caractéristique dans le jeu de données.

3. Mise à l'Échelle des Valeurs
La fonction get_scaled_values() met à l'échelle les valeurs saisies par l'utilisateur pour qu'elles soient comprises entre 0 et 1, en utilisant les valeurs minimales et maximales de chaque caractéristique dans le jeu de données.

4. Graphique Radar
La fonction get_radar_chart() génère un graphique radar interactif à l'aide de la bibliothèque Plotly. Le graphique affiche les valeurs moyennes, les erreurs standard et les pires valeurs des caractéristiques cliniques.

5. Prédiction
La fonction add_predictions() charge le modèle de machine learning et le scaler à partir de fichiers pickle, met à l'échelle les données saisies par l'utilisateur, et effectue une prédiction sur la nature de la tumeur. Les résultats de la prédiction, ainsi que les probabilités associées, sont affichés à l'utilisateur.

6. Interface Principale
La fonction main() configure la page Streamlit, charge les styles CSS, et organise l'interface utilisateur en deux colonnes : une pour le graphique radar et une autre pour les résultats de la prédiction.

Utilisation
Installation des Dépendances :

Assurez-vous d'avoir installé les bibliothèques nécessaires en exécutant la commande suivante :

bash
Copy
pip install streamlit pandas plotly numpy scikit-learn
Lancement de l'Application :

Pour lancer l'application, exécutez la commande suivante dans votre terminal :

bash
Copy
streamlit run app.py
Saisie des Données :

Utilisez les curseurs dans la barre latérale pour saisir les valeurs des caractéristiques cliniques des cellules tumorales.

Visualisation des Résultats :

Le graphique radar et les résultats de la prédiction seront automatiquement mis à jour en fonction des valeurs saisies.

Avertissement
Cette application a été développée dans le but de fournir une estimation basée sur des données cliniques entrées par l'utilisateur. Les résultats fournis par cette application ne remplacent en aucun cas l'avis médical professionnel.

Contribution
Les contributions sont les bienvenues ! Si vous souhaitez améliorer cette application, n'hésitez pas à ouvrir une issue ou à soumettre une pull request.

Licence
Ce projet est sous licence MIT. Voir le fichier LICENSE pour plus de détails.

Auteur : [Votre Nom]
Contact : [votre.email@example.com]
GitHub : [lien vers votre profil GitHub]

ajoute des icones
Diagnostic du Cancer du Sein Predictor
Description du Projet
L'application Diagnostic du Cancer du Sein Predictor est un outil convivial basé sur Streamlit qui permet aux utilisateurs de prédire le diagnostic d'une tumeur mammaire (maligne ou bénigne) en utilisant des données cliniques. Cette application s'appuie sur un modèle pré-entraîné de machine learning pour fournir des prédictions fiables et rapides.

Fonctionnalités
📊 Interface Utilisateur Intuitive : L'application propose une interface utilisateur simple et intuitive, avec des curseurs pour saisir les valeurs des caractéristiques cliniques des cellules tumorales.

📈 Graphique Radar : Un graphique radar interactif est généré pour visualiser les valeurs moyennes, les erreurs standard et les pires valeurs des caractéristiques cliniques.

🔮 Prédiction en Temps Réel : L'application fournit une prédiction en temps réel sur la nature de la tumeur (maligne ou bénigne) ainsi que les probabilités associées.

⚠️ Avertissement Médical : L'application inclut un avertissement clair indiquant que les résultats fournis ne remplacent pas l'avis médical professionnel.

Structure du Code
1. 📂 Obtention et Nettoyage des Données
La fonction get_clean_data() charge les données à partir d'un fichier CSV, supprime les colonnes inutiles (id et Unnamed: 32), et recode la variable cible (diagnosis) en valeurs binaires (0 pour bénin, 1 pour malin).

2. 📏 Barre Latérale (Sidebar)
La fonction add_sidebar() crée une barre latérale avec des curseurs pour saisir les valeurs des caractéristiques cliniques. Les curseurs sont configurés pour accepter des valeurs comprises entre 0 et la valeur maximale de chaque caractéristique dans le jeu de données.

3. 📐 Mise à l'Échelle des Valeurs
La fonction get_scaled_values() met à l'échelle les valeurs saisies par l'utilisateur pour qu'elles soient comprises entre 0 et 1, en utilisant les valeurs minimales et maximales de chaque caractéristique dans le jeu de données.

4. 📊 Graphique Radar
La fonction get_radar_chart() génère un graphique radar interactif à l'aide de la bibliothèque Plotly. Le graphique affiche les valeurs moyennes, les erreurs standard et les pires valeurs des caractéristiques cliniques.

5. 🔍 Prédiction
La fonction add_predictions() charge le modèle de machine learning et le scaler à partir de fichiers pickle, met à l'échelle les données saisies par l'utilisateur, et effectue une prédiction sur la nature de la tumeur. Les résultats de la prédiction, ainsi que les probabilités associées, sont affichés à l'utilisateur.

6. 🖥️ Interface Principale
La fonction main() configure la page Streamlit, charge les styles CSS, et organise l'interface utilisateur en deux colonnes : une pour le graphique radar et une autre pour les résultats de la prédiction.

Utilisation
