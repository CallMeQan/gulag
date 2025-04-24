DROP TABLE sensor_data;
DROP TABLE forgot_password;
DROP TABLE mobile_session;
DROP TABLE personal_stat;
DROP TABLE users;
DROP TABLE run_history;

CREATE EXTENSION IF NOT EXISTS postgis;

CREATE TABLE users (
    user_id SERIAL PRIMARY KEY,
    username VARCHAR(25) NOT NULL UNIQUE,
    password VARCHAR(60) NOT NULL,
    email VARCHAR(320) NOT NULL UNIQUE,
    name VARCHAR(25) NOT NULL,
    admin BOOLEAN,
    goal FLOAT DEFAULT 1
);

CREATE TABLE sensor_data (
data_id SERIAL PRIMARY KEY,
user_id INT NOT NULL REFERENCES users(user_id),
start_time BIGINT NOT NULL,
created_at TIMESTAMPTZ NOT NULL,
location GEOMETRY(Point, 4326) NOT NULL
);

CREATE TABLE forgot_password (
   fp_id SERIAL PRIMARY KEY,
   email VARCHAR(320) NOT NULL,
   created_at TIMESTAMPTZ DEFAULT NOW(),
   hashed_timestamp VARCHAR(100) NOT NULL
);

CREATE TABLE mobile_session (
	mobile_id SERIAL PRIMARY KEY,
	user_id INT NOT NULL REFERENCES users(user_id),
created_at TIMESTAMPTZ NOT NULL,
hashed_timestamp CHAR(100) NOT NULL
);

CREATE TABLE personal_stat ( 
    person_id SERIAL PRIMARY KEY,
    user_id INT NOT NULL REFERENCES users(user_id),
    weight FLOAT NOT NULL DEFAULT 70,
    height FLOAT NOT NULL DEFAULT 1.7,
    age INT NOT NULL DEFAULT 20
);

CREATE TABLE run_history (
	run_id SERIAL PRIMARY KEY,
	user_id INT NOT NULL,
	start_time TIMESTAMPTZ NOT NULL,
	finish_goal INT NOT NULL,
	calorie FLOAT NOT NULL,
	step INT NOT NULL,
	total_distance FLOAT NOT NULL,
	total_time INTERVAL NOT NULL,
	pace FLOAT NOT NULL
);

-------------------------------------------
-- Insert sample data into users table --
-------------------------------------------
INSERT INTO users (username, password, email, name, admin, goal) VALUES
('alice123', 'hashed_password_1', 'alice@example.com', 'Alice', FALSE, 1),
('bob_dev', 'hashed_password_2', 'bob@example.com', 'Bob', FALSE, 1),
('charlie99', 'hashed_password_3', 'charlie@example.com', 'Charlie', FALSE, 1),
('david_admin', 'hashed_password_4', 'david@example.com', 'David', TRUE, 2),
('eve_runner', 'hashed_password_5', 'eve@example.com', 'Eve', FALSE, 3),
('Ceenen', 'hashed_password_6', 'phuhn.a1.2124@gmail.com', 'Fuu', TRUE, 2),
('cnn', '$2b$12$yikB/GYPtljv6lJDQd8OgO034wiNSWNO4Hl4kgpQ3phx/HqvmNudO', 'phu@gmail.com', 'cnn', True, 3);

------------------------------------------------------
-- Insert samples into sensor_data records --
------------------------------------------------------

INSERT INTO sensor_data (user_id, start_time, created_at, location) VALUES
(1, 1681638000, '2025-04-15T19:30:00+00', ST_SetSRID(ST_MakePoint(106.66105252, 10.76355252), 4326)),
(1, 1681638000, '2025-04-15T19:40:00+00', ST_SetSRID(ST_MakePoint(106.66200000, 10.76400000), 4326)),
(1, 1681638000, '2025-04-15T19:50:00+00', ST_SetSRID(ST_MakePoint(106.66300000, 10.76500000), 4326)),
(1, 1681638000, '2025-04-15T20:00:00+00', ST_SetSRID(ST_MakePoint(106.66400000, 10.76600000), 4326)),
(1, 1681638000, '2025-04-15T20:10:00+00', ST_SetSRID(ST_MakePoint(106.66500000, 10.76700000), 4326)),
(1, 1681638000, '2025-04-15T20:20:00+00', ST_SetSRID(ST_MakePoint(106.66600000, 10.76800000), 4326)),
(1, 1681638000, '2025-04-15T20:30:00+00', ST_SetSRID(ST_MakePoint(106.66700000, 10.76900000), 4326)),
(1, 1681638000, '2025-04-15T20:40:00+00', ST_SetSRID(ST_MakePoint(106.66800000, 10.77000000), 4326)),
(1, 1681638000, '2025-04-15T20:50:00+00', ST_SetSRID(ST_MakePoint(106.66900000, 10.77100000), 4326)),
(1, 1681638000, '2025-04-15T21:00:00+00', ST_SetSRID(ST_MakePoint(106.67000000, 10.77200000), 4326)),
(1, 1681598400, '2025-04-15T08:30:00+00', ST_SetSRID(ST_MakePoint(106.7000, 10.7769), 4326)),
(1, 1681602000, '2025-04-15T09:30:00+00', ST_SetSRID(ST_MakePoint(106.6820, 10.7626), 4326)),
(1, 1681605600, '2025-04-15T10:30:00+00', ST_SetSRID(ST_MakePoint(106.6602, 10.7629), 4326)),
(1, 1681609200, '2025-04-15T11:30:00+00', ST_SetSRID(ST_MakePoint(106.6297, 10.7764), 4326)),
(1, 1681612800, '2025-04-15T12:30:00+00', ST_SetSRID(ST_MakePoint(106.6410, 10.7915), 4326)),
(1, 1681616400, '2025-04-15T13:30:00+00', ST_SetSRID(ST_MakePoint(106.6756, 10.7620), 4326)),
(1, 1681620000, '2025-04-15T14:30:00+00', ST_SetSRID(ST_MakePoint(106.7120, 10.7767), 4326)),
(1, 1681623600, '2025-04-15T15:30:00+00', ST_SetSRID(ST_MakePoint(106.6900, 10.7710), 4326)),
(1, 1681598400, '2025-04-15T08:30:00+00', ST_SetSRID(ST_MakePoint(106.7000, 10.7769), 4326)),
(2, 1681602000, '2025-04-15T09:30:00+00', ST_SetSRID(ST_MakePoint(106.6820, 10.7626), 4326)),
(2, 1681605600, '2025-04-15T10:30:00+00', ST_SetSRID(ST_MakePoint(106.6602, 10.7629), 4326)),
(2, 1681609200, '2025-04-15T11:30:00+00', ST_SetSRID(ST_MakePoint(106.6297, 10.7764), 4326)),
(2, 1681612800, '2025-04-15T12:30:00+00', ST_SetSRID(ST_MakePoint(106.6410, 10.7915), 4326)),
(2, 1681616400, '2025-04-15T13:30:00+00', ST_SetSRID(ST_MakePoint(106.6756, 10.7620), 4326)),
(2, 1681620000, '2025-04-15T14:30:00+00', ST_SetSRID(ST_MakePoint(106.7120, 10.7767), 4326)),
(3, 1681623600, '2025-04-15T15:30:00+00', ST_SetSRID(ST_MakePoint(106.6900, 10.7710), 4326)),
(3, 1681627200, '2025-04-15T16:30:00+00', ST_SetSRID(ST_MakePoint(106.7012, 10.7780), 4326)),
(3, 1681630800, '2025-04-15T17:30:00+00', ST_SetSRID(ST_MakePoint(106.6422, 10.7920), 4326)),
(3, 1681634400, '2025-04-15T18:30:00+00', ST_SetSRID(ST_MakePoint(106.7130, 10.7770), 4326)),
(4, 1681638000, '2025-04-15T19:30:00+00', ST_SetSRID(ST_MakePoint(106.66105252, 10.76355252), 4326)),
(4, 1681641600, '2025-04-15T20:30:00+00', ST_SetSRID(ST_MakePoint(106.6835, 10.7633), 4326)),
(4, 1681645200, '2025-04-15T21:30:00+00', ST_SetSRID(ST_MakePoint(106.6910, 10.7720), 4326)),
(4, 1681648800, '2025-04-15T22:30:00+00', ST_SetSRID(ST_MakePoint(106.6765, 10.7625), 4326)),
(4, 1681652400, '2025-04-15T23:30:00+00', ST_SetSRID(ST_MakePoint(106.6995, 10.7755), 4326)),
(4, 1681656000, '2025-04-16T00:30:00+00', ST_SetSRID(ST_MakePoint(106.6302, 10.7770), 4326)),
(4, 1681659600, '2025-04-16T01:30:00+00', ST_SetSRID(ST_MakePoint(106.6430, 10.7910), 4326)),
(4, 1681663200, '2025-04-16T02:30:00+00', ST_SetSRID(ST_MakePoint(106.6770, 10.7610), 4326)),
(4, 1681666800, '2025-04-16T03:30:00+00', ST_SetSRID(ST_MakePoint(106.6920, 10.7700), 4326));

------------------------------------------------
-- Insert 3 sample forgot_password records --
------------------------------------------------

INSERT INTO forgot_password (email, hashed_timestamp) VALUES
('phuhn.a1.2124@gmail.com', 'hash1'),
('bob@example.com', 'hash2');

------------------------------------------------------
-- Insert Personal Stat --
------------------------------------------------------
INSERT INTO personal_stat (user_id, weight, height, age) VALUES
(7, 70, 169, 19);

INSERT INTO run_history (user_id, start_time, finish_goal, calorie, step, total_distance, total_time, pace) VALUES
-- January 2025
(7, '2025-01-03 07:15:00+00', 0, 320.5, 6500, 5.0, '00:30:00', 6.0),
(7, '2025-01-10 06:45:00+00', 0, 420.0, 9100, 7.0, '00:42:00', 6.0),
(7, '2025-01-17 18:20:00+00', 0, 220.3, 4000, 3.2, '00:20:00', 6.4),
(7, '2025-01-25 08:00:00+00', 0, 670.1, 12500, 10.0, '01:00:00', 6.0),

-- February 2025
(7, '2025-02-02 07:10:00+00', 0, 500.0, 10500, 8.0, '00:50:00', 6.25),
(7, '2025-02-12 19:30:00+00', 1, 410.5, 8000, 6.2, '00:36:00', 5.8),
(7, '2025-02-18 06:00:00+00', 1, 290.0, 5100, 4.0, '00:25:00', 6.0),
(7, '2025-02-27 07:45:00+00', 1, 685.0, 13000, 10.0, '01:05:00', 6.5),

-- March 2025
(7, '2025-03-03 06:30:00+00', 0, 450.0, 9200, 7.0, '00:42:00', 6.0),
(7, '2025-03-09 07:00:00+00', 0, 210.0, 3800, 3.1, '00:18:00', 5.8),
(7, '2025-03-16 18:00:00+00', 1, 350.0, 6400, 5.0, '00:28:00', 5.6),
(7, '2025-03-25 06:15:00+00', 1, 590.0, 11700, 9.0, '00:55:00', 6.1),

-- April 2025
(7, '2025-04-01 07:20:00+00', 0, 410.0, 8200, 6.0, '00:35:00', 5.8),
(7, '2025-04-08 07:50:00+00', 1, 530.0, 10800, 8.0, '00:48:00', 6.0),
(7, '2025-04-15 19:00:00+00', 1, 260.0, 5200, 4.0, '00:24:00', 6.0),
(7, '2025-04-24 06:00:00+00', 1, 680.0, 12800, 10.0, '01:00:00', 6.0);
