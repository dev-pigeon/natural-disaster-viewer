import csv
import json
import os

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


def createJsonEntry(type, begin_date, end_date, fips, id):
    entry = {
        "disaster_type" : type,
        "begin_date" : begin_date,
        "end_date" : end_date,
        "fips_code" : fips,
        "id" : id,
    }
    return entry


def updateDictionary(dict, key, value):
    prev_list = dict.get(key)
    if prev_list is not None:
        prev_list.append(value)
    else:
        dict[key] = [value]


def readFile():
    with open(INPUT_FILE_PATH, "r") as file:
        reader = csv.reader(file)
        for index, line in enumerate(reader):
            disaster_type = line[6]
            begin_date = line[12]
            end_date = line[13]
            fips = line[15]
            id = line[22]
            entry = createJsonEntry(disaster_type, begin_date, end_date, fips, id)
            updateDictionary(fips_index_dict, key=fips, value=index)
            output_objects.append(entry)


def writeFile():
    with open(OUTPUT_FILE_PATH, 'w') as output_file:
        json.dump(output_objects, output_file, indent=4)


readFile()
writeFile()