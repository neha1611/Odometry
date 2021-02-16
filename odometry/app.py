import dash
import dash_bootstrap_components as dbc
from settings import config


app = dash.Dash(__name__,
    suppress_callback_exceptions=True,
    external_stylesheets=[dbc.themes.BOOTSTRAP],meta_tags=[
        {"name": "viewport", "content": "width=device-width, initial-scale=1"}
    ])
app.title = config.name

