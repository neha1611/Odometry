from app import app
import dash_bootstrap_components as dbc
import dash_html_components as html

from utils.constants import home_page_location, home1_page_location
sidebar_header = dbc.Row([
                    dbc.Col(
                        html.H2("Odometry")
                        ),
                    dbc.Col([
                        html.Button(
                            html.Span(
                                html.Img(src=app.get_asset_url("/assets/images/Odometry_Carbonblue.png"), 
                                    style = {'height' : '40px' , 'width' : '40px'})
                                ),
                                className="navbar-toggler",
                                style={"color": "rgba(0,0,0,.5)"},
                                id="navbar-toggle",
                            ),
                            html.Button(
                                html.Span(
                                    html.Img(src=app.get_asset_url("images/Odometry_Carbonblue.png"), 
                                        style = {'height' : '40px' , 'width' : '40px'})
                                    ),
                                    className="navbar-toggler",
                                    style={"color": "rgba(0,0,0,.5)"},
                                    id="sidebar-toggle",
                                )
                            ],
                            width="auto",
                            align="center",
                            )
                        ])

sidebar = html.Div([
            sidebar_header,
            html.Div(
                html.Hr(),
                id="blurb"
                ),
            dbc.Collapse([
                    dbc.Nav([
                        dbc.NavLink("Event Labeling", href=home_page_location, id="page-1-link", active="exact"),
                        dbc.NavLink("Event Labeling Alternate", href=home1_page_location, id="page-1.1-link",active="exact"),
                        dbc.NavLink("Classification Performance", href=".", id="page-2-link",active="exact"),
                        dbc.NavLink("Classification Review", href=".", id="page-3-link",active="exact")
                    ],
                    vertical=True, pills=True,
                    ),
                ],
                id="collapse"
                )
            ],
            id="sidebar",
            )
