from datetime import datetime as dt
import dash_datetimepicker as dd
import datetime
import plotly.express as px 
import dash_table 
import plotly.graph_objects as go
import dash_html_components as html
import dash_core_components as dcc
import dash_bootstrap_components as dbc

from utils.functions import *
from pages.home.home_data import  currentTrainMinDF, TrainListDF,TrainMinDataFrame

from pages.home.home_callbacks import update_output

def onBodyLoad():
    return "{\"boday_loaded\":\"true\"}"

layout = html.Div(
    [
    html.Div( id="hid_body_loaded", style={'display': 'none'} , children=onBodyLoad()),
    html.Div(id="hid_timeoffset", style={'display':'none'}),
    html.Div(id='hid_train', style={'display': 'none'} ,
        children="{\"train_id_val\":\""+str(TrainListDF.at[0,'TrainId'])+"\"}"
        ),
    html.Div(id='hid_time', style={'display': 'none'} ,
        children="{\"time_val\":\""+str(currentTrainMinDF.at[0,'TimeStamp'])+"\"}"#, \"time_val\":\""+str(currentTrainMinDF.at[0, 'TimeStamp'])+"\"}"
        ),
    dbc.Row(
        dbc.Col(
            dbc.Card([
                dbc.CardHeader(html.H4('Edit Labels')),
                dbc.CardBody([
                    dbc.Row([
                        dbc.Col(
                            [
                            dbc.Label(html.P("Train Id")),
                            html.Div(
                                dcc.Dropdown(id="slct_train",
                                    options=[
                                    {'label': i, 'value': i}
                                    for i in TrainListDF['TrainId'].tolist()
                                    ],
                                    multi=False,
                                    # placeholder='Filter by Train ID...',
                                     value=eval('currentTrainMinDF.iloc[{}]'.format(0))['TrainId']
                                    )
                                )
                            ]),
                        dbc.Col(
                            [
                            dbc.Label(html.P("PickDate Range")),
                            html.Div([
                                dd.DashDatetimepicker(
                                    id='dateRange',
                                    startDate=(eval('TrainListDF.iloc[{}]'.format(0))['MinDate']),
                                    endDate=((eval('TrainListDF.iloc[{}]'.format(0))['MaxDate'])),
                                    # initial_visible_month=date(2017, 8, 5),
                                    # end_date=date(2017, 8, 25)
                                ),
                                html.Div(id='hid_time_range', style={'display': 'none'}),
                            ])
                            # dbc.Label(html.P("TimeStamp")),
                            # html.Div(
                            #     dcc.Dropdown(id="slct_time",
                            #         options=[
                            #         {'label': i, 'value': i}
                            #         for i in listTime
                            #         ],
                            #         multi=False,
                            #         # placeholder='Filter by Time...',
                            #         value=eval('TrainMinDataFrame.iloc[{}]'.format(0))['TimeStamp']
                            #         )
                            #     )
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
                        ]),
                    dbc.Row([
                        dbc.Col([
                            dbc.Row(
                                dbc.Col(
                                    html.Div(
                                        dbc.Row([
                                            dbc.Col(
                                                    dbc.Label(html.P("Axle Event")), width=2),
                                            dbc.Col(
                                                    dbc.RadioItems( id="rd_axle",
                                                        options=[
                                                        {'label': 'Likely', 'value': 'Likely'},
                                                        {'label': 'Unlikely', 'value': 'UnLikely'},
                                                        {'label': 'Maybe', 'value': 'Maybe'}
                                                        ],
                                                        value=eval('currentTrainMinDF.iloc[{}]'.format(0))['LblAxleEvent']
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
                                                    dbc.Label(html.P("Odometry Algo")), width=2),
                                            dbc.Col(
                                                dbc.RadioItems( id="rd_algo",
                                                    options=[
                                                    {'label': 'Likely', 'value': 'Likely'},
                                                    {'label': 'UnLikely', 'value': 'UnLikely'},
                                                    {'label': 'Maybe', 'value': 'Maybe'}
                                                    ],
                                                    value=eval('currentTrainMinDF.iloc[{}]'.format(0))['LblOdoAlgo']
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
                                                    dbc.Label(html.P("Speed")), width=2),
                                            dbc.Col(
                                                    dbc.RadioItems( id="rd_speed",
                                                        options=[
                                                        {'label': 'Possible Under Estimation', 'value': 'PossUnder'},
                                                        {'label': 'Possible Over Estimation', 'value': 'PossOver'},
                                                        {'label': 'OK', 'value': 'OK'}
                                                        ],
                                                        value=eval('currentTrainMinDF.iloc[{}]'.format(0))['LblSpeed']
                                                        , inline=True
                                                        )
                                                )
                                            ])
                                        )
                                    )
                                ),
                            dbc.Row([
                                dbc.Col(dbc.Label(html.P("Expert Comment")), width=2
                                    ), 
                                dbc.Col(
                                    dbc.Input(id="expert_comment", placeholder="Expert Comments", 
                                            type="text", value=eval('currentTrainMinDF.iloc[{}]'.format(0))['ExpertComment'])
                                    )
                                ]),
                            dbc.Row(dbc.Col(html.Br())),
                            dbc.Row([
                                dbc.Col(
                                    html.Div(
                                        dash_table.DataTable(id='table',
                                            # columns=[{'name': i, 'id': i} for i in TrainMinDataFrame.loc[:,['TrainId','TimeStamp','AnomalyScore','LblAxleEvent','LblOdoAlgo','LblSpeed']]],
                                            # columns=[{"name": i, "id": i} 
                                            #     for i in [TrainMinDataFrame.columns
                                            columns= [{"name": "Vehicle Id", "id": "TrainId"},
                                                        {"name": "Timestamp", "id": "TimeStamp"},
                                                        {"name": "Anomaly Score", "id": "AnomalyScore"},
                                                        {"name": "Axle Event", "id": "LblAxleEvent"},
                                                        {"name": "Odometry Algo", "id": "LblOdoAlgo"},
                                                        {"name": "Speed", "id": "LblSpeed"},],
                                            style_cell_conditional=[
                                                       {
                                                        'if': {'column_id': c},
                                                        'textAlign': 'left'
                                                        } for c in ['LblAxleEvent', 'LblOdoAlgo', 'LblSpeed']],
                                            data=TrainMinDataFrame.to_dict('records'),
                                            page_action='none',
                                            fixed_rows={'headers': True},
                                            style_table={'height': '300px', 'overflowY': 'auto'}
                                            )
                                        )
                                    ),
                                dbc.Col([
                                    dbc.Row(
                                        dbc.Col(
                                            html.Div([
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
                                        dbc.Col([
                                            html.Br(),
                                            dbc.Label(html.P("Labeled Events for the current Vehicle")),
                                            html.Br(),
                                            html.Div(id="lblCount", style={'display':'none'},
                                                    children="{\"currTrnLblCount\":0, \"allLblCount\":0}"),
                                            html.H2(id="lbl1")
                                            ])
                                        ,
                                        dbc.Col([
                                                html.Br(),
                                                dbc.Label(html.P("Labeled Events for all the Vehicles")),
                                                html.Br(),
                                                html.H2(id="lbl2")
                                                ]
                                         )
                                    ])
                                ])
                            ])
                    ])
                ])
            ])
        ])
    )
        
)])
        