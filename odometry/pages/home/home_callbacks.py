import json, datetime
import plotly.express as px
import pandas as pd
import plotly.graph_objects as go
import pages.home.home_data as hd
from utils.functions import *
from dash.dependencies import Input, Output, State
from app import app
from pages.home.home_data import currentTrainMinDF,  currentTrainFeatureDF, TrainListDF
from pages.home.home_functions import *

#When a Train is selected in dropdown, call this function to change working dataframe to that trains dataframe
@app.callback(
    [
    Output("dateRange", "max_date_allowed"),
    Output("dateRange", "min_date_allowed"),
    Output("dateRange", "start_date"),
    Output("dateRange", "end_date"),
    Output(component_id='hid_train', component_property='children'),
    Output(component_id='lbl1', component_property='children'),
    Output(component_id='lbl2', component_property='children')],
    Input(component_id='slct_train', component_property='value'),
    State(component_id='hid_train', component_property='children')
)
def update_dp(train_val, hid_train):
    #get all data for selected Train
    print(train_val) 
    trainDF  = TrainListDF.query("TrainId==@train_val")
    trainDF.reset_index()
    print(trainDF)
    retMinDate = (trainDF.iloc[0]['MinDate']).date()
    retMaxDate = (trainDF.iloc[0]['MaxDate']).date()+datetime.timedelta(weeks=6)
    data = json.loads(hid_train)
    #set the hidden variables
    data['train_id_val']=train_val
    #Count Train Level lables
    #TODO implement update all lables count
    # lbldAllEvents= TrainMinDataFrame.query('LblAxleEvent.notna() or LblSpeed.notna() or LblOdoAlgo.notna()')
    # lbldTrainEvents = currentTrainMinDF.query('LblAxleEvent.notna() or LblSpeed.notna() or LblOdoAlgo.notna()')
    allLblCount = 0 #len(lbldAllEvents.index)
    trnLblCount = 0#len(lbldTrainEvents.index)
    jsret = json.dumps(data)
    print(retMinDate, retMaxDate,retMinDate, retMaxDate, jsret, trnLblCount, allLblCount)
    return retMinDate, retMaxDate,retMinDate, retMaxDate, jsret, trnLblCount, allLblCount


@app.callback(
    Output(component_id='hid_time_range', component_property='children'),
    [Input(component_id='dateRange', component_property='start_date'),
    Input(component_id='dateRange', component_property='end_date'),
    Input(component_id='hid_train', component_property='children')]
)
def update_time_range(startDate, endDate, train_var):
    #get all data for selected Train
    data = json.loads(train_var)
    train_val = data['train_id_val']
    print(train_val, startDate, endDate) 
    hd.currentTrainMinDF  = getTrainDataInRange(train_val,startDate, endDate )
    print(hd.currentTrainMinDF.at[0, 'TrainMinIdx'])
    data['start_date'] = startDate
    data['end_date'] = endDate
    data['nClicksTimestamp'] = datetime.datetime.now().timestamp()*1000
    jsret = json.dumps(data)
    print(jsret)
    return jsret



@app.callback(
    [Output(component_id='my_map', component_property='figure'),
    Output(component_id="rd_axle",  component_property="value"),
    Output(component_id="rd_algo",  component_property="value"),
    Output(component_id="rd_speed",  component_property="value"),
    Output(component_id="expert_comment",  component_property="value")],
    #[#Input(component_id='hid_time_range', component_property='children'),
    #Input(component_id='hid_time', component_property='children'), 
    Input("divAnomalyIndex", "children"),#],
    State(component_id='hid_train', component_property='children')
)
def update_output( hid_anmly, hid_train):
    print(" hid_anmly, hid_train")
    print(  hid_anmly, hid_train)
    train_val = json.loads(hid_train)['train_id_val']
    indexVal = json.loads(hid_anmly)['indexVal']
    print(indexVal)
    trainMinIdx_val = hd.currentTrainMinDF.at[indexVal,'TrainMinIdx']
    print(trainMinIdx_val)
    t = getTrainFeatures(trainMinIdx_val)
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

    layout = go.Layout()
    figure= go.Figure(data=data, layout=layout)  
    figure.update_layout(margin={'l': 40, 'b': 40, 't': 10, 'r': 0}, 
        hovermode='closest', legend_orientation='h')
    # retTime = hd.currentTrainMinDF.at[indexVal,'TimeStamp']
    # retTrain = currentTrainMinDF.at[indexVal,'TrainId']
    retAxleEvent = hd.currentTrainMinDF.at[indexVal,'LblAxleEvent']
    retOdoAlgo = hd.currentTrainMinDF.at[indexVal,'LblOdoAlgo']
    retSpeed = hd.currentTrainMinDF.at[indexVal,'LblSpeed']
    retExpertComment = hd.currentTrainMinDF.at[indexVal,'ExpertComment']
    print("return")
    # print(retTime)
    print(retAxleEvent, retOdoAlgo, retSpeed, retExpertComment)
    return figure, retAxleEvent, retOdoAlgo, retSpeed, retExpertComment

@app.callback(
    [#Output(component_id='hid_time', component_property='children'),
     Output("divAnomalyIndex", "children"),
     Output('prev_btn', 'disabled'),
     Output('nxt_btn', 'disabled'),
     Output('btn_prev_anm', 'disabled'),
     Output('btn_nxt_anm', 'disabled')],
    [Input('sbmt_lbl_btn', 'n_clicks_timestamp'),
     Input('prev_btn', 'n_clicks_timestamp'),
     Input('nxt_btn', 'n_clicks_timestamp'),
     Input('btn_prev_anm', 'n_clicks_timestamp'),
     Input('btn_nxt_anm', 'n_clicks_timestamp'), 
     Input(component_id='hid_time_range', component_property='children')],
    [#State(component_id='hid_time', component_property='children'),
     State(component_id="divAnomalyIndex", component_property="children"), 
     State("rd_axle", "value"),
     State("rd_algo","value"),
     State("rd_speed", "value"), 
     State("expert_comment", "value")]
)
def updated_clicked(sbmtBtn_clicks, prevAnm_clicks, nxtAnm_clicks, 
    prevBtn_clicks, nextBtn_clicks, hid_time_range, vars, lblAxl, lblOdo, lblSpd, exptCmt):
    prev_dsbl=False
    nxt_dsbl=False
    prev_anm_dsbl=False
    next_anm_dsbl=False
    print(lblAxl, lblOdo, lblSpd, exptCmt)
    timeRangeData = json.loads(hid_time_range)
    range_nclicksTimeStamp = timeRangeData['nClicksTimestamp']
    print(range_nclicksTimeStamp,prevAnm_clicks )
    # timeData = json.loads(time_var)
    # retTime = timeData['time_val']
    data = json.loads(vars)
    anomalyIndex = data['anomalyIndex']
    indexVal = data['indexVal']
    btn_clicked = ''
    max_val = max(range_nclicksTimeStamp, sbmtBtn_clicks, prevAnm_clicks, nxtAnm_clicks, prevBtn_clicks, nextBtn_clicks)
    if (max_val>0):
        if(range_nclicksTimeStamp==max_val):
            print("date Range was changed")
            indexVal=0
            anomalyIndex=0
            prev_dsbl=True
            prev_anm_dsbl=True
            print(hd.currentTrainMinDF.at[0, 'TrainMinIdx'])
        elif sbmtBtn_clicks==max_val:
            print("btn_clicked = 'sbmt'")
            hd.currentTrainMinDF.at[indexVal,'LblAxleEvent']=lblAxl
            hd.currentTrainMinDF.at[indexVal,'LblOdoAlgo']=lblOdo
            hd.currentTrainMinDF.at[indexVal,'LblSpeed']=lblSpd
            hd.currentTrainMinDF.at[indexVal,'ExpertComment']=exptCmt
            currentDF = eval('hd.currentTrainMinDF.iloc[{}]'.format(indexVal))
            updateTrainData(currentDF)
        elif nxtAnm_clicks==max_val:
            print('next button clicked')
            anomalyIndex = anomalyIndex+1
            indexVal = anomalyIndex
            btn_clicked = 'sbmtNxt'
        elif prevAnm_clicks==max_val:
            print('previous anomaly button clicked')
            anomalyIndex=anomalyIndex-1
            indexVal = anomalyIndex
            if anomalyIndex==0:
                 prev_anm_dsbl=True
            btn_clicked = 'skp'
        elif prevBtn_clicks==max_val:
            print('previous button clicked')
            trainMinIdx = hd.currentTrainMinDF.at[indexVal,'TrainMinIdx']
            print(trainMinIdx, indexVal)
            trainMinIdx = trainMinIdx-1
            indexVal = hd.currentTrainMinDF[hd.currentTrainMinDF['TrainMinIdx']==trainMinIdx].index[0]
            print(trainMinIdx, indexVal)
            if indexVal==0:
                prev_dsbl=False
            btn_clicked = 'prev'
        elif nextBtn_clicks==max_val:
            print('next button clicked')
            trainMinIdx = hd.currentTrainMinDF.at[indexVal,'TrainMinIdx']
            print(trainMinIdx, indexVal)
            trainMinIdx = trainMinIdx+1
            indexVal = hd.currentTrainMinDF[hd.currentTrainMinDF['TrainMinIdx']==trainMinIdx].index[0]
            print(trainMinIdx, indexVal)
        else:
            btn_clicked = 'None'
    # time_val = hd.currentTrainMinDF.at[indexVal,'TimeStamp']
    data['anomalyIndex']=int(anomalyIndex)
    data['indexVal']=int(indexVal)
    # timeData['time_val'] = time_val
    jsret = json.dumps(data)
    # jsretTime = json.dumps(timeData)
    print(jsret, prev_dsbl, nxt_dsbl, prev_anm_dsbl, next_anm_dsbl)
    return jsret, prev_dsbl, nxt_dsbl, prev_anm_dsbl, next_anm_dsbl


