import pandas as pd
import plotly.express as px
from data import prepare_data

def prepare_coordinates(df, coord_column='geom'):
    # Séparer les coordonnées en deux nouvelles colonnes 'latitude' et 'longitude'
    df[['latitude', 'longitude']] = df[coord_column].str.split(',', expand=True).astype(float)
    return df

def plot_gas_stations():
    df = prepare_data()
    # Préparer les coordonnées
    df = prepare_coordinates(df)


    # Créer la carte avec Plotly
    fig = px.scatter_mapbox(
        df, 
        lat='latitude', 
        lon='longitude', 
        zoom=5, 
        center={"lat": 46.2276, "lon": 2.2137},  # Centre de la France
        mapbox_style="open-street-map"
    )

    fig.update_layout(
        title='Stations de carburants en France',
        title_font_size=24,
        margin=dict(l=30, r=30, t=50, b=30),  # Ajuster la marge ici
        mapbox=dict(bearing=0, pitch=0)
    )

    return fig

    


