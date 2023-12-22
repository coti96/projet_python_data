import pandas as pd
import plotly.express as px
from dash import Dash, dcc, html
from dash.dependencies import Input, Output

app = Dash(__name__)

# Créer un dataframe à partir d'un fichier csv
df = pd.read_csv('data.csv')

# Définir les colonnes pour la comparaison
df = df[['id', 'nom', 'prenom', 'age', 'region', 'code_region']]

# Créer un graphique interactif avec Plotly
fig = px.scatter(df, x="age", y="region", color="code_region")

# Ajouter le graphique à l'application Dash
app.layout = html.Div([
    dcc.Graph(figure=fig),
    html.Label('Choisissez une région'),
    dcc.Dropdown(
        id='region-dropdown',
        options=[{'label': i, 'value': i} for i in df['region'].unique()],
        value='Toutes les régions'
    ),
    dcc.Graph(id='output-graph')
])

@app.callback(
    Output('output-graph', 'figure'),
    [Input('region-dropdown', 'value')]
)
def update_graph(region):
    if region == 'Toutes les régions':
        return px.scatter(df, x="age", y="region", color="code_region")
    else:
        df_filtered = df[df['region'] == region]
        return px.scatter(df_filtered, x="age", y="region", color="code_region")

if __name__ == '__main__':
    app.run_server(debug=True)
