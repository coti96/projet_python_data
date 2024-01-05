import plotly.express as px
import pandas as pd
from data import prepare_data
import locale

locale.setlocale(locale.LC_TIME, 'fr_FR')

def prepare_data_graphicLine(df):
    """
    Prépare les données pour la création d'un graphique linéaire montrant l'évolution des prix des carburants.

    Cette fonction transforme le DataFrame en format approprié pour un graphique linéaire, incluant 
    la conversion des dates, le filtrage des données des trois dernières années, et le calcul 
    des moyennes mensuelles des prix par type de carburant.

    Args:
        df (pandas.DataFrame): DataFrame contenant les données des prix du carburant.

    Returns:
        pandas.DataFrame: DataFrame transformé, prêt pour la visualisation linéaire.
    """
  
     # Convertir les colonnes de date en format datetime
    date_columns = ['gazole_maj', 'sp95_maj', 'e85_maj', 'e10_maj', 'sp98_maj']
    for col in date_columns:
        df[col] = pd.to_datetime(df[col], utc=True)

        

    # Supprimer les lignes où toutes les colonnes de date sont NaN ou NaT
    df = df.dropna(subset=date_columns, how='all')

    # Filtrer les données pour les trois dernières années
    six_month_ago = (pd.Timestamp.now(tz='UTC') - pd.DateOffset(days=15)).normalize()
    df = df[df['gazole_maj'] >= six_month_ago]

    # Extraire le mois et l'année de la colonne 'gazole_maj'
    df['day'] = df['gazole_maj'].dt.day
    df['year'] = df['gazole_maj'].dt.year
    df['month'] = df['gazole_maj'].dt.month


    # Grouper par jour, mois et année, puis calculer le prix moyen
    df_grouped = df.groupby(['day', 'month', 'year'])[date_columns + ['gazole_prix', 'sp95_prix', 'e85_prix', 'e10_prix', 'sp98_prix']].mean().reset_index()

    # Créer une nouvelle colonne pour l'axe des abscisses qui combine le jour, le mois et l'année
    df_grouped['date'] = pd.to_datetime(df_grouped[['year', 'month', 'day']]).dt.strftime('%d %B %Y')

    df_grouped = df_grouped.rename(columns={
        'gazole_prix': 'Gazole',
        'sp95_prix': 'SP95',
        'e85_prix': 'E85',
        'e10_prix': 'E10',
        'sp98_prix': 'SP98'
    })

    # Trier le DataFrame par date
    df_grouped = df_grouped.sort_values('date')

    # Retourner le DataFrame groupé
    return df_grouped

def create_graphic_line(df):
    """ Crée un graphique linéaire montrant l'évolution mensuelle des prix moyens des différents carburants.

    Cette fonction utilise un DataFrame préparé pour générer un graphique linéaire affichant 
    les tendances des prix des carburants sur les trois dernières années.

    Args:
        df (pandas.DataFrame): DataFrame contenant les données des prix du carburant.

    Returns:
        plotly.graph_objs._figure.Figure: Un objet Figure Plotly représentant le graphique linéaire.
    """

    # Préparer les données
    df_grouped = prepare_data_graphicLine(df)

    # Créer le graphique à courbes
    fig = px.line(
        df_grouped, 
        x='date', 
        y=['Gazole', 'SP95', 'E85', 'E10', 'SP98'],
        labels={'value': 'Prix moyen (€/L)', 'variable': 'Type de Carburant', 'date': 'Date'},
        color_discrete_sequence=px.colors.qualitative.Vivid
    )

    # Définir la plage de l'axe des ordonnées et personnaliser le graphique
    fig.update_yaxes(range=[0.5, 2.5], title='Prix moyen (€/L)')
    fig.update_layout(
        title='Évolution Quotidienne du Prix des Carburants en France',
        title_font_size=24,
        xaxis=dict(
            title='Date',
            title_font_size=18,
            tickangle=-45
        ),
        yaxis_title='Prix Moyen (€/L)',
        yaxis_title_font_size=18,
        legend_title='Carburants',
        legend_title_font_size=18,
        legend_font_size=16,
        margin=dict(l=50, r=50, t=100, b=50)
    )

    return fig
