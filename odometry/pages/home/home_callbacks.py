import json, datetime
import plotly.express as px
import pandas as pd
import plotly.graph_objects as go

from utils.functions import *
from dash.dependencies import Input, Output, State
from app import app
from pages.home.home_data import TrainMinDataFrame, listOfTrains, listTime, FineSpeedDataFrame

@app.callback(
    [Output(component_id='slct_time', component_property='options'),
    Output(component_id='intermediate-value', component_property='children')],
    Input(component_id='slct_train', component_property='value'),
    Input(component_id='intermediate-value', component_property='children')
)
def update_dp(train_val, hiden):
    temp = TrainMinDataFrame.query('TrainId == @train_val')
    temp = temp.reset_index()
    listTime = temp['TimeStamp']
    data = json.loads(hiden)
    data['train_id_val']=train_val
    data['time_val']=listTime[0]
    jsret = json.dumps(data)
    optn = [{'label': i, 'value': i} for i in listTime]
    return optn, jsret


@app.callback(
    Output(component_id='my_map', component_property='figure'),
    [Input(component_id='slct_train', component_property='value'),
    Input(component_id='slct_time', component_property='value')]
)
def update_graph(train_val, time_val):
    print(eval('TrainMinDataFrame.iloc[{}]'.format(0))['LblAxleEvent'])
    temp = TrainMinDataFrame.query('TrainId==@train_val & TimeStamp==@time_val')
    print(train_val, time_val)
    print(temp)
    trainMinIdx_val = temp['TrainMinIdx'].values[0]
    print(trainMinIdx_val)
    t = FineSpeedDataFrame.query('TrainMinIdx==@trainMinIdx_val')
    t = t.reset_index()
    
    trace0=go.Scatter(
         x=t.Seconds,
         y=t.LeftAxleSpeed,
         mode='lines',
         name='LeftAxleSpeed'
         )
    trace1=go.Scatter(
         x=t.Seconds,
         y=t.RightAxleSpeed,
         mode='lines',
         name='RightAxleSpeed'
         )
    trace2=go.Scatter(
         x=t.Seconds,
         y=t.OdoSpeed,
         mode='lines',
         name='OdoSpeed'
         )
    data = [trace0, trace1, trace2]

    layout = go.Layout()#title = 'Left and Right Axle Graph')
    figure= go.Figure(data=data, layout=layout)    
    return figure

@app.callback(
    [
    Output("slct_time", "value"),
    Output("slct_train", "value"),
    Output("divAnomalyIndex", "children"),
    Output("rd_axle", "value"),
    Output(component_id="rd_algo", component_property="value"),
    Output(component_id="rd_speed", component_property="value")
    ],
    [Input('sbmt_lbl_btn', 'n_clicks_timestamp'),
     Input('prev_btn', 'n_clicks_timestamp'),
     Input('nxt_btn', 'n_clicks_timestamp'),
     Input('btn_prev_anm', 'n_clicks_timestamp'),
     Input('btn_nxt_anm', 'n_clicks_timestamp')],
     [State(component_id="slct_time", component_property="value"),
     State(component_id="divAnomalyIndex", component_property="children")]
)
def updated_clicked(sbmtBtn_clicks, prevAnm_clicks, nxtAnm_clicks, 
    prevBtn_clicks, nextBtn_clicks, time_val, vars):
    # print("axle val "+str(axle_val))
    retTime = time_val
    print("anomaly index "+str(vars))
    data = json.loads(vars)
    temp = data['anomalyIndex']
    print(temp)
    retTrain=eval('TrainMinDataFrame.iloc[{}]'.format(temp))['TrainId']
    print(retTrain)
    btn_clicked = ''
    max_val = max(sbmtBtn_clicks, prevAnm_clicks, nxtAnm_clicks, prevBtn_clicks, nextBtn_clicks)
    if sbmtBtn_clicks==max_val:
        btn_clicked = 'sbmt'
    elif nxtAnm_clicks==max_val:
        temp = temp+1
        retTime =eval('TrainMinDataFrame.iloc[{}]'.format(temp))['TimeStamp']
        retTrain =eval('TrainMinDataFrame.iloc[{}]'.format(temp))['TrainId']
        btn_clicked = 'sbmtNxt'
    elif prevAnm_clicks==max_val:
        print(temp)
        temp=temp-1
        print(temp)
        btn_clicked = 'skp'
        retTime =eval('TrainMinDataFrame.iloc[{}]'.format(temp))['TimeStamp']
        retTrain = eval('TrainMinDataFrame.iloc[{}]'.format(temp))['TrainId']
    elif prevBtn_clicks==max_val:
        dt = pd.to_datetime(time_val, format="%d-%m-%Y:%H:%M")
        dt = dt - datetime.timedelta(minutes=1)
        retTime = dt.strftime("%d-%m-%Y:%H:%M")
        btn_clicked = 'prev'
    elif nextBtn_clicks==max_val:
        dt = pd.to_datetime(time_val, format="%d-%m-%Y:%H:%M")
        dt = dt + datetime.timedelta(minutes=1)
        retTime = dt.strftime("%d-%m-%Y:%H:%M")
        print("abc")
        btn_clicked = 'nxt'
    else:
        btn_clicked = 'None'
        print("assdf")
    retAxleEvent = eval('TrainMinDataFrame.iloc[{}]'.format(temp))['LblAxleEvent']
    retOdoAlgo = eval('TrainMinDataFrame.iloc[{}]'.format(temp))['LblOdoAlgo']
    retSpeed = eval('TrainMinDataFrame.iloc[{}]'.format(temp))['LblSpeed']
    print("ewwer")
    data['anomalyIndex']=temp
    jsret = json.dumps(data)
    print(retTime, retTrain, jsret,retAxleEvent, retOdoAlgo, retSpeed)
    return retTime,retTrain,jsret, retAxleEvent, retOdoAlgo, retSpeed
