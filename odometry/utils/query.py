query_distinct_train = ("SELECT train_id \"TrainId\", "
						+ " to_char(MIN(time_stamp), 'YYYY-MM-DD HH:MI') \"MinDate\", "
						+" to_char(MAX(time_stamp), 'YYYY-MM-DD HH:MI') \"MaxDate\" "
						+ " FROM odometry.tbl_train_min_data GROUP BY train_id ORDER BY train_id")
query_FeaturesData=("SELECT train_min_idx \"TrainMinIdx\", "
					+ "seconds \"Seconds\", "
					+ "left_axle_speed \"LeftAxleSpeed\", " 
					+ "odo_speed \"OdoSpeed\", "
					+ "right_axle_speed \"RightAxleSpeed\" "  
					+ "FROM odometry.tbl_fine_feature "
					+ "WHERE train_min_idx = {train_min_idx} "
					+ "ORDER BY train_min_idx, seconds")
query_TrainMinData = ("SELECT train_min_idx \"TrainMinIdx\", "
					+ "train_id \"TrainId\", "
					+ "to_char(time_stamp, 'YYYY-MM-DD HH:MI') \"TimeStamp\", "
					+ "anomaly_score \"AnomalyScore\", "
					+ "expert_comment \"ExpertComment\", "
					+ "class_axle_event \"LblAxleEvent\", "
					+ "probability_axle_event, "
					+ "class_odo_algo \"LblOdoAlgo\", " 
					+ "probability_odo_algo, "
					+ "class_speed \"LblSpeed\" , "
					+ "probability_speed "
					+ "FROM odometry.tbl_train_min_data "
					+ "WHERE train_id = {train_id} "
					+ " ORDER BY anomaly_Score DESC")
query_train_min_update= ("UPDATE odometry.tbl_train_min_data" 
					    + " SET class_axle_event ='{axle_class}' "
					    + " , class_odo_algo = '{odo_class}' "
					    + ", class_speed = '{speed_class}' "
					    + ", expert_comment = '{expert_comment}' "
					    + " WHERE train_min_idx = {id}")
query_TrainMinRangeData = ("SELECT train_min_idx \"TrainMinIdx\", "
					+ "train_id \"TrainId\", "
					+ "to_char(time_stamp, 'YYYY-MM-DD HH:MI') \"TimeStamp\", "
					+ "anomaly_score \"AnomalyScore\", "
					+ "expert_comment \"ExpertComment\", "
					+ "class_axle_event \"LblAxleEvent\", "
					+ "probability_axle_event, "
					+ "class_odo_algo \"LblOdoAlgo\", " 
					+ "probability_odo_algo, "
					+ "class_speed \"LblSpeed\" , "
					+ "probability_speed "
					+ "FROM odometry.tbl_train_min_data "
					+ "WHERE train_id = {train_id} "
					+ " AND time_stamp>='{startDate}' "
					+ " AND time_stamp<='{endDate}' "
					+ " ORDER BY anomaly_Score DESC")
quey_AllTrainData = ("SELECT train_id \"TrainId\", "
					+ "to_char(time_stamp, 'YYYY-MM-DD HH:MI') \"TimeStamp\", "
					+ "anomaly_score \"AnomalyScore\", "
					+ "class_axle_event \"LblAxleEvent\", "
					+ "class_odo_algo \"LblOdoAlgo\", " 
					+ "class_speed \"LblSpeed\" "
					+ "FROM odometry.tbl_train_min_data "
					+ " ORDER BY Train_id, anomaly_Score DESC")