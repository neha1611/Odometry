import pandas as pd
import pandasql as ps
from app import engine, metadata, sqlalchemy
from sqlalchemy.sql import text
from utils.query import *

connection = engine.connect()
TBLTrainMin = sqlalchemy.Table('tbl_train_min_data', metadata, autoload=True, autoload_with=engine)

# Print the column names
# print(TBLTrainMin.columns.keys())
# print(repr(metadata.tables['tbl_train_min_data']))
query = sqlalchemy.select([TBLTrainMin]).order_by(TBLTrainMin.columns.train_id, sqlalchemy.desc(TBLTrainMin.columns.anomaly_score))
resultSet = connection.execute(query).fetchall()
TrainMinDataFrame = pd.DataFrame(resultSet)
TrainMinDataFrame.columns = resultSet[0].keys()
TrainMinDataFrame = TrainMinDataFrame.rename(columns={"train_min_idx": "TrainMinIdx", "train_id": "TrainId", "time_stamp":"TimeStamp", "anomaly_score":"AnomalyScore", "expert_comment":"ExpertComment", "class_axle_event":"LblAxleEvent", "class_odo_algo":"LblOdoAlgo", "class_speed":"LblSpeed"})
TrainMinDataFrame.reset_index(inplace=True)
# print(TrainMinDataFrame)
TrainMinDataFrame.head()

FineSpeedDataFrame = pd.read_sql(query_FineSpeedData, engine)
FineSpeedDataFrame.reset_index(inplace=True)
# TrainMinDataFrame = pd.read_sql(query_TrainMinData, engine)
# TrainMinDataFrame.reset_index(inplace=True)
listOfTrains =TrainMinDataFrame.TrainId.unique() 
listTime = TrainMinDataFrame.TimeStamp.unique()




