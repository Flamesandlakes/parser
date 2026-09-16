# Importing necessary libraries
import json

test_file_paths = ["data/employees.ascii.csv", "data/sogne.dawa.csv"]

class Parser():
    def __init__(self, input_file_path, output_file_path="outputs/placeholder.json", ignore_placeholder=False):
        # input_file_path is the path to the input file (including file name and type)
        # output_file_path is the path where the resulting file will be saved (without file name)
        # NOTE: DEPRECATED
            # index_variable is the index variable to be used for the JSON output. If None, unique numbers will be used.
        # ignore_placeholder is a boolean indicating whether to ignore the use of the placeholder output file path. 
            # If False, the user will be prompted to enter a output file path. If False, the placeholder path will just be used.

        self.input_file_path = input_file_path
        self.output_file_path = output_file_path
        #self.index_variable = index_variable
        self.ignore_placeholder = ignore_placeholder
        

        if self.output_file_path == "outputs/placeholder":
                    self.output_file_path = input("Please enter the output file path (must end with .json): ")
                    if self.output_file_path.endswith(".json") == False:
                        print("Typo assumed, appending .json to the output file path.")
                        self.output_file_path += ".json"

    def load_file(self):
        with open(self.input_file_path, "r") as file:
            content = file.read()
            self.file_content = content

    def to_JSON(self):
    
        headers = [head.strip() for head in self.file_content.split('\n')[0].split(',')]
        # # if self.index_variable is not None and self.index_variable not in headers:
        # #     raise ValueError(f"Index variable '{self.index_variable}' not found in headers: {headers}")
        # # elif self.index_variable is not None:
        # #     idx_variable_location = headers.index(self.index_variable) 

        rows = [line for line in self.file_content.split('\n')[1:] if line]

        # entries = {} # init dict til at holde entries #NOTE: DEPRECATED
        entries = [] # init list til at holde entries
        
        for idx, row in enumerate(rows):
            values = {head: value for head, value in zip(headers, row.split(','))} # find værdierne for det givne index, opstillet som dict (inkl. eventuel index selv)
            entries.append(values)

            # # NOTE: DEPRECATED CODE BELOW
            # # if self.index_variable is None:
            # #     entries[idx] = values
            # # else:
            # #     entries[row.split(',')[idx_variable_location]] = values

        entries_str = self.stringify_entries(entries)

        with open(self.output_file_path, "w") as file:
                    file.write(entries_str)
                    #file.write(str(entries).replace("'", '"'))

    def stringify_entries(self, entries):
        entries = str(entries).replace("'", '"')
        entries_str = ""
        for pc, cc, nc in zip(entries, entries[1:], entries[2:]):
            #print(f"pc: {pc}, cc: {cc}, nc: {nc}")
            if cc == '"' and pc != " " and pc != "[" and pc != "{" and (nc != " " and (nc != ":" and nc !=",") and nc != "]" and nc != "}") : # hvis en karakter følger og efterfølges af ikke-mellemrum eller særlige tegn, ændrer karakteren (antag at tegnet er inden i tekst)
                entries_str += "'"
            
            else:
                entries_str += cc

        entries_str = "["+entries_str+"]"
        return entries_str

    def parse_to_JSON(self):
        self.load_file()
        self.to_JSON()
        
            
if __name__ == "__main__": # sørger for at koden ikke executes når den blot importeres som modul
    parser = Parser("data/employees.ascii.csv", output_file_path="outputs/employees_2.json", ignore_placeholder=False)
    parser.parse_to_JSON()


