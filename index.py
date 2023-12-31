from dash import dcc, html
from app import create_app
from data import prepare_data
from components.histogram import prepare_data_histogram, create_histogram
from components.map import prepare_coordinates, plot_gas_stations

# Créer l'instance de l'application Dash
app = create_app()

# Créer  l'histogramme
fig_histogram = create_histogram()

# Créer la carte
fig_map = plot_gas_stations()

# Définir l'agencement de l'application
app.layout = html.Div(children=[
    html.Div([
        dcc.Graph(figure=fig_histogram),
    ], style={'width': '50%', 'display': 'inline-block'}),  # Histogramme à gauche
    html.Div([
        dcc.Graph(figure=fig_map),
    ], style={'width': '50%', 'display': 'inline-block'}),  # Carte à droite
])


# Lancer le serveur Flask
if __name__ == '__main__':
    app.run_server(debug=True)
