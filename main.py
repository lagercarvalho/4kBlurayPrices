import psycopg2
import os

conn = psycopg2.connect(database="postgres",
                        host="localhost",
                        user="postgres",
                        password="mysecretpassword",
                        port="5432")

cursor = conn.cursor()

truncate_query = "TRUNCATE TABLE movies;"
cursor.execute(truncate_query)
conn.commit()

for file in os.listdir('data'):
    vendor = file[:-4] if file.endswith('.csv') else None
    if not vendor:
        continue

    with open(f'data/{file}', 'r') as f:
        print(f'Importing {file} into {vendor} database')
        copy_query = f"""
        COPY movies FROM '/var/lib/csv/{file}'
        DELIMITER ',' CSV HEADER;
        """
        cursor.execute(copy_query)

conn.commit()

cursor.close()
conn.close()


