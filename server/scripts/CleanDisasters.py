import csv
import json

def createJsonEntry(type, begin_date, end_date, fips, id):
    entry = {
        "disaster_type" : type,
        "begin_date" : begin_date,
        "end_date" : end_date,
        "fips_code" : fips,
        "id" : id,
    }
    return entry

output_objects = []

with open("../data/us_disaster_declarations.csv", "r") as file:
    reader = csv.reader(file)
    for line in reader:
        disaster_type = line[6]
        begin_date = line[12]
        end_date = line[13]
        fips = line[15]
        id = line[22]
        entry = createJsonEntry(disaster_type, begin_date, end_date, fips, id)
        output_objects.append(entry)

with open("../data/us_disasters_clean.json", 'w') as output_file:
    json.dump(output_objects, output_file, indent=4)
