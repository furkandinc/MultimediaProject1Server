drop table colorname;

CREATE TABLE ColorName (
        cn_id           VARCHAR(100) PRIMARY KEY,
        color_name      VARCHAR(255) NOT NULL,
        color_hex       VARCHAR(10) NOT NULL,
        color_r         INT NOT NULL,
        color_g         INT NOT NULL,
        color_b         INT NOT NULL
);