import pandas as pd

def prepare_data_comparison(departement, carburant, df):
    """
    Prépare les données pour une comparaison spécifique basée sur le département et le type de carburant.

    Args:
        departement (str): Le code du département pour lequel effectuer la comparaison.
        carburant (str): Le type de carburant (par exemple, 'gazole', 'e10').
        df (pandas.DataFrame): Le DataFrame source contenant les données des stations-service.

    Returns:
        pandas.DataFrame: Un DataFrame filtré contenant les informations de comparaison.
    """
    
    # Filtrer les données pour le département sélectionné
    df = df[df['code_departement'] == departement]

    # Filtrer les données pour le carburant sélectionné
    prix_col = f'{carburant}_prix'
    date_col = f'{carburant}_maj'

    # Convertir les colonnes en nombres et dates
    df[prix_col] = pd.to_numeric(df[prix_col], errors='coerce')
    df[date_col] = pd.to_datetime(df[date_col], errors='coerce', utc=True).dt.tz_convert(None)

    # Filtrer pour ne garder que les données récentes
    seuil_limit = pd.Timestamp.now() - pd.Timedelta(days=2)
    df = df[df[date_col] >= seuil_limit]
   
    # Grouper par adresse, cp, ville et obtenir les prix minimaux pour chaque carburant
    resultat = df.groupby(['adresse', 'cp', 'ville'])[prix_col].min().reset_index()

    # Trier par prix de carburant et obtenir les 5 premières lignes
    resultat = resultat.sort_values(by=prix_col).head(5)

    # Mettre en forme le résultat prix €/L et arrondi à 2 chiffres après la virgule 
    resultat[prix_col] = resultat[prix_col].round(2).astype(str) + ' €/L'

    # Retourner le résultat
    return resultat





