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
query = sqlalchemy.select([TBLTrainMin]).order_by(sqlalchemy.desc(TBLTrainMin.columns.anomaly_score))
resultSet = connection.execute(query).fetchall()
TrainMinDataFrame = pd.DataFrame(resultSet)
TrainMinDataFrame.columns = resultSet[0].keys()
TrainMinDataFrame = TrainMinDataFrame.rename(columns={"train_min_idx": "TrainMinIdx", "train_id": "TrainId", "time_stamp":"TimeStamp", "anomaly_score":"AnomalyScore", "expert_comment":"ExpertComment", "class_axle_event":"LblAxleEvent", "class_odo_algo":"LblOdoAlgo", "class_speed":"LblSpeed"})
TrainMinDataFrame.reset_index(inplace=True)
print(TrainMinDataFrame)
TrainMinDataFrame.head()

FineSpeedDataFrame = pd.read_sql(query_FineSpeedData, engine)
FineSpeedDataFrame.reset_index(inplace=True)
# TrainMinDataFrame = pd.read_sql(query_TrainMinData, engine)
# TrainMinDataFrame.reset_index(inplace=True)
listOfTrains =TrainMinDataFrame.TrainId.unique() 
listTime = TrainMinDataFrame.TimeStamp.unique()

# query_train_min_update=''

def updateTrainData(t):

	query = sqlalchemy.update(TBLTrainMin).values(LblAxleEvent = t.LblAxleEvent, 
															LblOdoAlgo = t.LblOdoAlgo, 
															LblSpeed = t.LblSpeed, 
															ExpertComment = t.ExpertComment )
	query = query.where(TBLTrainMin.columns.train_min_idx == t.TrainMinIdx)
	results = connection.execute(query)

	# query_train_min_update = ("UPDATE odometry.tbl_train_min_data "
	#     +"SET class_axle_event ='{axle_class}' "
	#     +",class_odo_algo = '{odo_class}' "
	#     +",class_speed = '{speed_class}' "
	#     +",expert_comment = '{expert_comment}' "
	#     +"WHERE train_min_idx = {id}"
	# 	).format(axle_class=str(t.LblAxleEvent), odo_class=str(t.LblOdoAlgo), 
	# 	speed_class=str(t.LblSpeed), expert_comment=str(t.ExpertComment),
	# 	id=str(t.TrainMinIdx))
	# print("UpdateQuery"+query_train_min_update)
	# with engine.begin() as conn:     conn.execute(text(query_train_min_update))
