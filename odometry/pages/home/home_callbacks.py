import json, datetime
from dateutil import tz
import plotly.express as px
import pandas as pd
import plotly.graph_objects as go
import pages.home.home_data as hd
from utils.functions import *
from dash.dependencies import Input, Output, State, ClientsideFunction
from app import app
from pages.home.home_data import currentTrainMinDF,  currentTrainFeatureDF, TrainListDF
from pages.home.home_functions import *

app.clientside_callback(
    output=Output('hid_timeoffset', 'children'),
    inputs=[Input('hid_body_loaded', 'children')],
    clientside_function = ClientsideFunction(
        namespace='clientside',
        function_name ='getOffset'
    )
)

#When a Train is selected in dropdown, call this function 
#Sets hidden variable hid_train to TrainId,
#Sets from and to date in dateTime range picker to Min and max date
#Calculates number of lables
@app.callback(
    [
    Output("dateRange", "startDate"),
    Output("dateRange", "endDate"),
    Output(component_id='hid_train', component_property='children')],
    Input(component_id='slct_train', component_property='value')
)
def onUpdateTrain(train_val):
    trainDF  = TrainListDF.query("TrainId==@train_val")
    trainDF.reset_index()
    retMinDate = (trainDF.iloc[0]['MinDate'])
    retMaxDate = (trainDF.iloc[0]['MaxDate'])
    data = {}
    data['train_id_val']=train_val
    data['nClicksTimestamp'] = datetime.datetime.now().timestamp()*1000
    #Count Train Level lables
    #TODO implement update all lables count
    # allLblCount = len(lbldAllEvents.index)
    # trnLblCount = len(lbldTrainEvents.index)
    jsret = json.dumps(data)
    return retMinDate, retMaxDate, jsret

#Called on Update of hidden variable hid_train (change of Train Id selection)
#Or when to and from date is changed in Date Picker
#Also correct timezoneOffset when picking time from DateTimePicker
#updates hidden variable hid_time_range.
@app.callback(
    Output(component_id='hid_time_range', component_property='children'),
    [Input(component_id='dateRange', component_property='startDate'),
    Input(component_id='dateRange', component_property='endDate'),
    Input(component_id='hid_train', component_property='children')],
    State("hid_timeoffset", "children")
)
def update_time_range(startDate, endDate, train_var, hid_offset):
    print("called back of datetimepicker")
    offset = json.loads(hid_offset)['offset']
    #Time offset needs to be corrected only when picking time from DateTime Picker. 
    if(len(startDate)>19):
        startDate = startDate[:-8]+'Z'
        startDate = datetime.datetime.strptime(startDate,"%Y-%m-%dT%H:%MZ")
        startDate = startDate-datetime.timedelta(minutes=int(offset))
        startDate = startDate.strftime("%Y-%m-%d %H:%M")
    #get all data for selected Train
    train_val = json.loads(train_var)['train_id_val']
    #query DB for data for Selected Train and Time Range
    hd.currentTrainMinDF  = getTrainDataInRange(train_val,startDate, endDate )
    print(hd.currentTrainMinDF[:5])
    # print(hd.currentTrainMinDF.at[0, 'TrainMinIdx'])
    data={}
    data['start_date'] = startDate
    data['end_date'] = endDate
    data['nClicksTimestamp'] = datetime.datetime.now().timestamp()*1000
    jsret = json.dumps(data)
    print(jsret)
    return jsret


#TODO break into two which button is clicked and submit functionality
#Use n_clicks_timestamp to determine which button was clicked.
#Update the IndexVal and Anomaly Index hidden variables base on which button is clicked.
#Also, enable and disable various buttons accordingly
#In case Submit button is clicked, then udated user's selection for labels and comments in DB
@app.callback(
    [Output("divAnomalyIndex", "children"),
     Output('prev_btn', 'disabled'),
     Output('nxt_btn', 'disabled'),
     Output('btn_prev_anm', 'disabled'),
     Output('btn_nxt_anm', 'disabled'),
     Output('id_alert_submit_success', 'is_open'),
     Output('id_alert_submit_failure', 'is_open'),
     Output(component_id='lbl1', component_property='children'),
     Output(component_id='lbl2', component_property='children') ],
    [Input('sbmt_lbl_btn', 'n_clicks_timestamp'),
     Input('prev_btn', 'n_clicks_timestamp'),
     Input('nxt_btn', 'n_clicks_timestamp'),
     Input('btn_prev_anm', 'n_clicks_timestamp'),
     Input('btn_nxt_anm', 'n_clicks_timestamp'), 
     Input(component_id='hid_time_range', component_property='children')],
    [State(component_id="divAnomalyIndex", component_property="children"), 
     State("rd_axle", "value"),
     State("rd_algo","value"),
     State("rd_speed", "value"),
     State("expert_comment", "value"),
     State("hid_train","children")]
)
def updated_clicked(sbmtBtn_clicks, prevAnm_clicks, nxtAnm_clicks, 
    prevBtn_clicks, nextBtn_clicks, hid_time_range, vars, lblAxl, lblOdo, lblSpd, exptCmt,hid_train):
    prev_dsbl=False
    nxt_dsbl=False
    prev_anm_dsbl=False
    next_anm_dsbl=False
    updateSuccess=False
    updateFailure=False
    train_val = json.loads(hid_train)['train_id_val']
    range_nclicksTimeStamp = json.loads(hid_time_range)['nClicksTimestamp']
    data = json.loads(vars)
    anomalyIndex = data['anomalyIndex']
    indexVal = data['indexVal']
    max_val = max(range_nclicksTimeStamp, sbmtBtn_clicks, prevAnm_clicks, nxtAnm_clicks, prevBtn_clicks, nextBtn_clicks)
    if (max_val>0):
        if(range_nclicksTimeStamp==max_val):
            indexVal=0
            anomalyIndex=0
            prev_dsbl=True
            prev_anm_dsbl=True
        elif sbmtBtn_clicks==max_val:
            hd.currentTrainMinDF.at[indexVal,'LblAxleEvent']=lblAxl
            hd.currentTrainMinDF.at[indexVal,'LblOdoAlgo']=lblOdo
            hd.currentTrainMinDF.at[indexVal,'LblSpeed']=lblSpd
            hd.currentTrainMinDF.at[indexVal,'ExpertComment']=exptCmt
            currentDF = eval('hd.currentTrainMinDF.iloc[{}]'.format(indexVal))
            result = updateTrainData(currentDF)
            if result==True:
                updateSuccess=True
                hd.TrainMinDataFrame = getAllTrainMinData()
            else:
                updateFailure=True
        elif nxtAnm_clicks==max_val:
            anomalyIndex = anomalyIndex+1
            indexVal = anomalyIndex
        elif prevAnm_clicks==max_val:
            anomalyIndex=anomalyIndex-1
            indexVal = anomalyIndex
            if anomalyIndex==0:
                 prev_anm_dsbl=True
        elif prevBtn_clicks==max_val:
            trainMinIdx = hd.currentTrainMinDF.at[indexVal,'TrainMinIdx']
            trainMinIdx = trainMinIdx-1
            indexVal = hd.currentTrainMinDF[hd.currentTrainMinDF['TrainMinIdx']==trainMinIdx].index[0]
            if indexVal==0:
                prev_dsbl=False
        elif nextBtn_clicks==max_val:
            trainMinIdx = hd.currentTrainMinDF.at[indexVal,'TrainMinIdx']
            trainMinIdx = trainMinIdx+1
            indexVal = hd.currentTrainMinDF[hd.currentTrainMinDF['TrainMinIdx']==trainMinIdx].index[0]
    lbldTrainEvents = hd.TrainMinDataFrame.query('TrainId==@train_val and (LblAxleEvent.notna() or LblSpeed.notna() or LblOdoAlgo.notna())')
    trnLblCount = len(lbldTrainEvents.index)
    lbldAllEvents= hd.TrainMinDataFrame.query('LblAxleEvent.notna() or LblSpeed.notna() or LblOdoAlgo.notna()')   
    allLblCount = len(lbldAllEvents.index)
    data['anomalyIndex']=int(anomalyIndex)
    data['indexVal']=int(indexVal)
    jsret = json.dumps(data)
    print(jsret, prev_dsbl, nxt_dsbl, prev_anm_dsbl, next_anm_dsbl, updateSuccess, updateFailure, allLblCount, trnLblCount)
    return jsret, prev_dsbl, nxt_dsbl, prev_anm_dsbl, next_anm_dsbl, updateSuccess, updateFailure,trnLblCount,allLblCount

#Update all output Elements - Map, Labels for Axle, Odo Algo and Speed, and Expert Comment
#Update the output Elements based on which tuple is to be shown determined by IndexVal
@app.callback(
    [Output(component_id='my_map', component_property='figure'),
    Output(component_id="rd_axle",  component_property="value"),
    Output(component_id="rd_algo",  component_property="value"),
    Output(component_id="rd_speed",  component_property="value"),
    Output(component_id="expert_comment",  component_property="value")],
    Input("divAnomalyIndex", "children"),#],
    # State(component_id='hid_train', component_property='children')
)
def update_output( hid_anmly):
    # train_val = json.loads(hid_train)['train_id_val']
    print("in Update Output")
    indexVal = json.loads(hid_anmly)['indexVal']
    print (indexVal)
    print(hd.currentTrainMinDF[:5])
    trainMinIdx_val = hd.currentTrainMinDF.at[indexVal,'TrainMinIdx']
    print(trainMinIdx_val)
    #Query DB for Features data based on TraiMinIdx. This is displayed in Line Graph
    t = getTrainFeatures(trainMinIdx_val)
    print("got Train Features")
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
        hovermode='closest', legend_orientation='h',plot_bgcolor="white",)
    figure.update_layout(legend=dict( orientation="h",yanchor="bottom",y=1.02,xanchor="right",x=1, 
        font=dict(
            family="WorkSans",
            size=12,
            color="black"
        )))
    print("print graph done")
    retAxleEvent = hd.currentTrainMinDF.at[indexVal,'LblAxleEvent']
    retOdoAlgo = hd.currentTrainMinDF.at[indexVal,'LblOdoAlgo']
    retSpeed = hd.currentTrainMinDF.at[indexVal,'LblSpeed']
    retExpertComment = hd.currentTrainMinDF.at[indexVal,'ExpertComment']
    print(retAxleEvent, retOdoAlgo, retSpeed, retExpertComment)
    return figure, retAxleEvent, retOdoAlgo, retSpeed, retExpertComment


