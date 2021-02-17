import pandas as pd
import pandasql as ps
from app import dbConn

# FineSpeedDataFrame = pd.read_csv("C:\\Users\\lenovo\\Desktop\\Teliolabs\\DashTry\\data\\FineSpeedData.csv")
FineSpeedDataFrame = pd.read_sql("Select train_min_idx \"TrainMinIdx\", "
							+"seconds \"Seconds\", "
							+"left_axle_speed \"LeftAxleSpeed\", "
							+"odo_speed \"OdoSpeed\", "
							+"right_axle_speed \"RightAxleSpeed\" from odometry.tbl_fine_feature order by train_min_idx, seconds", dbConn)
# FineSpeedDataFrame = FineSpeedDataFrame.sort_values(by='TrainMinIdx', ascending = True)
FineSpeedDataFrame.reset_index(inplace=True)
FineSpeedDataFrame.head()
TrainMinDataFrame = pd.read_sql("Select train_min_idx \"TrainMinIdx\", "
							+"train_id \"TrainId\", "
    						+"time_stamp \"TimeStamp\", "
    						+"anomaly_score \"AnomalyScore\","
    						+"expert_comment \"ExpertComment\", "
    						+"class_axle_event \"LblAxleEvent\", "
    						+"class_odo_algo \"LblOdoAlgo\",  "
    						+"class_speed \"LblSpeed\" "
    						+"from odometry.tbl_train_min_data order by anomaly_Score desc", dbConn)
# TrainMinDataFrame.head()
# TrainMinDataFrame = pd.read_csv("C:\\Users\\lenovo\\Desktop\\Teliolabs\\DashTry\\data\\TrainMinData.csv")
# TrainMinDataFrame = TrainMinDataFrame.sort_values(by='AnomalyScore', ascending = False)
TrainMinDataFrame.reset_index(inplace=True)
# sdf = ps.sqldf("select FineSpeedDataFrame.TrainMinIdx, Seconds, Train_Id, Time_Stamp, AnomalyScore "
# 	+"from FineSpeedDataFrame, TrainMinDataFrame "
# 	+"where FineSpeedDataFrame.TrainMinIdx=TrainMinDataFrame.TrainMinIdx "
# 	+" order by AnomalyScore desc")
# sdf.reset_index()
listOfTrains =TrainMinDataFrame.TrainId.unique() 
listTime = TrainMinDataFrame.TimeStamp.unique()
