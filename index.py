from dash.exceptions import PreventUpdate
from dash import dcc, html,  Input, Output, State
from app import create_app
from components.comparison import prepare_data_comparison
from components.graphic_line import create_graphic_line
from data import prepare_data , carburants, departements_dict
from components.histogram import  create_histogram
from components.map import plot_gas_stations


# Créer l'instance de l'application Dash
app = create_app()


# Recuperer les données en DataFrame grace à la fonction prepare_data() du fichier data.py
df = prepare_data()

# Créer  l'histogramme
fig_histogram = create_histogram(df)

# Creer le graphique
fig_graphic = create_graphic_line(df)

# Créer la carte
fig_map = plot_gas_stations(df)


# Définir l'agencement de l'application
app.layout = html.Div(className='app', children=[
    html.H1("Dashboard Carburants en France"),  
    html.Div(className='container', children=[
        html.Div([
            # Affiche l'histogramme 
            dcc.Graph(
                figure=fig_histogram,
                className='graph'
            ),
        ], className='card'),  

        html.Div([
            # Affiche la carte
            dcc.Graph(
                figure=fig_map,
                className='graph'
            ),
        ], className='card'),  
    ]),
    html.Div(className='container', children=[
        html.Div([
            # Affiche le graphique à courbes
            dcc.Graph(
                figure=fig_graphic,
                className='graph'
            ),
        ], className='card'),  

        html.Div(children=[
            # Titre
            html.H2("Trouver les prix les plus bas dans ma région :"),
            # Div pour le formulaire
            html.Div([
                # Menu déroulant pour le département
                dcc.Dropdown(id='departement', 
                            options = [{'label': str(name), 'value': str(code)} for code, name in departements_dict.items()], 
                            placeholder="Sélectionnez un département"),

                            
                # Menu déroulant pour le carburant
                dcc.Dropdown(id='checklist-carburant', options=[{'label': carb, 'value': carb} for carb in carburants], 
                            placeholder="Sélectionnez un carburant", value='gazole'),

                # Bouton pour soumettre le formulaire
                html.Button('Soumettre', id='bouton-soumettre')
            ]),  

            # Div pour afficher les résultats
            html.Div(id='resultat-comparaison'),
        ], className='card', id='card4'),
    ]),
])



    # Traiment des données du formulaire
@app.callback(
    # Spécifie le composant, propriétés mis à jour par le callback( div vide resultat-comparaison)
    Output('resultat-comparaison', 'children'),
    # Spécifie le composants et les propriétés qui déclenchent le callback lorsqu'ils changent
    # (bouton-soumettre, departement, checklist-carburant)
    [Input('bouton-soumettre', 'n_clicks')],
    [State('departement', 'value'),  
     State('checklist-carburant', 'value')]
)


def update_output(n_clicks, departement, carburant):
    """
    Traite les entrées du formulaire utilisateur et met à jour le contenu du tableau de bord.

    Cette fonction est appelée en réponse à un événement de clic sur le bouton du formulaire.
    Elle utilise les valeurs sélectionnées par l'utilisateur pour le département et le type de carburant,
    appelle une fonction pour préparer les données de comparaison correspondantes et retourne
    un élément HTML affichant les résultats.

    Args:
        n_clicks (int): Le nombre de fois que le bouton a été cliqué.
        departement (str): Le code du département sélectionné par l'utilisateur.
        carburant (str): Le type de carburant sélectionné par l'utilisateur.

    Returns:
        dash_html_components.Div: Un composant HTML Div contenant les résultats de la comparaison.
    
    Raises:
        PreventUpdate: Cette exception est levée pour empêcher la mise à jour du callback
                       si le bouton n'a pas été cliqué.
    """


    # Si le bouton n'a pas été cliqué, ne rien faire
    if n_clicks is None:
        raise PreventUpdate
    # Si le bouton a été cliqué, afficher le résultat
    else:
        resultat = prepare_data_comparison(departement, carburant, df)
        mise_en_forme = [f"{prix} : {adresse} {cp} {ville}" for adresse, cp, ville, prix in resultat.itertuples(index=False)]
        mise_en_forme = html.Div([html.P(ligne) for ligne in mise_en_forme])

    return mise_en_forme


# Lancer le serveur Flask
if __name__ == '__main__':
    app.run_server(debug=True)
