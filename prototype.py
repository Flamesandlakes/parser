# Importing necessary libraries
import os 
import json

test_file_paths = ["data/employees.ascii.csv", "data/sogne.dawa.csv"]

with open("data/employees.ascii.csv", "r") as file:
    content = file.read()#.replace('\n', '')
    #print(content)
    headers = [head.strip() for head in content.split('\n')[0].split(',')]
    #print(headers)

    # dict format /hashmap (for json)
    idx_var = 0 # mulighed for at specificere en anden index variabel

    rows = [line for line in content.split('\n')[1:] if line]

    entries = {}
    for row in rows:
        idx = row.split(',')[idx_var] # sæt index 
        entries[idx] = {head: value for head, value in zip(headers, row.split(','))} # find værdierne for det givne index, opstillet som dict (inkl. index selv)
    print(entries)
