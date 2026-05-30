import streamlit as st
import pickle as pickle 
import pandas as pd
import plotly.graph_objects as go
import numpy as np
import os

# Détermination du dossier de base de manière portable
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# obtenion de la table de donnees et netoyage
def get_clean_data():
    data_path = os.path.join(BASE_DIR, "data.csv")
    data = pd.read_csv(data_path)
    
    # supression des colonnes id et unnamaed
    data = data.drop(["id","Unnamed: 32"], axis = 1)
    
    # recoage de la varible cible en  et 1
    data["diagnosis"] = data["diagnosis"].map({"M":1, "B":0})
    
    return data

# Initialisation de la session state pour chaque métrique si absente
data = get_clean_data()
for col in data.columns:
    if col != 'diagnosis':
        session_key = f"slider_{col}"
        if session_key not in st.session_state:
            st.session_state[session_key] = float(data[col].mean())

# ----------------- SIDEBAR -----------------
def add_sidebar():
    st.sidebar.markdown("""
    <div style="display: flex; align-items: center; gap: 8px; margin-bottom: 12px;">
        <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="#2563eb" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="3"></circle><path d="M19.4 15a1.65 1.65 0 0 0 .33 1.82l.06.06a2 2 0 1 1-2.83 2.83l-.06-.06a1.65 1.65 0 0 0-1.82-.33 1.65 1.65 0 0 0-1 1.51V21a2 2 0 0 1-4 0v-.09A1.65 1.65 0 0 0 9 19.4a1.65 1.65 0 0 0-1.82.33l-.06.06a2 2 0 1 1-2.83-2.83l.06-.06a1.65 1.65 0 0 0 .33-1.82 1.65 1.65 0 0 0-1.51-1H3a2 2 0 0 1 0-4h.09A1.65 1.65 0 0 0 4.6 9a1.65 1.65 0 0 0-.33-1.82l-.06-.06a2 2 0 1 1 2.83-2.83l.06.06a1.65 1.65 0 0 0 1.82.33H9a1.65 1.65 0 0 0 1-1.51V3a2 2 0 0 1 4 0v.09a1.65 1.65 0 0 0 1 1.51 1.65 1.65 0 0 0 1.82-.33l.06-.06a2 2 0 1 1 2.83 2.83l-.06.06a1.65 1.65 0 0 0-.33 1.82V9a1.65 1.65 0 0 0 1.51 1H21a2 2 0 0 1 0 4h-.09a1.65 1.65 0 0 0-1.51 1z"></path></svg>
        <span style="font-size: 1.1rem; font-weight: 700; color: #1e293b;">Console de Contrôle</span>
    </div>
    """, unsafe_allow_html=True)
    
    # Boutons d'exemples cliniques interactifs
    st.sidebar.markdown("<div style='font-size:0.8rem; text-transform:uppercase; color:#64748b; font-weight:700; letter-spacing:0.05em; margin-bottom:8px;'>Cas Cliniques Prédéfinis :</div>", unsafe_allow_html=True)
    
    col_benign, col_malignant = st.sidebar.columns(2)
    with col_benign:
        if st.sidebar.button("Exemple Bénin", use_container_width=True, key="side_btn_benign"):
            benign_samples = data[data['diagnosis'] == 0]
            if not benign_samples.empty:
                sample = benign_samples.sample(1).iloc[0]
                for col in data.columns:
                    if col != 'diagnosis':
                        st.session_state[f"slider_{col}"] = float(sample[col])
                st.rerun()
                
    with col_malignant:
        if st.sidebar.button("Exemple Malin", use_container_width=True, key="side_btn_malignant"):
            malignant_samples = data[data['diagnosis'] == 1]
            if not malignant_samples.empty:
                sample = malignant_samples.sample(1).iloc[0]
                for col in data.columns:
                    if col != 'diagnosis':
                        st.session_state[f"slider_{col}"] = float(sample[col])
                st.rerun()
                
    col_random, col_reset = st.sidebar.columns(2)
    with col_random:
        if st.sidebar.button("Cas Aléatoire", use_container_width=True, key="side_btn_random"):
            sample = data.sample(1).iloc[0]
            for col in data.columns:
                if col != 'diagnosis':
                    st.session_state[f"slider_{col}"] = float(sample[col])
            st.rerun()
            
    with col_reset:
        if st.sidebar.button("Moyennes", use_container_width=True, key="side_btn_reset"):
            for col in data.columns:
                if col != 'diagnosis':
                    st.session_state[f"slider_{col}"] = float(data[col].mean())
            st.rerun()
            
    st.sidebar.markdown("---")
    
    # Catégorisation des curseurs dans la sidebar pour la rendre intéressante
    st.sidebar.markdown("<div style='font-size:0.8rem; text-transform:uppercase; color:#64748b; font-weight:700; letter-spacing:0.05em; margin-bottom:8px;'>Groupes de Paramètres :</div>", unsafe_allow_html=True)
    
    slider_labels_mean = [
        ("Rayon (Moyenne)","radius_mean"),
        ("Texture (Moyenne)", "texture_mean"),
        ("Périmètre (Moyenne)", "perimeter_mean"),
        ("Aire (Moyenne)","area_mean"),
        ("Lissage (Moyenne)","smoothness_mean"),
        ("Compacité (Moyenne)", "compactness_mean"),
        ("Concavité (Moyenne)","concavity_mean"),
        ("Points Concaves (Moyenne)","concave points_mean"),
        ("Symétrie (Moyenne)","symmetry_mean"),
        ("Dim. Fractale (Moyenne)","fractal_dimension_mean"),
    ]
    
    slider_labels_se = [
        ("Rayon (Erreur Std)","radius_se"),
        ("Texture (Erreur Std)","texture_se"),
        ("Périmètre (Erreur Std)","perimeter_se"),
        ("Aire (Erreur Std)","area_se"),
        ("Lissage (Erreur Std)", "smoothness_se"),
        ("Compacité (Erreur Std)", "compactness_se"),
        ("Concavité (Erreur Std)","concavity_se"),
        ("Points Concaves (Erreur Std)","concave points_se"),
        ("Symétrie (Erreur Std)","symmetry_se"), 
        ("Dim. Fractale (Erreur Std)","fractal_dimension_se"),
    ]
    
    slider_labels_worst = [
        ("Rayon (Pire)","radius_worst"),
        ("Texture (Pire)","texture_worst"),
        ("Périmètre (Pire)","perimeter_worst"),
        ("Aire (Pire)","area_worst"),
        ("Lissage (Pire)","smoothness_worst"),
        ("Compacité (Pire)","compactness_worst"),
        ("Concavité (Pire)","concavity_worst"),
        ("Points Concaves (Pire)","concave points_worst"),
        ("Symétrie (Pire)","symmetry_worst"),
        ("Dim. Fractale (Pire)","fractal_dimension_worst"),
    ]
    
    input_dict = {}
    
    # Groupe 1 : Mesures Moyennes (Mean)
    with st.sidebar.expander("Dimensions Moyennes (Mean)", expanded=True):
        st.markdown("<p style='font-size:0.75rem; color:#64748b; margin-top:0;'>Mesures physiques et géométriques principales des noyaux.</p>", unsafe_allow_html=True)
        for label, key in slider_labels_mean:
            session_key = f"slider_{key}"
            input_dict[key] = st.slider(
                label, 
                min_value=float(0),
                max_value=float(data[key].max()),
                value=st.session_state[session_key],
                key=session_key
            )
            st.session_state[key] = input_dict[key]
            
    # Groupe 2 : Variations et Erreurs Standards (SE)
    with st.sidebar.expander("Variations & Écarts (SE)", expanded=False):
        st.markdown("<p style='font-size:0.75rem; color:#64748b; margin-top:0;'>Variabilité et erreurs types mesurées d'une cellule à l'autre.</p>", unsafe_allow_html=True)
        for label, key in slider_labels_se:
            session_key = f"slider_{key}"
            input_dict[key] = st.slider(
                label, 
                min_value=float(0),
                max_value=float(data[key].max()),
                value=st.session_state[session_key],
                key=session_key
            )
            st.session_state[key] = input_dict[key]
            
    # Groupe 3 : Pires Scénarios (Worst)
    with st.sidebar.expander("Valeurs Extrêmes (Worst)", expanded=False):
        st.markdown("<p style='font-size:0.75rem; color:#64748b; margin-top:0;'>Les plus grandes valeurs mesurées, indiquant l'irrégularité maximale.</p>", unsafe_allow_html=True)
        for label, key in slider_labels_worst:
            session_key = f"slider_{key}"
            input_dict[key] = st.slider(
                label, 
                min_value=float(0),
                max_value=float(data[key].max()),
                value=st.session_state[session_key],
                key=session_key
            )
            st.session_state[key] = input_dict[key]
        
    return input_dict

# ----------------- NORMALISATION -----------------
def get_scaled_values(input_dict):
    X = data.drop(["diagnosis"], axis = 1)
    
    scaled_dict = {}
    for key, value in input_dict.items():
        max_val = X[key].max()
        min_val = X[key].min()
        if max_val == min_val:
            scaled_value = 0.0
        else:
            scaled_value = (value - min_val) / (max_val - min_val)
        scaled_dict[key] = scaled_value
        
    return scaled_dict 

# ----------------- GRAPHIQUE RADAR -----------------
def get_radar_chart(input_data):
    input_data = get_scaled_values(input_data)
    
    categories = ['Rayon', 'Texture', 'Périmètre', 'Aire',
                  'Lissage', 'Compacité',
                  'Concavité', 'Pts Concaves',
                  'Symétrie', 'Dim. Fractale']

    fig = go.Figure()
    
    # Valeurs moyennes (Bleu)
    fig.add_trace(go.Scatterpolar(
          r = [
              input_data['radius_mean'], input_data['texture_mean'], input_data['perimeter_mean'],
              input_data['area_mean'], input_data['smoothness_mean'], input_data['compactness_mean'],
              input_data['concavity_mean'], input_data['concave points_mean'], input_data['symmetry_mean'],
              input_data['fractal_dimension_mean']
              ],
          theta=categories,
          fill='toself',
          name='Moyenne',
          fillcolor='rgba(59, 130, 246, 0.15)',
          line=dict(color='#3b82f6', width=2)
    ))
    
    # Erreur standard (Vert)
    fig.add_trace(go.Scatterpolar(
          r = [
              input_data['radius_se'], input_data['texture_se'], input_data['perimeter_se'],
              input_data['area_se'], input_data['smoothness_se'], input_data['compactness_se'],
              input_data['concavity_se'], input_data['concave points_se'], input_data['symmetry_se'],
              input_data['fractal_dimension_se']
              ],
          theta=categories,
          fill='toself',
          name='Erreur Type',
          fillcolor='rgba(16, 185, 129, 0.12)',
          line=dict(color='#10b981', width=2)
    ))
    
    # Pires valeurs (Rose-Rouge)
    fig.add_trace(go.Scatterpolar(
          r = [
              input_data['radius_worst'], input_data['texture_worst'], input_data['perimeter_worst'],
              input_data['area_worst'], input_data['smoothness_worst'], input_data['compactness_worst'],
              input_data['concavity_worst'], input_data['concave points_worst'], input_data['symmetry_worst'],
              input_data['fractal_dimension_worst']
              ],
          theta=categories,
          fill='toself',
          name='Pire Valeur',
          fillcolor='rgba(244, 63, 94, 0.15)',
          line=dict(color='#f43f5e', width=2)
    ))
    
    fig.update_layout(
      polar=dict(
        radialaxis=dict(
          visible=True,
          range=[0, 1],
          gridcolor='#e2e8f0',
          linecolor='#cbd5e1'
        ),
        angularaxis=dict(
          gridcolor='#e2e8f0',
          linecolor='#cbd5e1'
        ),
        bgcolor='rgba(255, 255, 255, 0.6)'
      ),
      showlegend=True,
      margin=dict(l=40, r=40, t=20, b=20),
      paper_bgcolor='rgba(0,0,0,0)',
      plot_bgcolor='rgba(0,0,0,0)'
    )
    
    return fig

# ----------------- MODULE PRÉDICTIONS (FIXÉ) -----------------
def add_predictions(input_data):
    model_path = os.path.join(BASE_DIR, "model.pkl")
    scaler_path = os.path.join(BASE_DIR, "scaler.pkl")
    
    try:
        model = pickle.load(open(model_path, "rb"))
        scaler = pickle.load(open(scaler_path, "rb"))
    except FileNotFoundError:
        st.error("Les fichiers du modèle (model.pkl ou scaler.pkl) sont introuvables.")
        return
        
    input_array = np.array(list(input_data.values())).reshape(1,-1)
    input_array_scaled = scaler.transform(input_array)
    
    # Prédiction clinique
    prediction = model.predict(input_array_scaled)
    prob_benign = model.predict_proba(input_array_scaled)[0][0] # Indice 0 = Bénigne (B)
    prob_malignant = model.predict_proba(input_array_scaled)[0][1] # Indice 1 = Maligne (M)
    
    st.markdown("""
    <div style="display: flex; align-items: center; gap: 8px; margin-bottom: 12px; margin-top: 5px;">
        <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="#2563eb" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"></path><polyline points="22 4 12 14.01 9 11.01"></polyline></svg>
        <span style="font-size: 1.15rem; font-weight: 700; color: #1e293b;">Analyse Prédictive</span>
    </div>
    """, unsafe_allow_html=True)
    
    # DIAGNOSTIC CORRIGÉ
    if prediction[0] == 1:
        st.markdown(f"""
        <div class="diagnosis-card malicious">
            <div class="diagnosis-title">
                <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round" style="vertical-align: middle; margin-right: 6px;"><path d="M10.29 3.86L1.82 18a2 2 0 0 0 1.71 3h16.94a2 2 0 0 0 1.71-3L13.71 3.86a2 2 0 0 0-3.42 0z"></path><line x1="12" y1="9" x2="12" y2="13"></line><line x1="12" y1="17" x2="12.01" y2="17"></line></svg>
                Tumeur Maligne Détectée
            </div>
            <div class="diagnosis-desc">Les caractéristiques des noyaux cellulaires saisies indiquent de fortes similitudes avec des échantillons malins (cancer du sein).</div>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown(f"""
        <div class="diagnosis-card benign">
            <div class="diagnosis-title">
                <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round" style="vertical-align: middle; margin-right: 6px;"><path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"></path></svg>
                Tumeur Bénigne Détectée
            </div>
            <div class="diagnosis-desc">Les caractéristiques des noyaux cellulaires saisies indiquent des similitudes avec des échantillons sains ou non cancéreux.</div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("<div style='margin-top:20px;'></div>", unsafe_allow_html=True)
    
    # Rendu des probabilités
    st.write(f"**Probabilité de tumeur bénigne :** {prob_benign:.2%}")
    st.progress(prob_benign)
    
    st.write(f"**Probabilité de tumeur maligne :** {prob_malignant:.2%}")
    st.progress(prob_malignant)
    
    st.markdown("""
    <div style="background-color: rgba(217, 119, 6, 0.05); border: 1px solid rgba(217, 119, 6, 0.15); border-radius: 8px; padding: 12px; font-size: 0.8rem; color: #b45309; margin-top: 25px; line-height: 1.4;">
        <strong>Information Légale Clinique :</strong><br>
        Cette application a été développée dans le but de fournir une analyse prédictive automatisée basée sur des métriques de noyaux cellulaires (WBCD). Les prédictions fournies ne remplacent en aucun cas l'analyse d'un oncologue ou un diagnostic pathologique officiel.
    </div>
    """, unsafe_allow_html=True)

# ----------------- FONCTION PRINCIPALE -----------------
def main():
    st.set_page_config(
        page_title="Diagnostic Prédictif - Cancer du Sein",
        page_icon=":microscope:",
        layout='wide',
        initial_sidebar_state='expanded'
    )
    
    # Lecture portable de style.css
    style_path = os.path.join(BASE_DIR, "style.css")
    try:
        with open(style_path, "r", encoding="utf-8") as f:
            st.markdown("<style>{}</style>".format(f.read()), unsafe_allow_html=True)
    except FileNotFoundError:
        pass
    
    # En-tête principal de la page
    st.markdown("""
    <div style="display: flex; align-items: center; gap: 16px; margin-top: -30px; margin-bottom: 5px;">
        <svg width="44" height="44" viewBox="0 0 24 24" fill="none" stroke="#e11d48" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round" style="filter: drop-shadow(0 0 8px rgba(225, 29, 72, 0.15));">
            <path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"></path>
            <path d="M8.5 10a3.5 3.5 0 1 1 7 0"></path>
        </svg>
        <div>
            <h1 style="margin: 0; padding: 0; font-size: 2.2rem; font-weight: 800; background: linear-gradient(135deg, #0f172a 40%, #881337 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent; letter-spacing: -0.03em;">
                Diagnostic du Cancer du Sein
            </h1>
            <p style="margin: 4px 0 0 0; padding: 0; color: #475569; font-size: 1rem; font-weight: 500;">
                Modélisation Prédictive & Analyse de Noyaux Cellulaires (WBCD)
            </p>
        </div>
    </div>
    <hr>
    """, unsafe_allow_html=True)
    
    # Chargement global de la barre latérale pour la console de contrôle
    input_data = add_sidebar()

    # Onglets d'utilisation
    tab_about, tab_single, tab_batch = st.tabs([
        "Présentation & Contexte Clinique", 
        "Diagnostic Individuel (FNA)", 
        "Diagnostic en Lot (Fichier CSV)"
    ])
    
    with tab_about:
        col_left, col_right = st.columns([7, 5])
        
        with col_left:
            st.markdown("""<div class="presentation-section">
<div style="display: flex; align-items: center; gap: 8px; margin-bottom: 12px; margin-top: 5px;">
<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="#2563eb" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><path d="M12 2L2 7l10 5 10-5-10-5zM2 17l10 5 10-5M2 12l10 5 10-5"></path></svg>
<span style="font-size: 1.25rem; font-weight: 800; color: #0f172a;">Le Projet & Contexte Clinique</span>
</div>
<div class="clinical-info-box">
<h3>Qu'est-ce que l'analyse par cytoponction (FNA) ?</h3>
<p style="font-size: 0.88rem; line-height: 1.5; color: #475569; margin-bottom: 12px;">
La cytoponction à l'aiguille fine (<b>Fine Needle Aspiration - FNA</b>) est une procédure de biopsie rapide et peu invasive consistant à prélever un échantillon de cellules directement dans une masse mammaire suspecte. 
</p>
<p style="font-size: 0.88rem; line-height: 1.5; color: #475569; margin-bottom: 0;">
L'échantillon extrait est ensuite numérisé au microscope. Les images numériques des noyaux cellulaires sont traitées par ordinateur pour extraire <b>10 caractéristiques géométriques clés</b> (rayon, concavité, régularité, etc.). L'algorithme d'apprentissage automatique évalue ces mesures pour classer instantanément la tumeur comme bénigne ou maligne.
</p>
</div>
</div>

<div class="presentation-section">
<div style="display: flex; align-items: center; gap: 8px; margin-bottom: 10px;">
<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="#2563eb" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"></circle><line x1="12" y1="16" x2="12" y2="12"></line><line x1="12" y1="8" x2="12.01" y2="8"></line></svg>
<span style="font-size: 1.25rem; font-weight: 800; color: #0f172a;">Exploration des 10 Paramètres Biologiques</span>
</div>
<p style="font-size: 0.88rem; color: #475569; margin-top: -5px; margin-bottom: 15px;">
Les mesures proviennent du jeu de données clinique mondialement reconnu <b>Wisconsin Breast Cancer Dataset (WBCD)</b>. Pour chaque échantillon de tumeur, l'ordinateur évalue la moyenne, l'erreur standard et la valeur extrême (pire cas) de ces 10 mesures, totalisant ainsi 30 variables :
</p>

<div class="feature-grid">
<div class="feature-card">
<div class="feature-card-title">Rayon (Radius)</div>
<div class="feature-card-desc">Distance moyenne du centre aux contours externes du noyau.</div>
</div>
<div class="feature-card">
<div class="feature-card-title">Texture</div>
<div class="feature-card-desc">Variabilité de l'intensité des niveaux de gris sur l'image.</div>
</div>
<div class="feature-card">
<div class="feature-card-title">Périmètre & Aire</div>
<div class="feature-card-desc">Mesures de la taille et de la surface du noyau cellulaire.</div>
</div>
<div class="feature-card">
<div class="feature-card-title">Lissage (Smoothness)</div>
<div class="feature-card-desc">Degré de régularité et de lissage du contour nucléaire.</div>
</div>
<div class="feature-card">
<div class="feature-card-title">Compacité (Compactness)</div>
<div class="feature-card-desc">Indice de déformation calculé selon le périmètre et l'aire.</div>
</div>
<div class="feature-card">
<div class="feature-card-title">Concavité & Points Concaves</div>
<div class="feature-card-desc">Sévérité et nombre de creux identifiés sur le contour.</div>
</div>
<div class="feature-card">
<div class="feature-card-title">Symétrie</div>
<div class="feature-card-desc">Régularité spatiale bilatérale de la forme du noyau.</div>
</div>
<div class="feature-card">
<div class="feature-card-title">Dimension Fractale</div>
<div class="feature-card-desc">Complexité géométrique microscopique des contours cellulaires.</div>
</div>
</div>
</div>""", unsafe_allow_html=True)
            
        with col_right:
            st.markdown("""<div class="presentation-section">
<div style="display: flex; align-items: center; gap: 8px; margin-bottom: 12px; margin-top: 5px;">
<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="#2563eb" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><polygon points="12 2 2 7 12 12 22 7 12 2"></polygon><polyline points="2 17 12 22 22 17"></polyline><polyline points="2 12 12 17 22 12"></polyline></svg>
<span style="font-size: 1.25rem; font-weight: 800; color: #0f172a;">Performance et Entraînement de l'IA</span>
</div>

<div class="kpi-container">
<div class="kpi-card">
<div class="kpi-value">97,37%</div>
<div class="kpi-label">Précision (Accuracy)</div>
<div class="kpi-desc">Taux de réussite global du modèle sur des échantillons tests externes non vus lors de sa phase d'apprentissage.</div>
</div>
<div class="kpi-card">
<div class="kpi-value emerald">95,83%</div>
<div class="kpi-label">Sensibilité (Recall)</div>
<div class="kpi-desc">Capacité du modèle à identifier les vrais cas positifs (tumeurs malignes), un critère majeur en dépistage clinique.</div>
</div>
<div class="kpi-card">
<div class="kpi-value">98,25%</div>
<div class="kpi-label">Spécificité</div>
<div class="kpi-desc">Aptitude du modèle à diagnostiquer correctement les cas négatifs (tumeurs bénignes), évitant le sur-traitement.</div>
</div>
<div class="kpi-card">
<div class="kpi-value rose">99,12%</div>
<div class="kpi-label">ROC AUC</div>
<div class="kpi-desc">Aire sous la courbe ROC, mesurant le pouvoir de discrimination probabiliste entre cellules saines et cancéreuses.</div>
</div>
</div>

<div class="clinical-info-box" style="border-left-color: #e11d48;">
<h3>Détails Techniques du Modèle</h3>
<p style="font-size: 0.8rem; line-height: 1.5; color: #475569; margin-bottom: 0;">
L'algorithme utilisé est une <b>Régression Logistique</b> (L2 Regularization), entraîné avec Scikit-Learn.
Toutes les variables sont normalisées via standardisation (z-score) pour pallier les disparités physiques d'échelle (ex: aires nucléaires pouvant atteindre plus de 1000 µm² versus dimensions fractales inférieures à 0.1).
</p>
</div>

<div class="clinical-info-box" style="border-left-color: #059669; margin-bottom: 0;">
<h3>Comment démarrer l'exploration ?</h3>
<ul style="font-size: 0.8rem; line-height: 1.5; color: #475569; padding-left: 18px; margin-bottom: 0; margin-top: 5px;">
<li style="margin-bottom: 4px;">Naviguez vers l'onglet <b>Diagnostic Individuel</b> pour ajuster les 30 curseurs de mesures cellulaires.</li>
<li style="margin-bottom: 4px;">Utilisez l'un des <b>presets de la console</b> à gauche ("Exemple Bénin", "Exemple Malin") pour importer en un clic des profils patients réels.</li>
<li>Sélectionnez l'onglet <b>Diagnostic en Lot</b> pour soumettre directement un fichier de données CSV complet et en extraire le diagnostic groupé.</li>
</ul>
</div>
</div>""", unsafe_allow_html=True)
            
    with tab_single:
        # Division de l'espace principal
        col_chart, col_pred = st.columns([5, 4])
        
        with col_chart:
            st.markdown("""
            <div style="display: flex; align-items: center; gap: 8px; margin-bottom: 12px; margin-top: 5px;">
                <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="#2563eb" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><line x1="18" y1="20" x2="18" y2="10"></line><line x1="12" y1="20" x2="12" y2="4"></line><line x1="6" y1="20" x2="6" y2="14"></line></svg>
                <span style="font-size: 1.15rem; font-weight: 700; color: #1e293b;">Visualisation des Mesures Nucléaires (Échelle Normalisée)</span>
            </div>
            """, unsafe_allow_html=True)
            
            radar_chart = get_radar_chart(input_data)
            st.plotly_chart(radar_chart, use_container_width=True)
            
        with col_pred:
            with st.container(border=True):
                add_predictions(input_data)
                
    with tab_batch:
        st.markdown("""
        <div style="display: flex; align-items: center; gap: 10px; margin-top: 5px; margin-bottom: 15px;">
            <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="#2563eb" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
                <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"></path>
                <polyline points="14 2 14 8 20 8"></polyline>
                <line x1="16" y1="13" x2="8" y2="13"></line>
                <line x1="16" y1="17" x2="8" y2="17"></line>
                <polyline points="10 9 9 9 8 9"></polyline>
            </svg>
            <span style="font-size: 1.25rem; font-weight: 700; color: #1e293b;">Téléverser un fichier patient en lot</span>
        </div>
        <p style="font-size:0.9rem; color:#64748b; margin-top:-5px;">Importez un fichier CSV contenant les 30 mesures caractéristiques pour prédire en une seule fois les diagnostics de plusieurs patients.</p>
        """, unsafe_allow_html=True)
        
        uploaded_csv = st.file_uploader("Sélectionnez votre fichier CSV patient :", type="csv")
        
        if uploaded_csv is not None:
            try:
                # Lire le CSV
                input_df = pd.read_csv(uploaded_csv)
                
                # Charger le modèle et le scaler
                model_path = os.path.join(BASE_DIR, "model.pkl")
                scaler_path = os.path.join(BASE_DIR, "scaler.pkl")
                model = pickle.load(open(model_path, "rb"))
                scaler = pickle.load(open(scaler_path, "rb"))
                
                # Identifier les colonnes nécessaires
                required_cols = list(data.columns)
                required_cols.remove('diagnosis')
                
                missing_cols = [c for c in required_cols if c not in input_df.columns]
                
                if missing_cols:
                    st.error(f"Le fichier CSV importé est incomplet. Il manque les colonnes de mesures suivantes : {', '.join(missing_cols)}")
                else:
                    # Aligner les colonnes exactement dans le même ordre que pour l'entraînement
                    X_batch = input_df[required_cols]
                    
                    # Normaliser et prédire
                    X_batch_scaled = scaler.transform(X_batch)
                    batch_predictions = model.predict(X_batch_scaled)
                    batch_probs = model.predict_proba(X_batch_scaled)
                    
                    # Ajouter les colonnes de diagnostic
                    output_df = input_df.copy()
                    output_df['Diagnostic Prédiction'] = np.where(batch_predictions == 1, 'Maligne (Cancer)', 'Bénigne (Sain)')
                    output_df['Confiance Tumeur Maligne'] = batch_probs[:, 1]
                    output_df['Confiance Tumeur Bénigne'] = batch_probs[:, 0]
                    
                    st.success(f"Traitement terminé avec succès ! {len(output_df)} enregistrements analysés.")
                    
                    # Affichage des résultats
                    st.write("**Résultats du Diagnostic en Lot :**")
                    st.dataframe(output_df[['Diagnostic Prédiction', 'Confiance Tumeur Maligne', 'Confiance Tumeur Bénigne'] + required_cols[:5]], use_container_width=True)
                    
                    # Téléchargement du CSV enrichi
                    csv_data = output_df.to_csv(index=False).encode('utf-8')
                    st.download_button(
                        label="Télécharger les diagnostics générés (CSV)",
                        data=csv_data,
                        file_name="diagnostics_patients_generes.csv",
                        mime="text/csv"
                    )
            except Exception as e:
                st.error(f"Une erreur est survenue lors de l'analyse du fichier CSV : {str(e)}")
            
    # Pied de page
    st.markdown("""
    <hr>
    <center style='font-size: 0.85rem; color: #64748b; margin-top: 15px;'>
        Développé avec <b>Streamlit</b> & <b>Scikit-Learn</b> | MLOps Classification & WBCD Clinical Analysis
    </center>
    """, unsafe_allow_html=True)

if __name__ == '__main__':
    main()
