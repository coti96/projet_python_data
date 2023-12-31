import pandas as pd
import plotly.express as px


def prepare_data():
    # Lire les données CSV depuis l'URL
    url = "https://data.economie.gouv.fr/explore/dataset/prix-des-carburants-en-france-flux-instantane-v2/download?format=csv&timezone=Europe/Berlin&use_labels_for_header=false"
    df = pd.read_csv(url, sep=';')

    return df

   

