from app import engine
from utils.query import *
import pandas as pd
from psycopg2 import OperationalError, errorcodes, errors
def updateTrainData(t):
	result=False
	updateQuery = query_train_min_update.format(axle_class=str(t.LblAxleEvent), odo_class=str(t.LblOdoAlgo), 
		speed_class=str(t.LblSpeed), expert_comment=str(t.ExpertComment),
		id=str(t.TrainMinIdx))
	# print("UpdateQuery"+updateQuery)
	try:
		with engine.begin() as conn:     conn.execute(updateQuery)
	except OperationalError as e:
		print_exception(err)
		conn.rollback()
		result=False
	else:
		result = True
	return result
	

def getDistinctTrains():
	return pd.read_sql(query_distinct_train, engine)
def getAllTrainMinData():
	return pd.read_sql(quey_AllTrainData, engine)

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

def print_psycopg2_exception(err):
	print ("Extensions.Diagnostics:", err.diag)
	print ("pgerror:", err.pgerror)
	print ("pgcode:", err.pgcode, "\n")