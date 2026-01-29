import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px

# ============================================================================
# CONFIGURATION PAGE
# ============================================================================

st.set_page_config(
    page_title="🎵 Spotify Trends Dashboard",
    page_icon="🎵",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS
st.markdown("""
    <style>
        body { background: #fff5f7; }
        .main { background: #fff5f7; }
        
        /* Style des tables */
        [data-testid="dataframe"] {
            background: white !important;
            border: 2px solid #ff6b9d !important;
            border-radius: 10px !important;
        }
    </style>
""", unsafe_allow_html=True)

# ============================================================================
# HEADER ÉLÉGANT ROSE
# ============================================================================

col1, col2, col3 = st.columns([1, 2, 1])

with col2:
    st.markdown("""
        <div style='text-align: center; padding: 50px 20px; 
                    background: linear-gradient(135deg, #ff6b9d 0%, #c44569 100%); 
                    border-radius: 20px; color: white; box-shadow: 0 10px 30px rgba(255, 107, 157, 0.3);'>
            <h1 style='font-size: 52px; margin: 0; text-shadow: 2px 2px 8px rgba(0,0,0,0.2);'>🎵 SPOTIFY TRENDS 2025</h1>
            <p style='font-size: 20px; margin-top: 15px; opacity: 0.95;'>Tendances Musicales France</p>
            <p style='font-size: 15px; opacity: 0.85; margin-top: 8px;'>Dashboard pour Agence d'Animation d'Événements</p>
        </div>
    """, unsafe_allow_html=True)

st.markdown("")

# ============================================================================
# CHARGER LES DONNÉES
# ============================================================================

@st.cache_data
def load_data():
    df = pd.read_csv('spotify_trends_correct.csv')
    df['streams'] = pd.to_numeric(df['streams'], errors='coerce')
    df['rank'] = pd.to_numeric(df['rank'], errors='coerce')
    df['days_on_chart'] = pd.to_numeric(df['days_on_chart'], errors='coerce')
    
    # PRENDRE SEULEMENT LE PREMIER ARTISTE (avant la virgule)
    df['artist_names'] = df['artist_names'].str.split(',').str[0].str.strip()
    
    return df

df = load_data()

st.divider()

# ============================================================================
# REQUÊTE  : TOP 20 HITS  - TABLE
# ============================================================================

st.markdown("###  TOP 20 HITS - À PASSER EN SOIRÉE")
st.markdown("*Les 20 chansons essentielles pour une soirée réussie*")

top_20_hits = df.nlargest(20, 'streams')[['artist_names', 'track_name', 'streams', 'rank']].reset_index(drop=True)
top_20_hits.index = top_20_hits.index + 1
top_20_hits.index.name = '#'

# Formater les données pour affichage - SEULEMENT Artiste et Chanson
top_20_display = top_20_hits[['artist_names', 'track_name']].copy()
top_20_display.columns = ['Artiste', 'Chanson']

# Centrer le tableau
col_center1, col_center2, col_center3 = st.columns([0.5, 3, 0.5])
with col_center2:
    st.dataframe(
        top_20_display,
        use_container_width=True,
        hide_index=True,
        column_config={
            'Artiste': st.column_config.TextColumn(width=200),
            'Chanson': st.column_config.TextColumn(width=300)
        }
    )

st.markdown("")

st.divider()

# ============================================================================
# REQUÊTE  : TOP 12 CHANSONS DURABLES  - TABLE
# ============================================================================

st.markdown("###  CHANSONS DURABLES - LES HITS QUI RESTENT")
st.markdown("*Chansons qui apparaissent plusieurs fois = restent longtemps en tendance*")

chansons_durables = df.groupby(['artist_names', 'track_name']).agg({
    'rank': 'mean',
    'streams': 'sum'
}).reset_index()

chansons_durables['nb_apparitions'] = df.groupby(['artist_names', 'track_name']).size().values
chansons_durables = chansons_durables[chansons_durables['nb_apparitions'] >= 2]
chansons_durables = chansons_durables.nlargest(10, 'nb_apparitions').reset_index(drop=True)
chansons_durables.index = chansons_durables.index + 1
chansons_durables.index.name = '#'

# Formater pour affichage - SEULEMENT Artiste + Chanson
durables_display = chansons_durables[['artist_names', 'track_name']].copy()
durables_display.columns = ['Artiste', 'Chanson']

# Centrer le tableau
col_center1, col_center2, col_center3 = st.columns([0.5, 3, 0.5])
with col_center2:
    st.dataframe(
        durables_display,
        use_container_width=True,
        hide_index=True,
        column_config={
            'Artiste': st.column_config.TextColumn(width=200),
            'Chanson': st.column_config.TextColumn(width=350)
        }
    )

st.markdown("")

st.divider()

# ============================================================================
# ARTISTES TOP - TABLE
# ============================================================================

st.markdown("### ARTISTES TOP 15")
st.markdown("*Les artistes les plus demandés en soirée*")

artistes_top = df.groupby('artist_names').agg({
    'track_name': 'count',
    'streams': 'sum',
    'rank': 'mean'
}).reset_index()

artistes_top.columns = ['artist_names', 'nb_hits', 'total_streams', 'classement_moyen']
artistes_top = artistes_top.nlargest(15, 'total_streams').reset_index(drop=True)
artistes_top.index = artistes_top.index + 1
artistes_top.index.name = '#'

# Formater - SEULEMENT Artiste + Nb Hits
artistes_display = artistes_top[['artist_names', 'nb_hits']].copy()
artistes_display['nb_hits'] = artistes_display['nb_hits'].apply(lambda x: f"{int(x)}")
artistes_display.columns = ['Artiste', 'Nb Hits']

# Centrer le tableau
col_center1, col_center2, col_center3 = st.columns([0.5, 3, 0.5])
with col_center2:
    st.dataframe(
        artistes_display,
        use_container_width=True,
        hide_index=True,
        column_config={
            'Artiste': st.column_config.TextColumn(width=250),
            'Nb Hits': st.column_config.TextColumn(width=150)
        }
    )

st.markdown("")

st.divider()

# ============================================================================
# LABELS - PIE CHART EN PLEINE LARGEUR
# ============================================================================

st.markdown("###  LABELS DOMINANTS")
st.markdown("*Part de marché par label*")

labels_data = df.groupby('source').agg({
    'artist_names': 'nunique',
    'track_name': 'nunique'
}).reset_index()

labels_data.columns = ['source', 'nb_artistes', 'nb_chansons']
labels_data = labels_data[labels_data['source'].notna()]
labels_data = labels_data[labels_data['source'] != '']
labels_data = labels_data[labels_data['nb_chansons'] > 0]  # Filtrer les 0
labels_data = labels_data.nlargest(10, 'nb_chansons')

# Calculer les pourcentages sur le nombre de chansons
total = labels_data['nb_chansons'].sum()
if total > 0:
    labels_data['percentage'] = (labels_data['nb_chansons'] / total * 100).round(1)
else:
    labels_data['percentage'] = 0

# Palette rose pour pie
rose_palette = [
    '#ff6b9d', '#ff85b3', '#ffb3d9', '#ffc9e1',
    '#c44569', '#d96a8a', '#e084a1', '#ff99b9',
    '#ff7fa8', '#ff5c8e'
]

# Filtrer les données vides pour le pie chart
labels_pie = labels_data[labels_data['nb_chansons'] > 0].copy()

if len(labels_pie) > 0:
    # Créer le pie chart
    fig_labels = go.Figure(data=[go.Pie(
        labels=labels_pie['source'].tolist(),
        values=labels_pie['nb_chansons'].tolist(),
        marker=dict(colors=rose_palette[:len(labels_pie)], line=dict(color='white', width=3)),
        textposition='auto',
        textinfo='label+percent',
        hovertemplate='<b>%{label}</b><br>Chansons: %{value}<br>Part: %{customdata:.1f}%<extra></extra>',
        customdata=labels_pie['percentage'].tolist(),
        hole=0.3
    )])
else:
    fig_labels = go.Figure()

fig_labels.update_layout(
    height=700,
    template='plotly_white',
    font=dict(size=13, family='Arial'),
    margin=dict(l=100, r=100, t=80, b=100),
    title_text='<b>Part de Marché (Top 10 Labels)</b>',
    title_font_size=18,
    paper_bgcolor='white',
    showlegend=True,
    legend=dict(x=1.1, y=1, font=dict(size=11))
)

st.plotly_chart(fig_labels, use_container_width=True)

st.markdown("")

# TABLEAU DES LABELS
col_left, col_right = st.columns(2)

with col_left:
    st.markdown("#### Détails des Labels")
    
    labels_table = labels_data[['source', 'nb_artistes', 'nb_chansons', 'percentage']].copy()
    labels_table.index = labels_table.index + 1
    labels_table.index.name = '#'
    
    labels_display = labels_table.copy()
    labels_display['percentage'] = labels_display['percentage'].apply(lambda x: f"{x:.1f}%")
    labels_display['nb_artistes'] = labels_display['nb_artistes'].apply(lambda x: f"{int(x)}")
    labels_display['nb_chansons'] = labels_display['nb_chansons'].apply(lambda x: f"{int(x)}")
    labels_display.columns = ['Label', 'Nb Artistes', 'Nb Chansons', 'Part Marché']
    
    st.dataframe(
        labels_display,
        use_container_width=True,
        hide_index=True,
        column_config={
            'Label': st.column_config.TextColumn(width=180),
            'Nb Artistes': st.column_config.TextColumn(width=100),
            'Nb Chansons': st.column_config.TextColumn(width=100),
            'Part Marché': st.column_config.TextColumn(width=100)
        }
    )

with col_right:
    st.markdown("#### 📊 Statistiques Labels")
    
    if len(labels_data) > 0:
        st.metric(" Nombre de Labels", len(labels_data))
        st.metric(" Label Dominant", labels_data.iloc[0]['source'])
        st.metric(" Part du Leader", f"{labels_data.iloc[0]['percentage']:.1f}%")
    else:
        st.warning("Aucune donnée de label disponible")
