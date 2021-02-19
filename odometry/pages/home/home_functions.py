from app import engine

def updateTrainData(t):
	print(t)
	# query = sqlalchemy.update(TBLTrainMin).values(LblAxleEvent = t.LblAxleEvent, 
	# 														LblOdoAlgo = t.LblOdoAlgo, 
	# 														LblSpeed = t.LblSpeed, 
	# 														ExpertComment = t.ExpertComment )
	# query = query.where(TBLTrainMin.columns.train_min_idx == t.TrainMinIdx)
	# results = connection.execute(query)

	query_train_min_update = ("UPDATE odometry.tbl_train_min_data "
	    +"SET class_axle_event ='{axle_class}' "
	    +",class_odo_algo = '{odo_class}' "
	    +",class_speed = '{speed_class}' "
	    +",expert_comment = '{expert_comment}' "
	    +"WHERE train_min_idx = {id}"
		).format(axle_class=str(t.LblAxleEvent), odo_class=str(t.LblOdoAlgo), 
		speed_class=str(t.LblSpeed), expert_comment=str(t.ExpertComment),
		id=str(t.TrainMinIdx))
	print("UpdateQuery"+query_train_min_update)
	with engine.begin() as conn:     conn.execute(text(query_train_min_update))