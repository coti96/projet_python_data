import requests
import pandas as pd
import dash
import plotly

#URL de l'API
url = "https://data.economie.gouv.fr/api/explore/v2.1/catalog/datasets/prix-des-carburants-en-france-flux-instantane-v2/records?limit=20"

#Faire une requête GET à l'API
response = requests.get(url) 

#Vérifier que la requête a reussi
if response.status_code == 200:
    # Convertir la réponse en JSON
    data = response.json()
    #Convertir les données en DataFrame pandas
    df = pd.DataFrame(data['results'])
    #Afficher les premières lignes du DataFrame
    print(df.head())
else :
    print("Erreur lors de la recuperation des données")

