CREATE DATABASE py_test_db;

CREATE TABLE tb_countries (
    id int NOT NULL AUTO_INCREMENT,
    country varchar(255) NOT NULL,
    capital varchar(255) NOT NULL,
    PRIMARY KEY (id)
);

/* cleanup */
DELETE FROM tb_countries;
