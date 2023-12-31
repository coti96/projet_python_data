from dash import Dash
from components.histogram import create_histogram

def create_app():
    # Créer une instance de l'application Dash
    app = Dash(__name__)

    # Configurer les paramètres de l'application
    app.title = "Prix du carburant en France"
    app.css.config.serve_locally = True
    app.scripts.config.serve_locally = True


    # Retourner l'instance de l'application Dash
    return app
