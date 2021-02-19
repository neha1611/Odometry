from datetime import datetime as dt

import plotly.express as px 
import dash_table 
import plotly.graph_objects as go
import dash_html_components as html
import dash_core_components as dcc
import dash_bootstrap_components as dbc

from utils.functions import *
from pages.home.home_data import TrainMinDataFrame, listOfTrains, listTime

from pages.home.home_callbacks import update_graph

layout = html.Div(
    [
    html.Div(id='intermediate-value', style={'display': 'none'} ,
        children="{\"train_id_val\":"+str(listOfTrains[0])+", \"time_val\":\""+str(listTime[0])+"\"}"
        ),
    dbc.Row(
        dbc.Col(
            dbc.Card([
                dbc.CardHeader(html.H4('RSSI Curves')),
                dbc.CardBody([
                    dbc.Row([
                        dbc.Col(
                            [
                            dbc.Label(html.P("Train Id")),
                            html.Div(
                                dcc.Dropdown(id="slct_train",
                                    options=[
                                    {'label': i, 'value': i}
                                    for i in listOfTrains
                                    ],
                                    multi=False,
                                    # placeholder='Filter by Train ID...',
                                    value=eval('TrainMinDataFrame.iloc[{}]'.format(0))['TrainId']
                                    )
                                )
                            ]),
                        dbc.Col(
                            [
                            dbc.Label(html.P("TimeStamp")),
                            html.Div(
                                dcc.Dropdown(id="slct_time",
                                    options=[
                                    {'label': i, 'value': i}
                                    for i in listTime
                                    ],
                                    multi=False,
                                    # placeholder='Filter by Time...',
                                    value=eval('TrainMinDataFrame.iloc[{}]'.format(0))['TimeStamp']
                                    )
                                )
                            ])
                         ]
                         ),
                        dbc.Row([
                            dbc.Col(dbc.Button("<",id="btn_prev_anm", 
                                color="primary", n_clicks_timestamp=0), width=1,
                                align="center", className="h-50"),
                            dbc.Col(
                                html.Div(
                                    dcc.Graph(id='my_map', figure={})
                                    ) ,width=10
                                ),
                            dbc.Col(dbc.Button(">",id="btn_nxt_anm", 
                                color="primary", n_clicks_timestamp=0), width=1,
                                align="center", className="h-50")
                            ]
                            ),
                        dbc.Row([
                            dbc.Col([
                                dbc.Row(
                                    dbc.Col(
                                        html.Div(
                                            dbc.Row([
                                                dbc.Col(
                                                        dbc.Label(html.P("Axle Event"))),
                                                dbc.Col(
                                                        dbc.RadioItems( id="rd_axle",
                                                            options=[
                                                            {'label': 'Likely', 'value': 'Likely'},
                                                            {'label': 'Unlikely', 'value': 'Unlikely'},
                                                            {'label': 'Maybe', 'value': 'Maybe'}
                                                            ],
                                                            value=eval('TrainMinDataFrame.iloc[{}]'.format(0))['LblAxleEvent']
                                                            , inline=True
                                                        )
                                                    )
                                                ])
                                            )
                                        )
                                    ),
                                dbc.Row(
                                    dbc.Col(
                                        html.Div(
                                            dbc.Row([
                                                dbc.Col(
                                                        dbc.Label(html.P("Odometry Algo Issues"))),
                                                dbc.Col(
                                                    dbc.RadioItems( id="rd_algo",
                                                        options=[
                                                        {'label': 'Likely', 'value': 'Likely'},
                                                        {'label': 'UnLikely', 'value': 'UnLikely'},
                                                        {'label': 'Maybe', 'value': 'Maybe'}
                                                        ],
                                                        value=eval('TrainMinDataFrame.iloc[{}]'.format(0))['LblOdoAlgo']
                                                        , inline=True
                                                        )
                                                    )
                                                ])
                                            )
                                        )
                                    ),
                                dbc.Row(
                                    dbc.Col(
                                        html.Div(
                                            dbc.Row([
                                                dbc.Col(
                                                        dbc.Label(html.P("Speed"))),
                                                dbc.Col(
                                                        dbc.RadioItems( id="rd_speed",
                                                            options=[
                                                            {'label': 'Possible Under Estimation', 'value': 'PossUnder'},
                                                            {'label': 'Possible Over Estimation', 'value': 'PossOver'},
                                                            {'label': 'OK', 'value': 'OK'}
                                                            ],
                                                            value=eval('TrainMinDataFrame.iloc[{}]'.format(0))['LblSpeed']
                                                            , inline=True
                                                            )
                                                    )
                                                ])
                                            )
                                        )
                                    ),
                                dbc.Row(
                                    dbc.Col(
                                        html.Div(
                                            [
                                            dbc.Label(html.P("Expert Comment")),
                                            dbc.Input(id="expert_comment", placeholder="Expert Comments", 
                                                type="text", value=eval('TrainMinDataFrame.iloc[{}]'.format(0))['ExpertComment'])
                                            ])
                                        )
                                    ),
                                dbc.Row(
                                    dbc.Col(
                                        html.Div(
                                            [
                                            html.Br(),
                                            dbc.ButtonGroup(
                                                [dbc.Button("Previous",id="prev_btn", color="primary", n_clicks_timestamp=0), 
                                                dbc.Button("Submit Labels",id="sbmt_lbl_btn", color="primary", n_clicks_timestamp=0), 
                                                dbc.Button("Next",id="nxt_btn", color="primary", n_clicks_timestamp=0)]
                                            ),
                                            html.Div(id='clicked-button', 
                                                    children='sbmtLbl:0 sbmtLbLNxt:0 skp:0 prev:0 nxt:0 last:nan', 
                                                    style={'display': 'none'}),
                                            html.Div(id="divAnomalyIndex", style={'display':'none'},
                                                children="{\"anomalyIndex\":0,\"indexVal\":0}")
                                            ])
                                        )
                                    ),
                                dbc.Row([
                                    dbc.Col(
                                        html.Div(
                                            dash_table.DataTable(id='table',
                                                columns=[{'name': i, 'id': i} for i in TrainMinDataFrame.loc[:,['TrainId','TimeStamp','AnomalyScore','LblAxleEvent','LblOdoAlgo','LblSpeed']]],
                                                # columns=[{"name": i, "id": i} 
                                                #     for i in [TrainMinDataFrame.columns
                                                data=TrainMinDataFrame.to_dict('records'),
                                                page_action='none',
                                                fixed_rows={'headers': True},
                                                style_table={'height': '300px', 'overflowY': 'auto'}
                                                )
                                            )
                                        ),
                                    dbc.Col(
                                        # html.Div(
                                        #     [
                                        #     html.Br(),
                                        #     dbc.ButtonGroup(
                                        #         [, 
                                        #         dbc.Button("Next Anomaly",id="btn_nxt_anm", color="primary", n_clicks_timestamp=0)]
                                        #         )
                                        #     ])
                                        )
                                    ])
                                ])
                        ])
                    ])
             ] )
        )
        )
        
    ])
        