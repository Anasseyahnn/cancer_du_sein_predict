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

# ----------------- SIDEBAR -----------------
def add_sidebar():
    st.sidebar.markdown("""
    <div style="display: flex; align-items: center; gap: 8px; margin-bottom: 12px;">
        <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="#2563eb" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="3"></circle><path d="M19.4 15a1.65 1.65 0 0 0 .33 1.82l.06.06a2 2 0 1 1-2.83 2.83l-.06-.06a1.65 1.65 0 0 0-1.82-.33 1.65 1.65 0 0 0-1 1.51V21a2 2 0 0 1-4 0v-.09A1.65 1.65 0 0 0 9 19.4a1.65 1.65 0 0 0-1.82.33l-.06.06a2 2 0 1 1-2.83-2.83l.06-.06a1.65 1.65 0 0 0 .33-1.82 1.65 1.65 0 0 0-1.51-1H3a2 2 0 0 1 0-4h.09A1.65 1.65 0 0 0 4.6 9a1.65 1.65 0 0 0-.33-1.82l-.06-.06a2 2 0 1 1 2.83-2.83l.06.06a1.65 1.65 0 0 0 1.82.33H9a1.65 1.65 0 0 0 1-1.51V3a2 2 0 0 1 4 0v.09a1.65 1.65 0 0 0 1 1.51 1.65 1.65 0 0 0 1.82-.33l.06-.06a2 2 0 1 1 2.83 2.83l-.06.06a1.65 1.65 0 0 0-.33 1.82V9a1.65 1.65 0 0 0 1.51 1H21a2 2 0 0 1 0 4h-.09a1.65 1.65 0 0 0-1.51 1z"></path></svg>
        <span style="font-size: 1.1rem; font-weight: 700; color: #1e293b;">Paramètres des Nuclei</span>
    </div>
    """, unsafe_allow_html=True)
    
    data = get_clean_data()
    
    slider_labels = [
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
    
    for label, key in slider_labels:
        input_dict[key] = st.sidebar.slider(
            label, 
            min_value=float(0),
            max_value=float(data[key].max()),
            value = float(data[key].mean())
        )
        
    return input_dict

# ----------------- NORMALISATION -----------------
def get_scaled_values(input_dict):
    data = get_clean_data()
    X = data.drop(["diagnosis"], axis = 1)
    
    scaled_dict = {}
    for key, value in input_dict.items():
        max_val = X[key].max()
        min_val = X[key].min()
        # Éviter la division par zéro
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
        st.error("Les fichiers du modèle (model.pkl ou scaler.pkl) sont introuvables. Veuillez d'abord exécuter 'python cancer.py' pour entraîner le modèle.")
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
    
    # DIAGNOSTIC CORRIGÉ : prediction[0] == 1 signifie Tumeur Maligne
    if prediction[0] == 1:
        st.markdown(f"""
        <div class="diagnosis-card malicious">
            <div class="diagnosis-title">⚠️ Tumeur Maligne Détectée</div>
            <div class="diagnosis-desc">Les caractéristiques des noyaux cellulaires saisies indiquent de fortes similitudes avec des échantillons malins (cancer du sein).</div>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown(f"""
        <div class="diagnosis-card benign">
            <div class="diagnosis-title">🛡️ Tumeur Bénigne Détectée</div>
            <div class="diagnosis-desc">Les caractéristiques des noyaux cellulaires saisies indiquent des similitudes avec des échantillons sains ou non cancéreux.</div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("<div style='margin-top:20px;'></div>", unsafe_allow_html=True)
    
    # Rendu des probabilités cliniques avec barres de progression
    st.write(f"**Probabilité de tumeur bénigne :** {prob_benign:.2%}")
    st.progress(prob_benign)
    
    st.write(f"**Probabilité de tumeur maligne :** {prob_malignant:.2%}")
    st.progress(prob_malignant)
    
    # Avertissement légal
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
        page_icon="⚖️",
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
    
    # Chargement de la sidebar
    input_data = add_sidebar()
    
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
    
    st.markdown("""
    <p style="font-size: 0.95rem; line-height: 1.6; color: #475569; margin-top: -10px; margin-bottom: 25px;">
        Cette console clinique utilise une classification par <b>Régression Logistique</b> pour prédire si une tumeur mammaire est <b>bénigne</b> ou <b>maligne</b>. Les données sont issues de mesures d'aspiration à l'aiguille fine (FNA) de masses mammaires. Ajustez les curseurs dans le panneau latéral pour visualiser l'impact des mesures nucléaires sur le diagnostic.
    </p>
    """, unsafe_allow_html=True)
    
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
            
    # Pied de page
    st.markdown("""
    <hr>
    <center style='font-size: 0.85rem; color: #64748b; margin-top: 15px;'>
        Développé avec <b>Streamlit</b> & <b>Scikit-Learn</b> | MLOps Classification & WBCD Clinical Analysis
    </center>
    """, unsafe_allow_html=True)

if __name__ == '__main__':
    main()
