import plotly.express as px
import pandas as pd
from data import prepare_data


def prepare_data_histogram():
    df = prepare_data()
     # Convertir les colonnes de date en format datetime
    date_columns = ['gazole_maj', 'sp95_maj', 'e85_maj', 'gplc_maj', 'e10_maj', 'sp98_maj']
    for col in date_columns:
        df[col] = pd.to_datetime(df[col], utc=True)

    # Supprimer les lignes où toutes les colonnes de date sont NaN ou NaT
    df = df.dropna(subset=date_columns, how='all')

    # Filtrer les données pour les trois dernières années
    three_years_ago = (pd.Timestamp.now(tz='UTC') - pd.DateOffset(years=3)).normalize()
    df = df[df['gazole_maj'] >= three_years_ago]

    # Extraire le mois et l'année de la colonne 'gazole_maj'
    df['year'] = df['gazole_maj'].dt.year
    df['month'] = df['gazole_maj'].dt.month

    # Grouper par année, mois et code_region, puis calculer le prix moyen
    df_grouped = df.groupby(['year', 'month'])[date_columns + ['gazole_prix', 'sp95_prix', 'e85_prix', 'gplc_prix', 'e10_prix', 'sp98_prix']].mean().reset_index()

    # Créer une nouvelle colonne pour l'axe des abscisses qui combine l'année et le mois
    df_grouped['year_month'] = df_grouped['year'].astype(str) + '-' + df_grouped['month'].astype(str).str.zfill(2)

    # Retourner le DataFrame groupé
    return df_grouped

def create_histogram():

    df_grouped = prepare_data_histogram()
    # Créer l'histogramme
    fig = px.bar(
        df_grouped, 
        x='year_month', 
        y=['gazole_prix', 'sp95_prix', 'e85_prix', 'gplc_prix', 'e10_prix', 'sp98_prix'], 
        barmode='group', 
        labels={'value': 'Prix moyen (€/L)', 'variable': 'Type de Carburant', 'year_month': 'Mois et Année'},
        color_discrete_sequence=px.colors.qualitative.Vivid  # Palette de couleurs personnalisée
    )

    # Définir la plage de l'axe des ordonnées
    fig.update_yaxes(range=[1, 3], title='Prix moyen (€/L)')

    # Personnaliser l'histogramme
    fig.update_layout(
        title='Évolution du Prix des Carburants en France',
        title_font_size=24,
        xaxis=dict(
            title='Mois et Année',
            title_font_size=18,
            tickangle=-45  # Incliner les étiquettes de l'axe des x
        ),
        yaxis_title='Prix Moyen (€/L)',
        yaxis_title_font_size=18,
        legend_title='Carburants',
        legend_title_font_size=18,
        legend_font_size=16,
        margin=dict(l=50, r=50, t=100, b=50)
    )

    # Ajouter des étiquettes de données sur les barres
    fig.update_traces(texttemplate='%{y:.2f} €', textposition='outside')

    return fig

# Exemple d'utilisation :
# df_grouped = prepare_data_histogram()
# fig = create_histogram(df_grouped)
# fig.show()
