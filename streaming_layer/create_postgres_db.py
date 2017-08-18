##########################################################################################
# Dengue Fever Prediction System
# W205 Summer 2017 Final Project
# Felipe Campos, Frank Shannon, Josh Wilson and Matthew Holmes
##########################################################################################
# Streaming Layer: Database Creation script
#
# This is a setup script for the Streaming layer, which creates the database and tables
# schema that will store weather prediction data and dengue case prediction for the
# next seven days.
#
##########################################################################################

import sys
import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

print("################################################")
print("Dengue Fever Prediction System")
print("Streaming Layer: Database Creation Script")
print("################################################")
print(" ")
print("Initiating database creation:")
print(" * Connecting to PostgreSQL Server... ")

# Connect to the database
conn = psycopg2.connect(database="postgres", user="postgres", password="pass", host="localhost", port="5432")

print(" * Connected!")
print(" * Verifying if database already exists... ")

# Create the Database
try:
    # CREATE DATABASE can't run inside a transaction
    conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
    cur = conn.cursor()
    cur.execute("SELECT 1 from pg_database WHERE datname='denguepred';")
    record = cur.fetchone()
    if (record == None):
        print(" * Database does not exist, creating 'denguepred' database... ")
        cur.execute("CREATE DATABASE denguepred")
    else:
        print(" * Database already exists!")
    cur.close()
    conn.close()
except:
    print "Some unexpected error occurred."
    print "Quitting..."
    sys.exit()

print(" * Connecting to created database...")

# Connec to newly created DB
conn = psycopg2.connect(database="denguepred", user="postgres", password="pass", host="localhost", port="5432")

print(" * Connected!")
print(" * Creating tables... ")

# Create tables
try:
    cur = conn.cursor()
    cur.execute('''CREATE TABLE predictions
                        (index          SERIAL      PRIMARY KEY     NOT NULL,
                         city           INT                         NOT NULL,
                         wkfrstday      INT                         NOT NULL,
                         avg_temp_K     REAL                        NOT NULL,
                         dew_pt_temp_K  REAL                        NOT NULL,
                         max_temp_K     REAL                        NOT NULL,
                         min_temp_K     REAL                        NOT NULL,
                         rel_hum_pct    REAL                        NOT NULL,
                         avg_temp_C     REAL                        NOT NULL,
                         num_cases      REAL                        NOT NULL);''')
    conn.commit()
    conn.close()
    print(" * Tables created!")
except:
    print(" * Table already exists!")

print("Application database created!")
