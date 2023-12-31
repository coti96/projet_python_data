import plotly.express as px

def create_histogram(df_grouped):
    # Créer l'histogramme
    fig = px.bar(
        df_grouped, 
        x='year_month', 
        y=['gazole_prix', 'sp95_prix', 'e85_prix', 'gplc_prix', 'e10_prix', 'sp98_prix'], 
        barmode='group', 
        labels={'value': 'Prix moyen (€/L)', 'variable': 'Type de Carburant', 'year_month': 'Mois et Année'},
        color_discrete_sequence=px.colors.qualitative.Vivid  # Palette de couleurs personnalisée
    )

    # Définir la plage de l'axe des ordonnées
    fig.update_yaxes(range=[1, 3], title='Prix moyen (€/L)')

    # Personnaliser l'histogramme
    fig.update_layout(
        title='Évolution du Prix des Carburants en France',
        title_font_size=24,
        xaxis=dict(
            title='Mois et Année',
            title_font_size=18,
            tickangle=-45  # Incliner les étiquettes de l'axe des x
        ),
        yaxis_title='Prix Moyen (€/L)',
        yaxis_title_font_size=18,
        legend_title='Carburants',
        legend_title_font_size=18,
        legend_font_size=16,
        margin=dict(l=50, r=50, t=100, b=50)
    )

    # Ajouter des étiquettes de données sur les barres
    fig.update_traces(texttemplate='%{y:.2f} €', textposition='outside')

    return fig

# Exemple d'utilisation :
# df_grouped = prepare_data_histogram()
# fig = create_histogram(df_grouped)
# fig.show()
