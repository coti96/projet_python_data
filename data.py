import pandas as pd
from dash import Dash, dcc, html, dash_table 
from dash.dependencies import Input, Output
from dash.dash_table.Format import Group

# 1. Créer une instance de l'application Dash
app = Dash(__name__)

# 2. Lire les données CSV depuis l'URL
url = "https://data.economie.gouv.fr/explore/dataset/prix-des-carburants-en-france-flux-instantane-v2/download?format=csv&timezone=Europe/Berlin&use_labels_for_header=false"
df = pd.read_csv(url, sep=';')  # je spécifie le séparateur



# 3. Sélectionner uniquement les colonnes souhaitées
df = df.loc[:, ['id', 'cp', 'adresse', 'ville', 'geom', 'gazole_maj', 'gazole_prix', 'sp95_maj', 'sp95_prix', 'departement', 'code_departement', 'region', 'code_region']]

# 4. Mise en forme des données sous forme de tableau


app.layout = html.Div([
    html.H1('Prix des Carburants en France'),
    dash_table.DataTable(
    id='table',  # Identifiant pour le composant DataTable

    # Création d' une liste de dictionnaires où chaque dictionnaire représente une colonne du tableau. 
    # Itère sur chaque colonne du DataFrame df pour créer cette liste.
    # La clé "name" = nom  de la colonne, et la clé "id" = l’identifiant utilisé pour référencer les données de la colonne. 
    columns=[{"name": i, "id": i} for i in df.columns],  #  
    
    # Conversion des données en une liste de dictionnaires et spécification de l'argument data.
    # Chaque dictionnaire représente une ligne du DataFrame, avec les clés correspondant aux noms des colonnes et les valeurs correspondant aux données de cette ligne.
    data=df.to_dict('records'),  
    page_size=30  # Nombre de lignes affichées par page dans le tableau
)
])

#5. Exécuter l'application
if __name__ == '__main__':
    app.run_server(debug=True)
