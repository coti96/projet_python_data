import pandas as pd
import plotly.express as px

def prepare_data():
    """
    Prépare les données pour l'application en les téléchargeant et en les convertissant en DataFrame.

    Télécharge les données sur les prix des carburants depuis une source en ligne et les
    convertit en un DataFrame Pandas pour une utilisation ultérieure dans l'application.

    Returns:
        pandas.DataFrame: DataFrame contenant les données sur les prix des carburants.
    """
    
    # Télécharger les données depuis une source en ligne
    url = "https://data.economie.gouv.fr/explore/dataset/prix-des-carburants-en-france-flux-instantane-v2/download?format=csv&timezone=Europe/Berlin&use_labels_for_header=false"
    df = pd.read_csv(url, sep=';')

    return df


# Variables globales pour le menu déroulant 
carburants = ['gazole', 'sp95', 'sp98', 'e10', 'e85']
df = prepare_data()
#  Creation d'un DataFrame contenant les colonnes uniques 'departement' et 'code_departement'
unique_departements = df[['departement', 'code_departement']].drop_duplicates()
# Convertion en dictionnaire où 'code_departement' est la clé et 'departement' la valeur
departements_dict = dict(zip(unique_departements['code_departement'], unique_departements['departement']))



   

