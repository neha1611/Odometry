
CREATE TABLE odometry.tbl_train_min_data
(
    train_min_idx integer NOT NULL,
    train_id integer NOT NULL,
    time_stamp timestamp NOT NULL,
    anomaly_score numeric NOT NULL,
    expert_comment varchar,
    class_axle_event VARCHAR(10),
    probability_axle_event numeric,
    class_odo_algo VARCHAR(10),
    probability_odo_algo numeric,
    class_speed VARCHAR(10),
    probability_speed numeric,
    
    PRIMARY KEY (train_min_idx)
);

ALTER TABLE odometry.tbl_train_min_data
    OWNER to postgres;


CREATE TABLE odometry.tbl_fine_feature
(
    train_min_idx integer NOT NULL,
    seconds integer NOT NULL,
    left_axle_speed numeric NOT NULL,
    odo_speed numeric NOT NULL,
    right_axle_speed numeric NOT NULL,
    PRIMARY KEY (train_min_idx, seconds),
    CONSTRAINT fk_train_min FOREIGN KEY (train_min_idx)
        REFERENCES odometry.tbl_train_min_data (train_min_idx) MATCH SIMPLE
        ON UPDATE CASCADE
        ON DELETE CASCADE
        NOT VALID
);

ALTER TABLE odometry.tbl_fine_feature
    OWNER to postgres;