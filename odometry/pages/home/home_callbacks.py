import json, datetime
import plotly.express as px
import pandas as pd
import plotly.graph_objects as go

from utils.functions import *
from dash.dependencies import Input, Output, State
from app import app
from pages.home.home_data import TrainMinDataFrame, listOfTrains, listTime, FineSpeedDataFrame, updateTrainData

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
    temp = TrainMinDataFrame.query('TrainId==@train_val & TimeStamp==@time_val')
    # print("temp"+str(temp))
    trainMinIdx_val = temp['TrainMinIdx'].values[0]
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
    Output("rd_algo", "value"),
    Output("rd_speed", "value"),
    Output("expert_comment", "value")
    ],
    [Input('sbmt_lbl_btn', 'n_clicks_timestamp'),
     Input('prev_btn', 'n_clicks_timestamp'),
     Input('nxt_btn', 'n_clicks_timestamp'),
     Input('btn_prev_anm', 'n_clicks_timestamp'),
     Input('btn_nxt_anm', 'n_clicks_timestamp')],
     [State("rd_axle", "value"),
     State("rd_algo", "value"),
     State("rd_speed", "value"),
     State("expert_comment", "value"),
     State(component_id="slct_time", component_property="value"),
     State(component_id="divAnomalyIndex", component_property="children")]
)
def updated_clicked(sbmtBtn_clicks, prevAnm_clicks, nxtAnm_clicks, 
    prevBtn_clicks, nextBtn_clicks, lblAxl, lblOdo, lblSpd, exptCmt, time_val, vars):
    retTime = time_val
    data = json.loads(vars)
    anomalyIndex = data['anomalyIndex']
    indexVal = data['indexVal']
    retTrain=TrainMinDataFrame.at[anomalyIndex,'TrainId']
    btn_clicked = ''
    max_val = max(sbmtBtn_clicks, prevAnm_clicks, nxtAnm_clicks, prevBtn_clicks, nextBtn_clicks)
    if (max_val>0):
        if sbmtBtn_clicks==max_val:
            btn_clicked = 'sbmt'
            TrainMinDataFrame.at[indexVal,'LblAxleEvent']=lblAxl
            TrainMinDataFrame.at[indexVal,'LblOdoAlgo']=lblOdo
            TrainMinDataFrame.at[indexVal,'LblSpeed']=lblSpd
            TrainMinDataFrame.at[indexVal,'ExpertComment']=exptCmt
            currentDF = eval('TrainMinDataFrame.iloc[{}]'.format(indexVal))
            updateTrainData(currentDF)
        elif nxtAnm_clicks==max_val:
            anomalyIndex = anomalyIndex+1
            indexVal = anomalyIndex
            btn_clicked = 'sbmtNxt'
        elif prevAnm_clicks==max_val:
            anomalyIndex=anomalyIndex-1
            indexVal = anomalyIndex
            btn_clicked = 'skp'
        elif prevBtn_clicks==max_val:
            trainMinIdx = TrainMinDataFrame.at[indexVal,'TrainMinIdx']
            trainMinIdx = trainMinIdx-1
            indexVal = TrainMinDataFrame.index[TrainMinDataFrame['TrainMinIdx']==trainMinIdx][0]
            # retTime = TrainMinDataFrame.at[indexVal,'TimeStamp']
            # retTrain = TrainMinDataFrame.at[indexVal,'TrainId']
            # dt = pd.to_datetime(time_val, format="%d-%m-%Y:%H:%M")
            # dt = dt - datetime.timedelta(minutes=1)
            # retTime = dt.strftime("%d-%m-%Y:%H:%M")
            btn_clicked = 'prev'
        elif nextBtn_clicks==max_val:
            trainMinIdx = TrainMinDataFrame.at[indexVal,'TrainMinIdx']
            trainMinIdx = trainMinIdx+1
            indexVal = TrainMinDataFrame.index[TrainMinDataFrame['TrainMinIdx']==trainMinIdx][0]
            # retTime = TrainMinDataFrame.at[indexVal,'TimeStamp']
            # retTrain = TrainMinDataFrame.at[indexVal,'TrainId']
            # dt = pd.to_datetime(time_val, format="%d-%m-%Y:%H:%M")
            # dt = dt + datetime.timedelta(minutes=1)
            # retTime = dt.strftime("%d-%m-%Y:%H:%M")
            btn_clicked = 'nxt'
        else:
            btn_clicked = 'None'
    retTime = TrainMinDataFrame.at[indexVal,'TimeStamp']
    retTrain = TrainMinDataFrame.at[indexVal,'TrainId']
    retAxleEvent = TrainMinDataFrame.at[indexVal,'LblAxleEvent']
    retOdoAlgo = TrainMinDataFrame.at[indexVal,'LblOdoAlgo']
    retSpeed = TrainMinDataFrame.at[indexVal,'LblSpeed']
    retExpertComment = TrainMinDataFrame.at[indexVal,'ExpertComment']
    data['anomalyIndex']=int(anomalyIndex)
    data['indexVal']=int(indexVal)
    # print(data)
    jsret = json.dumps(data)
    # print(retTime, retTrain, jsret,retAxleEvent, retOdoAlgo, retSpeed, retExpertComment)
    return retTime,retTrain,jsret, retAxleEvent, retOdoAlgo, retSpeed, retExpertComment
