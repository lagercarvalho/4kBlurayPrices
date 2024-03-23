import psycopg2
import os
import json
import sys
from scrapers import cdon, kvarn, imusic

with open("config.json", "r") as f:
    config = json.load(f)["database"]

conn = psycopg2.connect(
    database=config["name"],
    host=config["host"],
    user=config["user"],
    password=config["password"],
    port=config["port"],
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
TRUNCATE TABLE movies;
"""
cursor.execute(create_query)
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
    COPY movies FROM '/var/lib/csv/{file}'
    DELIMITER ',' CSV HEADER;
    """
    cursor.execute(copy_query)

conn.commit()

print("Data stored in DB")

cursor.close()
conn.close()