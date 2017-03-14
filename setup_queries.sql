-- Create Tables
CREATE TABLE USERS(ID INT PRIMARY KEY NOT NULL, LOGIN CHAR(50) NOT NULL, PASSWORD CHAR(100) NOT NULL);

CREATE TABLE FUNCTIONS(ID INT PRIMARY KEY NOT NULL, FUNCTION_NAME CHAR(50) NOT NULL, FUNCTION_TYPE INT NOT NULL);

CREATE TABLE FUNCTION_TYPES(ID INT PRIMARY KEY NOT NULL, FUNCTION_TYPE_NAME CHAR(50) NOT NULL);

CREATE TABLE USER_FUNCTIONS(ID INT PRIMARY KEY NOT NULL, USER_ID INT NOT NULL, FUNCTION_ID INT NOT NULL);

-- Create Indices
CREATE INDEX index_user_login_pw
ON USERS (LOGIN, PASSWORD);

CREATE INDEX index_function_names
ON FUNCTIONS (FUNCTION_NAME);

CREATE INDEX index_function_types
ON FUNCTIONS (FUNCTION_TYPE);

CREATE INDEX index_user_functions
ON USER_FUNCTIONS (USER_ID, FUNCTION_ID);

-- Insert Values
INSERT INTO USERS
VALUES (1, 'rasibic@uclan.ac.uk', 'testtest');

INSERT INTO USERS
VALUES (2, 'test@uclan.ac.uk', 'test');

INSERT INTO FUNCTION_TYPES
VALUES (1, 'lock');

INSERT INTO FUNCTION_TYPES
VALUES (2, 'communication');

INSERT INTO FUNCTIONS
VALUES (1, 'front door', 1);

INSERT INTO FUNCTIONS
VALUES (2, 'front door com', 2);

INSERT INTO USER_FUNCTIONS
VALUES (1, 1, 1);

INSERT INTO USER_FUNCTIONS
VALUES (2, 1, 2);

INSERT INTO USER_FUNCTIONS
VALUES (3, 2, 1);