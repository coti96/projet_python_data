import pandas as pd

def prepare_data_histogram():
    # Lire les données CSV depuis l'URL
    url = "https://data.economie.gouv.fr/explore/dataset/prix-des-carburants-en-france-flux-instantane-v2/download?format=csv&timezone=Europe/Berlin&use_labels_for_header=false"
    df = pd.read_csv(url, sep=';')

    # Convertir les colonnes de date en format datetime
    date_columns = ['gazole_maj', 'sp95_maj', 'e85_maj', 'gplc_maj', 'e10_maj', 'sp98_maj']
    for col in date_columns:
        df[col] = pd.to_datetime(df[col], utc=True)

    # Supprimer les lignes où toutes les colonnes de date sont NaN ou NaT
    df = df.dropna(subset=date_columns, how='all')

    # Filtrer les données pour les trois dernières années
    three_years_ago = (pd.Timestamp.now(tz='UTC') - pd.DateOffset(years=3)).normalize()
    df = df[df['gazole_maj'] >= three_years_ago]

    # Extraire le mois et l'année de la colonne 'gazole_maj'
    df['year'] = df['gazole_maj'].dt.year
    df['month'] = df['gazole_maj'].dt.month

    # Grouper par année, mois et code_region, puis calculer le prix moyen
    df_grouped = df.groupby(['year', 'month'])[date_columns + ['gazole_prix', 'sp95_prix', 'e85_prix', 'gplc_prix', 'e10_prix', 'sp98_prix']].mean().reset_index()

    # Créer une nouvelle colonne pour l'axe des abscisses qui combine l'année et le mois
    df_grouped['year_month'] = df_grouped['year'].astype(str) + '-' + df_grouped['month'].astype(str).str.zfill(2)

    # Retourner le DataFrame groupé
    return df_grouped
