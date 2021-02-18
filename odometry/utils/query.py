query_FineSpeedData="""Select train_min_idx \"TrainMinIdx\", 
seconds \"Seconds\", 
left_axle_speed \"LeftAxleSpeed\", 
odo_speed \"OdoSpeed\", 
right_axle_speed \"RightAxleSpeed\"  
from odometry.tbl_fine_feature 
order by train_min_idx, seconds"""
query_TrainMinData = """Select train_min_idx \"TrainMinIdx\", 
train_id \"TrainId\", 
time_stamp \"TimeStamp\", 
anomaly_score \"AnomalyScore\",
expert_comment \"ExpertComment\", 
class_axle_event \"LblAxleEvent\", 
class_odo_algo \"LblOdoAlgo\",  
class_speed \"LblSpeed\" 
from odometry.tbl_train_min_data order by anomaly_Score desc"""