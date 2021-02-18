import dash
import sqlalchemy
import dash_bootstrap_components as dbc
import cdata
from settings.config import *
# import cdata

app = dash.Dash(__name__,
    suppress_callback_exceptions=True,
    external_stylesheets=[dbc.themes.BOOTSTRAP],meta_tags=[
        {"name": "viewport", "content": "width=device-width, initial-scale=1"}
    ])
app.title = name

dburl = 'postgresql://'+PGUSER+':'+PGPASSWORD+'@'+PGHOST+'/'+PGDATABASE
engine = sqlalchemy.create_engine(dburl)#'postgresql://scott:tiger@localhost/mydatabase')
# dbConn = psycopg2.connect(user="postgres",
# 					password="admin",
# 					database="postgres",
# 					host="127.0.0.1")

server = app.server