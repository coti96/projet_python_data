import pandas as pd

def prepare_data_comparison(departement, carburant, df):
    
    print (departement)
    print (carburant)
    # Filtrer les données pour le département sélectionné
    df = df[df['code_departement'] == departement]

    # Filtrer les données pour le carburant sélectionné
    prix_col = f'{carburant}_prix'
    date_col = f'{carburant}_maj'

    df[prix_col] = pd.to_numeric(df[prix_col], errors='coerce')
    df[date_col] = pd.to_datetime(df[date_col], errors='coerce', utc=True).dt.tz_convert(None)

    print('avant filtre')
    print (df)

    # Filtrer pour ne garder que les données récentes
    recent_threshold = pd.Timestamp.now() - pd.Timedelta(days=2)
    df = df[df[date_col] >= recent_threshold]
    print('apres filtre')
    print (df)

    # Grouper par adresse, cp, ville et obtenir les prix minimaux pour chaque carburant
    resultat = df.groupby(['adresse', 'cp', 'ville'])[prix_col].min().reset_index()

    # Trier par prix de carburant et obtenir les 5 premières lignes
    resultat = resultat.sort_values(by=prix_col).head(5)

    print(resultat)

    return resultat
