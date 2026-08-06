import json
#text, written with JavaScript object notation. 
import os
#methods for interacting with the operating system

#synthea -> output -> fhir -> patient data
with os.scandir('synthea/output/fhir') as entries:
    for entry in entries:
        if entry.is_file():
            if "Information" in entry.name:
                continue  # skip this file, move to the next one in the loop
            with open(entry.path, 'r') as f:
                bundle = json.load(f)

entries_list = bundle['entry']
for item in entries_list:
    resource = item['resource']['resourceType']

print(resource)