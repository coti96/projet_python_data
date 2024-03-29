import plotly.express as px
import pandas as pd
from data import prepare_data

def prepare_data_histogram(df):
    """
    Prépare les données pour la création d'un histogramme par trimestre.

    Cette fonction filtre et transforme le DataFrame pour les analyses trimestrielles
    des prix du carburant pour l'année 2023. Elle crée des colonnes supplémentaires pour
    le regroupement par trimestre et calcule le prix moyen de chaque type de carburant.

    Args:
        df (pandas.DataFrame): DataFrame contenant les données des prix du carburant.

    Returns:
        pandas.DataFrame: DataFrame transformé avec des données regroupées et moyennées par trimestre.
    """
    
    # Convertir les colonnes de date en format datetime
    date_columns = ['gazole_maj', 'sp95_maj', 'e85_maj', 'e10_maj', 'sp98_maj']
    for col in date_columns:
        df[col] = pd.to_datetime(df[col], utc=True)

    # Supprimer les lignes où toutes les colonnes de date sont NaN
    df = df.dropna(subset=date_columns, how='all')

    # Filtrer les données pour l'année 2023 uniquement
    start_date = pd.Timestamp('2023-01-01', tz='UTC')
    end_date = pd.Timestamp('2023-12-31', tz='UTC')
    filter_condition = ((df['gazole_maj'] >= start_date) & (df['gazole_maj'] <= end_date))
    df = df[filter_condition]

    
    # Créer une colonne 'trimestre' à partir de la colonne 'gazole_maj'
    df['trimestre'] = df['gazole_maj'].dt.to_period('Q')

    # Mapper les périodes trimestrielles aux chaînes de caractères et à un ordre numérique
    trimestre_mapper = {
        '2023Q1': ('janvier-mars 2023', 1),
        '2023Q2': ('avril-juin 2023', 2),
        '2023Q3': ('juillet-septembre 2023', 3),
        '2023Q4': ('octobre-décembre 2023', 4)
    }
    # Créer deux nouvelles colonnes à partir de la colonne 'trimestre'
    # Une colonne avec les chaînes de caractères 
    df['trimestre_str'] = df['trimestre'].astype(str).map(lambda x: trimestre_mapper[x][0])

    # et une autre avec les ordres numériques
    df['trimestre_order'] = df['trimestre'].astype(str).map(lambda x: trimestre_mapper[x][1])

    # Grouper par trimestre_str et calculer le prix moyen
    df_grouped = df.groupby(['trimestre_str', 'trimestre_order'])[['gazole_prix', 'sp95_prix', 'e85_prix', 'e10_prix', 'sp98_prix']].mean().reset_index()

    # Trier par l'ordre numérique des trimestres et supprimer la colonne de tri
    df_grouped = df_grouped.sort_values('trimestre_order').drop('trimestre_order', axis=1)
    
    df_grouped = df_grouped.rename(columns={
        'gazole_prix': 'Gazole',
        'sp95_prix': 'SP95',
        'e85_prix': 'E85',
        'e10_prix': 'E10',
        'sp98_prix': 'SP98'
    })
  
    return df_grouped


def create_histogram(df):
    """
    Crée un histogramme des prix moyens des carburants par trimestre.

    Cette fonction utilise un DataFrame préparé pour générer un graphique à barres
    qui montre l'évolution des prix moyens des différents carburants au fil des trimestres de l'année 2023.

    Args:
        df (pandas.DataFrame): DataFrame contenant les données des prix du carburant.

    Returns:
        plotly.graph_objs._figure.Figure: Un objet Figure Plotly représentant l'histogramme.
    """
    
    # Préparer les données
    df_grouped = prepare_data_histogram(df)
    # Créer l'histogramme
    fig = px.bar(
        df_grouped, 
        x='trimestre_str', 
        y=['Gazole', 'SP95', 'E85', 'SP98','E10'], 
        barmode='group', 
        labels={'value': 'Prix moyen (€/L)', 'variable': 'Type de Carburant', 'trimestre_str': 'Trimestre'},
        color_discrete_sequence=px.colors.qualitative.Vivid
    )

    # Définir la plage de l'axe des ordonnées
    fig.update_yaxes(range=[0.5, 2.5], title='Prix moyen (€/L)')

    # Personnaliser l'histogramme
    fig.update_layout(
        title='Évolution du Prix des Carburants en France en 2023',
        title_font_size=20,
        title_y=0.95,
        xaxis=dict(
            title='Trimestre',
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

    return fig
