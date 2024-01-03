from dash.exceptions import PreventUpdate
from dash import dcc, html,  Input, Output, State
from app import create_app
from components.comparison import prepare_data_comparison
from components.graphic_line import create_graphic_line
from data import prepare_data
from components.histogram import  create_histogram
from components.map import plot_gas_stations


# Créer l'instance de l'application Dash
app = create_app()

app.css.append_css({'external_url': '/assets/style.css'})

# Préparer les données
df = prepare_data()

# Créer  l'histogramme
fig_histogram = create_histogram(df)

# Creer le graphique
fig_graphic = create_graphic_line(df)

# Créer la carte
fig_map = plot_gas_stations(df)

# Définir les options de formulaire
carburants = ['gazole', 'sp95', 'sp98', 'e10', 'e85']
departements = ['01', '02', '03', '04', '05', '06', '07', '08', '09', '10','11', '12', '13', '14', '15', '16', '17', '18', '19','2A', '2B' '21', '22', '23', '24', '25', '26', '27', '28', '29','30', '31', '32', '33', '34', '35', '36', '37', '38', '39','40', '41', '42', '43', '44', '45', '46', '47', '48', '49','50', '51', '52', '53', '54', '55', '56', '57', '58', '59','60', '61', '62', '63', '64', '65', '66', '67', '68', '69','70', '71', '72', '73', '74', '75', '76', '77', '78', '79','80', '81', '82', '83', '84', '85', '86', '87', '88', '89','90', '91', '92', '93', '94', '95', '971', '972', '973', '974', '976']



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
    html.Div([
        dcc.Graph(
            figure=fig_graphic,
            style={
                'backgroundColor': '#4242b6',
                'border': '2px solid #92959B',
                'padding': '10px',
                'border-radius': '10px',
            }
        ),
    ], style={'width': '45%', 'display': 'inline-block', 'margin': '20px 0 20px 60px'}),  
    html.Div([
        dcc.Dropdown(id='departement', options=[{'label': dep, 'value': dep} for dep in departements], placeholder="Sélectionnez un département", style={'width': '300px', 'margin-right': '10px'}),
        dcc.Dropdown(id='checklist-carburant', options=[{'label': carb, 'value': carb} for carb in carburants], placeholder="Sélectionnez un carburant", value='gazole', style={'width': '300px', 'margin-right': '10px'}),
        html.Button('Soumettre', id='bouton-soumettre', style={'padding': '10px 20px'})
    ], style={'width': '45%', 'display': 'inline-block', 'margin': '20px 60px 20px 0'}),  
    # Div pour afficher les résultats
    html.Div(id='resultat-comparaison', style={'width': '45%', 'display': 'inline-block', 'margin': '20px 60px 60px 0'}), 
], style={'font-family': 'Roboto, sans-serif'})




     # Fonction de rappel pour traiter les données du formulaire
@app.callback(
    Output('resultat-comparaison', 'children'),
    [Input('bouton-soumettre', 'n_clicks')],
    [State('departement', 'value'),  
     State('checklist-carburant', 'value')]
)
def update_output(n_clicks, departement, carburant):
    if n_clicks is None:
        raise PreventUpdate
    else:
        resultat = prepare_data_comparison(departement, carburant, df)
        return html.Div(str(resultat))


# Lancer le serveur Flask
if __name__ == '__main__':
    app.run_server(debug=True)
