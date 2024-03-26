import mysql.connector
import os
import json
import sys
from scrapers import cdon, kvarn, imusic

with open("config.json", "r") as f:
    config = json.load(f)["mysql"]

conn = mysql.connector.connect(
    database=config["name"],
    host=config["host"],
    user=config["user"],
    password=config["password"],
    port=config["port"]
)

cursor = conn.cursor()
create_query = f"""
CREATE TABLE IF NOT EXISTS movies(
    vendor varchar(32) not null,
    title varchar(256) not null,
    current_price real not null,
    previous_price real not null,
    sale real,
    status varchar(32),
    img_src varchar(256),
    list_src varchar(256)
);
"""
cursor.execute(create_query)
cursor.fetchall()
conn.commit()

truncate_query = "TRUNCATE TABLE movies;"
cursor.execute(truncate_query)
cursor.fetchall()
conn.commit()

if "-s" in sys.argv:
    cdon.scrape_cdon()
    kvarn.scrape_kvarn()
    imusic.scrape_imusic()
else:
    print("use -s to run all scrapers")

for file in os.listdir("data"):
    vendor = file[:-4] if file.endswith(".csv") else None
    if not vendor:
        continue

    print(f"Importing {file}")
    copy_query = f"""
    LOAD DATA INFILE '/var/lib/csv/{file}'
    INTO TABLE movies
    FIELDS TERMINATED BY ',' 
    ENCLOSED BY '"'
    LINES TERMINATED BY '\\r\\n'
    IGNORE 1 LINES;
    """
    cursor.execute(copy_query)
    cursor.fetchall()
    conn.commit()

print("Data stored in DB")

cursor.close()
conn.close()