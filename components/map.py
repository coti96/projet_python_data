import pandas as pd
import plotly.express as px
from data import prepare_data

def prepare_coordinates(df, coord_column='geom'):
    """
    Sépare les coordonnées géographiques en deux colonnes distinctes pour la latitude et la longitude.

    Cette fonction prend en entrée un DataFrame contenant une colonne de coordonnées géographiques
    combinées et les sépare en deux colonnes distinctes pour faciliter la cartographie.

    Args:
        df (pandas.DataFrame): Le DataFrame contenant les coordonnées géographiques.
        coord_column (str, optional): Le nom de la colonne contenant les coordonnées géographiques. 
                                      Par défaut à 'geom'.

    Returns:
        pandas.DataFrame: Le DataFrame modifié avec les colonnes 'latitude' et 'longitude' ajoutées.
    """
    
    # Séparer les coordonnées en deux nouvelles colonnes 'latitude' et 'longitude'
    df[['latitude', 'longitude']] = df[coord_column].str.split(',', expand=True).astype(float)
    return df

def plot_gas_stations(df):
    """
    Crée une carte Plotly montrant l'emplacement des stations de carburants en France.

    Cette fonction prépare les coordonnées des stations de carburants et utilise Plotly
    pour créer une visualisation cartographique interactive des emplacements.

    Args:
        df (pandas.DataFrame): DataFrame contenant les données des stations de carburants,
                               incluant leurs coordonnées géographiques.

    Returns:
        plotly.graph_objs._figure.Figure: Un objet Figure Plotly représentant la carte des stations de carburants.
    """
   

    # Préparer les coordonnées
    df = prepare_coordinates(df)


    # Créer la carte avec Plotly
    fig = px.scatter_mapbox(
        df, 
        lat='latitude', 
        lon='longitude', 
        zoom=4, 
        center={"lat": 46.2276, "lon": 2.2137},  # Centre de la France
        mapbox_style="open-street-map"
    )

    fig.update_layout(
        title='Stations de carburants en France',
        title_y=0.95,
        title_font_size=20,
        margin=dict(l=30, r=30, t=50, b=30),  
        mapbox=dict(bearing=0, pitch=0)
    )

    return fig

    


