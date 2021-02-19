from app import app
import dash_bootstrap_components as dbc
import dash_html_components as html

from utils.constants import home_page_location
sidebar_header = dbc.Row([
                    dbc.Col(
                        html.H2("Odometry")
                        ),
                    dbc.Col([
                        html.Button(
                            html.Span(
                                html.Img(src=app.get_asset_url("/assets/images/Odometry_Logo_1.png"), 
                                    style = {'height' : '40px' , 'width' : '40px'})
                                ),
                                className="navbar-toggler",
                                style={"color": "rgba(0,0,0,.5)"},
                                id="navbar-toggle",
                            ),
                            html.Button(
                                html.Span(
                                    html.Img(src=app.get_asset_url("images/Odometry_Logo_1.png"), 
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
                        dbc.NavLink("Overview", href=home_page_location, id="page-1-link"),
                        dbc.NavLink("TRE", href=".", id="page-2-link"),
                        dbc.NavLink("Simulations", href=".", id="page-3-link"),
                        dbc.NavLink("Statistics", href=".", id="page-4-link"),
                        dbc.NavLink("Machine Learning", href=".", id="page-5-link"),
                        dbc.NavLink("Geographical view", href=".", id="page-6-link")
                    ],
                    vertical=True, pills=True,
                    ),
                ],
                id="collapse"
                )
            ],
            id="sidebar",
            )
