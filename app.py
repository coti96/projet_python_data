from dash import Dash


def create_app():
    """
    Crée et configure une instance de l'application Dash.

    Cette fonction initialise l'application Dash avec des paramètres par défaut
    et configure le titre, les feuilles de style et les scripts.

    Returns:
        dash.Dash: Une instance configurée de l'application Dash.
    """
    
    app = Dash(__name__)
    app.title = "Prix du carburant en France"
    app.css.config.serve_locally = True
    app.scripts.config.serve_locally = True

    return app
