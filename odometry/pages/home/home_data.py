import pandas as pd
import pandasql as ps

FineSpeedDataFrame = pd.read_csv("C:\\Users\\lenovo\\Desktop\\Teliolabs\\DashTry\\data\\FineSpeedData.csv")
FineSpeedDataFrame = FineSpeedDataFrame.sort_values(by='TrainMinIdx', ascending = True)
FineSpeedDataFrame.reset_index(inplace=True)
TrainMinDataFrame = pd.read_csv("C:\\Users\\lenovo\\Desktop\\Teliolabs\\DashTry\\data\\TrainMinData.csv")
TrainMinDataFrame = TrainMinDataFrame.sort_values(by='AnomalyScore', ascending = False)
TrainMinDataFrame.reset_index(inplace=True)
# sdf = ps.sqldf("select FineSpeedDataFrame.TrainMinIdx, Seconds, Train_Id, Time_Stamp, AnomalyScore "
# 	+"from FineSpeedDataFrame, TrainMinDataFrame "
# 	+"where FineSpeedDataFrame.TrainMinIdx=TrainMinDataFrame.TrainMinIdx "
# 	+" order by AnomalyScore desc")
# sdf.reset_index()
listOfTrains =TrainMinDataFrame.Train_Id.unique() 
listTime = TrainMinDataFrame.Time_Stamp.unique()
