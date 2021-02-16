CREATE TABLE public.tbl_train_min_data
(
    train_min_idx integer NOT NULL,
    train_id integer NOT NULL,
    time_stamp "char" NOT NULL,
    anomaly_score numeric NOT NULL,
    expert_comment "char",
    class_axle_event "char",
    probability_axle_event numeric,
    class_odo_algo "char",
    probability_odo_algo numeric,
    class_speed "char",
    probability_speed numeric,
    
    PRIMARY KEY (train_min_idx)
);

ALTER TABLE public.tbl_train_min_data
    OWNER to postgres;


CREATE TABLE public.tbl_fine_feature
(
    train_min_idx integer NOT NULL,
    seconds integer NOT NULL,
    left_axle_speed numeric NOT NULL,
    odo_speed numeric NOT NULL,
    right_axle_speed numeric NOT NULL,
    PRIMARY KEY (train_min_idx, seconds),
    CONSTRAINT fk_train_min FOREIGN KEY (train_min_idx)
        REFERENCES public.tbl_train_min_data (train_min_idx) MATCH SIMPLE
        ON UPDATE CASCADE
        ON DELETE CASCADE
        NOT VALID
);

ALTER TABLE public.tbl_fine_feature
    OWNER to postgres;