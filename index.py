from dash import dcc, html
from app import create_app
from data import prepare_data
from components.histogram import prepare_data_histogram, create_histogram
from components.map import prepare_coordinates, plot_gas_stations

# Créer l'instance de l'application Dash
app = create_app()

app.css.append_css({'external_url': '/assets/style.css'})

# Créer  l'histogramme
fig_histogram = create_histogram()

# Créer la carte
fig_map = plot_gas_stations()

# Définir l'agencement de l'application
app.layout = html.Div(children=[
    html.H1("Dashboard Carburants en France", 
            style={
                'textAlign': 'center', 
                'color': '#ffffff',
                'font-family': 'Roboto, sans-serif',  # Choisir la police de ton choix
                'font-size': '36px',  # Ajuster la taille de la police
                'font-weight': 'bold',  # Rendre le texte en gras si nécessaire
            }
    ),  # Ajout du titre
    html.Div([
        dcc.Graph(
            figure=fig_histogram,
            style={
                'backgroundColor': '#4242b6',
                'border': '2px solid #92959B',
                'padding': '10px',
                'border-radius': '10px',
            }
        ),
    ], style={'width': '45%', 'display': 'inline-block', 'margin': '20px 0 20px 60px'}),  # Histogramme à gauche
    html.Div([
        dcc.Graph(
            figure=fig_map,
            style={
                'backgroundColor': '#4242b6',
                'border': '2px solid #92959B',
                'padding': '10px',
                'border-radius': '10px',
            }
        ),
    ], style={'width': '45%', 'display': 'inline-block', 'margin': '20px 60px 20px 0'}),  # Carte à droite
])


# Lancer le serveur Flask
if __name__ == '__main__':
    app.run_server(debug=True)
