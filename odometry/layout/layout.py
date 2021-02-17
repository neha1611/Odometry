import dash 
import dash_html_components as html
import dash_core_components as dcc
import dash_bootstrap_components as dbc

from app import app
from layout.sidebar import sidebar
from dash.dependencies import Input, Output
from settings import config

logo_postion =  html.Div(
                    [
                        html.Img(src=app.get_asset_url("images/Odometry_Logo_2.png"), className = 'logo')
                    ]
                )

content = html.Div(id="page-content")

layout = html.Div([logo_postion,dcc.Location(id="url"), sidebar, content])
