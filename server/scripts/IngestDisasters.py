import psycopg2
import hjson
import os

FILE_PATH = '../data/us_disasters_clean.json'

PASSWORD = os.environ.get("DB_PASSWORD")

connection_params = {
    'dbname': 'disaster_viewer',
    'user': 'jackyoungadmin',
    'password': PASSWORD,
    'host': 'localhost',
    'port': '5432'
}

connection = psycopg2.connect(**connection_params)
cursor = connection.cursor()

insert_query = """
        INSERT INTO disasters (id,disaster_type, begin_date, end_date, fips_code, latitude, longitude)
        VALUES (%s, %s, %s, %s, %s, %s, %s);
        """

try:
    with open(FILE_PATH, 'r') as file:
        json_data = hjson.load(file)
except OSError:
    print(f'Error reading file {OSError}')


if isinstance(json_data, list):
    for obj in json_data:
        data = (obj["id"], obj['disaster_type'], obj['begin_date'],
                obj['end_date'], obj['fips_code'], obj['latitude'], obj['longitude'])
        cursor.execute(insert_query, data)

remove_null_query = """
DELETE FROM disasters
WHERE id = 'NA'
   OR disaster_type = 'NA'
   OR begin_date = 'NA'
   OR end_date = 'NA'
   OR fips_code = 'NA'
   OR latitude = 'NA'
   OR longitude = 'NA';
"""

cursor.execute(remove_null_query)

connection.commit()
