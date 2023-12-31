from dash import dcc, html
from app import create_app
from data import prepare_data_histogram
from components.histogram import create_histogram



# Créer l'instance de l'application Dash
app = create_app()

# Préparer les données pour l'histogramme
df_grouped = prepare_data_histogram()
# Créer l'histogramme
fig = create_histogram(df_grouped)



# Définir l'agencement de l'application
app.layout = html.Div(children=[
    dcc.Graph(figure=fig)
])

# Lancer le serveur Flask
if __name__ == '__main__':
    app.run_server(debug=True)
