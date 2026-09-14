# Importing necessary libraries
import os 
import json

test_file_paths = ["data/employees.ascii.csv", "data/sogne.dawa.csv"]

class Parser():
    def __init__(self, input_file_path, output_file_path="outputs/placeholder.json", group_by_headers=False, ignore_placeholder=False):
        # input_file_path is the path to the input file (including file name and type)
        # output_file_path is the path where the resulting file will be saved (without file name)
        # ignore_placeholder is a boolean indicating whether to ignore the use of the placeholder output file path. 
            # If False, the user will be prompted to enter a output file path. If False, the placeholder path will just be used.

        # Potential future features:
        # group_by_headers is a boolean indicating whether to group entries by their headers. A switch corresponds to transposing the data structure.
            # When False, the entries are indexed by row. When True, the entries are values for each header.
        
        self.input_file_path = input_file_path
        self.output_file_path = output_file_path
        self.group_by_headers = group_by_headers
        self.ignore_placeholder = ignore_placeholder

        if self.output_file_path == "outputs/placeholder":
                    self.output_file_path = input("Please enter the output file path (must end with .json): ")
                    if self.output_file_path.endswith(".json") == False:
                        print("Typo assumed, appending .json to the output file path.")
                        self.output_file_path += ".json"

    def parse_to_JSON(self):
        with open(self.input_file_path, "r") as file:
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

        json_output = json.dumps(entries)

        with open(self.output_file_path, "w") as file:
            file.write(json_output)

if __name__ == "__main__": # sørger for at koden ikke executes når den blot importeres som modul
    parser = Parser("data/employees.ascii.csv", output_file_path="outputs/employees.json", group_by_headers=False, ignore_placeholder=False)
    parser.parse_to_JSON()

