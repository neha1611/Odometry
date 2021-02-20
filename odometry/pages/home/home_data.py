import pandas as pd
import pandasql as ps
from app import engine, metadata, sqlalchemy
# from sqlalchemy.sql import text
from pages.home.home_functions import *


#Get List of Trains with their Min Max dates (date might not be needed)
TrainListDF = getDistinctTrains()
print(TrainListDF)
print(pd.to_datetime('20190212'))
TrainListDF['MinDate'] = pd.to_datetime(TrainListDF['MinDate'])
TrainListDF['MaxDate'] = pd.to_datetime(TrainListDF['MaxDate'])
print(TrainListDF)
#Get teh Minute level data for the first Train by default
currentTrainMinDF  = getTrainData(TrainListDF.at[0,'TrainId'])
# startTime = currentTrainMinDF.at[0, 'TimeStamp']
#Get the seconds level data for the most anomalous minute by default
currentTrainFeatureDF = getTrainFeatures(currentTrainMinDF['TrainMinIdx'].iloc[0])
connection = engine.connect()
TBLTrainMin = sqlalchemy.Table('tbl_train_min_data', metadata, autoload=True, autoload_with=engine)

query = sqlalchemy.select([TBLTrainMin]).order_by(TBLTrainMin.columns.train_id, sqlalchemy.desc(TBLTrainMin.columns.anomaly_score))
resultSet = connection.execute(query).fetchall()
TrainMinDataFrame = pd.DataFrame(resultSet)
TrainMinDataFrame.columns = resultSet[0].keys()
TrainMinDataFrame = TrainMinDataFrame.rename(columns={"train_min_idx": "TrainMinIdx", "train_id": "TrainId", "time_stamp":"TimeStamp", "anomaly_score":"AnomalyScore", "expert_comment":"ExpertComment", "class_axle_event":"LblAxleEvent", "class_odo_algo":"LblOdoAlgo", "class_speed":"LblSpeed"})
TrainMinDataFrame.reset_index(inplace=True)
TrainMinDataFrame.head()




