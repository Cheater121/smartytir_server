# run it only one time for create tables

import psycopg2
from secret_info import user as u, password as p

conn = psycopg2.connect(
    host="localhost",
    database="flask_db1",
    user=u,
    password=p)

# Open a cursor to perform database operations
cur = conn.cursor()

# Execute a command: this creates a new table
cur.execute('CREATE TABLE users (id serial PRIMARY KEY,'
            'user_name varchar (255) NOT NULL UNIQUE,'
            'user_password varchar (255) NOT NULL DEFAULT 1);'
            )
cur.execute('CREATE TABLE games (id serial PRIMARY KEY,'
            'game_id integer NOT NULL,'
            'user_name varchar (255) NOT NULL,'
            'shoots integer NOT NULL,'
            'hits integer NOT NULL,'
            'CONSTRAINT fk_user_games FOREIGN KEY (user_name) REFERENCES users (user_name));'
            )

conn.commit()
cur.close()
conn.close()
