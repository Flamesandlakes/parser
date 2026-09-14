# Importing necessary libraries
import os 
import json

test_file_paths = ["data/employees.ascii.csv", "data/sogne.dawa.csv"]

class Parser():
    def __init__(self, input_file_path, output_file_path="outputs/placeholder.json", index_variable = None, ignore_placeholder=False):
        # input_file_path is the path to the input file (including file name and type)
        # output_file_path is the path where the resulting file will be saved (without file name)
        # index_variable is the index variable to be used for the JSON output. If None, unique numbers will be used.
        # ignore_placeholder is a boolean indicating whether to ignore the use of the placeholder output file path. 
            # If False, the user will be prompted to enter a output file path. If False, the placeholder path will just be used.

        self.input_file_path = input_file_path
        self.output_file_path = output_file_path
        self.index_variable = index_variable
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
            if self.index_variable is not None and self.index_variable not in headers:
                raise ValueError(f"Index variable '{self.index_variable}' not found in headers: {headers}")
            elif self.index_variable is not None:
                idx_variable_location = headers.index(self.index_variable) 

            # dict format /hashmap (for json)
            rows = [line for line in content.split('\n')[1:] if line]

            entries = {} # init dict til at holde entries
            
            for idx, row in enumerate(rows):
                values = {head: value for head, value in zip(headers, row.split(','))} # find værdierne for det givne index, opstillet som dict (inkl. eventuel index selv)
                if self.index_variable is None:
                    entries[idx] = values
                else:
                    entries[row.split(',')[idx_variable_location]] = values

        json_output = json.dumps(entries)

        with open(self.output_file_path, "w") as file:
            file.write(json_output)

            
if __name__ == "__main__": # sørger for at koden ikke executes når den blot importeres som modul
    parser = Parser("data/employees.ascii.csv", output_file_path="outputs/employees.json", ignore_placeholder=False)
    parser.parse_to_JSON()

