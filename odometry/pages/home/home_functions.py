from app import engine
from utils.query import *
import pandas as pd
def updateTrainData(t):
	updateQuery = query_train_min_update.format(axle_class=str(t.LblAxleEvent), odo_class=str(t.LblOdoAlgo), 
		speed_class=str(t.LblSpeed), expert_comment=str(t.ExpertComment),
		id=str(t.TrainMinIdx))
	# print("UpdateQuery"+updateQuery)
	with engine.begin() as conn:     conn.execute(updateQuery)

def getDistinctTrains():
	return pd.read_sql(query_distinct_train, engine)
def getTrainData(trainId):
	trainMinQuery = query_TrainMinData.format(train_id = trainId)
	# print(trainMinQuery)
	TrainMinDF = pd.read_sql(trainMinQuery, engine)
	return TrainMinDF

def getTrainFeatures(trainMinIdx):
	featureQuery = query_FeaturesData.format(train_min_idx = trainMinIdx)
	# print(featureQuery)
	FeaturesData = pd.read_sql(featureQuery, engine)
	return FeaturesData

def getTrainDataInRange(train_val, startDate, endDate):
	rangeQuery = query_TrainMinRangeData.format(train_id = train_val, startDate=startDate, endDate=endDate)
	print(rangeQuery)
	TrainTimeRangeData = pd.read_sql(rangeQuery, engine)
	return TrainTimeRangeData