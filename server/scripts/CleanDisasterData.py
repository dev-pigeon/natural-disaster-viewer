import csv
import json
import os
import requests
import json

OUTPUT_FILE_PATH = "../data/us_disasters_clean.json"
INPUT_FILE_PATH = "../data/us_disaster_declarations.csv"
output_objects = []
fips_index_dict = {}

try:
    os.remove(OUTPUT_FILE_PATH)
    print("File removed successfully, contuining...")
except FileNotFoundError:
    print(f"Could not find file {OUTPUT_FILE_PATH}, contuining...")
except Exception as e:
    print(f"Could not remove file {OUTPUT_FILE_PATH}")
    print(e)


def create_json_entry(type, begin_date, end_date, fips, id):
    entry = {
        "disaster_type": type,
        "begin_date": begin_date,
        "end_date": end_date,
        "fips_code": fips,
        "id": id,
        "latitude": None,
        "longitude": None,
    }
    return entry


def update_dictionary(dict, key, value):
    prev_list = dict.get(key)
    if prev_list is not None:
        prev_list.append(value)
    else:
        dict[key] = [value]


def update_fips_values(latitude, longitude, values):
    for object_index in values:
        if object_index > len(output_objects):
            print(f"len {len(output_objects)} index {object_index}")
        output_objects[object_index]["latitude"] = latitude
        output_objects[object_index]["longitude"] = longitude


def get_fips_centroid(fips_code):
    state_code = fips_code[0: 2]
    county_code = fips_code[2:]
    request_url = f'https://tigerweb.geo.census.gov/arcgis/rest/services/TIGERweb/State_County/MapServer/1/query?where=STATE%3D%27{state_code}%27+AND+COUNTY%3D%27{county_code}%27&outFields=*&f=json'
    response = requests.get(request_url)
    response_json = response.json()
    features = response_json['features']
    if (len(features) > 0):
        lat_raw = features[0]['attributes']['CENTLAT']
        lon_raw = features[0]['attributes']['CENTLON']
        latitude, longitude = process_lat_lon(lat_raw, lon_raw)
        return latitude, longitude
    return 0, 0


def get_point_token(coord):
    token = coord[0]
    if token == "+":
        return ""
    return token


def process_lon(lon_raw, token):
    start = 1
    if lon_raw[start] == "0":
        start += 1
    return token + lon_raw[start:]


def process_lat_lon(lat_raw, lon_raw):
    lat_token = get_point_token(lat_raw)
    lon_token = get_point_token(lon_raw)
    lon = process_lon(lon_raw, lon_token)
    return lat_token + lat_raw[1:], lon


def update_entries_with_points():
    for fips_code in fips_index_dict.keys():
        latitude, longitude = get_fips_centroid(fips_code)
        update_fips_values(latitude, longitude, fips_index_dict.get(fips_code))


def read_file():
    with open(INPUT_FILE_PATH, "r") as file:
        reader = csv.reader(file)
        index = 0
        for line in reader:
            disaster_type = line[6]
            begin_date = line[12]
            end_date = line[13]
            fips = line[15]
            if fips[2:] != "000":
                id = line[22]
                entry = create_json_entry(
                    disaster_type, begin_date, end_date, fips, id)
                update_dictionary(fips_index_dict, key=fips, value=index)
                output_objects.append(entry)
                index += 1


def write_file():
    with open(OUTPUT_FILE_PATH, 'w') as output_file:
        json.dump(output_objects, output_file, indent=4)


read_file()
update_entries_with_points()
write_file()
