
test_file_paths = ["data/employees.ascii.csv", "data/sogne.dawa.csv"]

class Parser():
    seperator_placeholders = ["|", "//", "***", "[P]", "[PH]", "[_UNIQUE__PLACEHOLDER_]",
                              "gxOzlNQvKr","qkz08JWUIr","GC09mxT537","hsJzOlFHFu","QGwFStDLWH","xxemaNuMRL","a2GywH2k7E","KOomQhm0LO"]
    
    
    def __init__(self, input_file_path:str = None, output_file_path:str = None, assigned_headers:list = [], use_placeholder:bool=False):
        # input_file_path is the path to the input file (including file name and type)
        # output_file_path is the path where the resulting file will be saved (without file name)
        # assigned_headers is a list of strings to use for each column. Passing anything but None or an empty list makes this program assumes there is no header.
        # use_placeholder is a boolean indicating whether to ignore the use of the placeholder output file path. 
            # If False, the user will be prompted to enter a output file path. If False, the placeholder path will just be used.

        self.input_file_path = input_file_path
        self.output_file_path = output_file_path
        self.assigned_headers = assigned_headers
        self.ignore_placeholder = use_placeholder

    def load_file(self, input_file_path:str=None):
        # update the input_file_path if provided as an argument
        if input_file_path is not None:
            self.input_file_path = input_file_path

        if self.input_file_path is None:
            raise ValueError("Input file path is not set. Please provide a valid input file path.")  

        with open(self.input_file_path, "r", encoding = "utf-8") as file:
            content = file.read()
            self.file_content = content

    def text_to_array_of_dicts(self, content:str = None, assigned_headers = [], seperator = ",", quotation_marks = ["'", '"']):
        # NOTE: by passing a list to the assigned_headers argument, it is assumed that there is no existing header in the data itself
        
        if content is None:
            content = self.file_content
        
        if assigned_headers:
            self.assigned_headers = assigned_headers    

        if self.assigned_headers: # if assigned_headers, assign them
            headers = self.assigned_headers
            rows = [line for line in content.splitlines() if line] # and assume that all lines in the original text are entries/values (ie. non-headers)
        else: # otherwise assign the first row as the headers
            headers = [head.strip() for head in self._informed_seperation(content.splitlines()[0], seperator, quotation_marks)]
            rows = [line for line in content.splitlines()[1:] if line]

        entries = [] # init list til at holde entries
        
        for _, row in enumerate(rows):
            values = {head: value for head, value in zip(headers, self._informed_seperation(row, seperator, quotation_marks))} # find værdierne for det givne index, opstillet som dict
            entries.append(values)

    
        return entries

    def _content_seperator_marking(self, string:str, seperator:str, quotation_marks:list):#seperator = ",", quotation_marks = ["'", '"']):

        # def reverse_eval(string:str, do_reverse:bool):
        #     if do_reverse:
        #         return string[::-1]
        #     else:
        #         return string
        
        unique_placeholder = None
        for sp in Parser.seperator_placeholders:
            if sp not in string:
                unique_placeholder = sp
                break
        else:
            raise NotImplementedError("Error: All unique placeholders appear at least once within the input string.")

        #print(unique_placeholder)
        current_mark = None
        
        marked_string = ""
        quote_string =""
        
        for chr in string:
            if chr not in quotation_marks and chr != seperator: # eval the most common condition first
                if current_mark == None:
                    marked_string += chr
                    
                else:
                    quote_string += chr

            elif current_mark is None: # outside of quote
                if chr == seperator:
                    marked_string += unique_placeholder

                elif chr in quotation_marks: # beginning of quotation
                    current_mark = chr
                    quote_string += chr

                else: # pragma: no cover
                    print("Error; The condition for this print statement should never be met. #A") # error catcher

            else: # (chr in quotation_marks or chr == seperator) and current_mark != None, ie. inside quote
                if chr == seperator:
                    quote_string += unique_placeholder

                elif chr in quotation_marks:
                    if chr == current_mark: # end of quotation
                        current_mark = None
                        quote_string = quote_string.replace(unique_placeholder, seperator)
                        
                        marked_string += quote_string
                        quote_string = ""
                        marked_string += chr
                    else: # quotation mark but not for curren quote
                        quote_string += chr
                else:
                    quote_string += chr

        #print(marked_string)
        marked_string += quote_string
        return marked_string, unique_placeholder
            # ##
            # elif chr in quotation_marks:
            #     if current_mark == None:# and in_quote == False: # beginning of quotation
            #         current_mark = chr
                    
            #         quote_string += chr

            #     elif current_mark == chr:# and in_quote == True: # end of quotation
            #         current_mark = None
            #         quote_string = quote_string.replace(unique_placeholder, seperator)
                    
            #         marked_string += quote_string
            #         quote_string = ""
            #         marked_string += chr
            #     else: # other quotation mark inside existing quotation marks
            #         marked_string += chr

            # elif chr == seperator and current_mark is None:
            #     marked_string += unique_placeholder
                
            # elif : # seperator but inside a quote
            #     #marked_string += chr
            #     quote_string += unique_placeholder

        

    def _informed_seperation(self, string:str, seperator:str, quotation_marks:list) -> list: #seperator = ",", quotation_marks = ["'", '"']) -> list:

        marked_string, unique_placeholder = self._content_seperator_marking(string, seperator, quotation_marks)
        # marked_string_reversed, unique_placeholder_for_rev = self._content_seperator_marking(string[::-1], seperator, quotation_marks) 

        # if unique_placeholder != unique_placeholder_for_rev: # pragma: no cover
        #     raise NotImplementedError("Error: The mirrored versions of the generated placeholders does not match.")

        # if marked_string != marked_string_reversed[::-1]:
        #     for chr in 

        return marked_string.split(unique_placeholder)

    #def _
    
    def _stringify_entries(self, entries: list) -> str:
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

    def export(self, content, output_file_path = None): #pragma: no cover
        
        if output_file_path is not None:
            self.output_file_path = output_file_path
        
        with open(self.output_file_path, "w", encoding = "utf-8") as file:
            file.write(content)
                
    def parse_to_JSON(self):
        self.load_file()
        entries = self.text_to_array_of_dicts(self.file_content)
        entries_str = self._stringify_entries(entries)
        self.export(entries_str, self.output_file_path)

        
            
if __name__ == "__main__": # pragma: no cover # sørger for at koden ikke executes når den blot importeres som modul
    #parser = Parser("data/employees.ascii.csv", output_file_path="outputs/employees_2.json", use_placeholder=False)
    #parser.parse_to_JSON()
    # parser = Parser()
    # array = parser.text_to_array_of_dicts("Ol'MacDonald,human,production,38000,The Farmhouse", 
    #                                         ["navn", "art", "ansvarsområde", "løn", "opholdsområde"], quotation_marks= [""])
    parser = Parser()
    # unequal length across multiple entries (both too few, and too many values)
    array = parser.text_to_array_of_dicts("name,species,department,salary\nOl'MacDonald,human,production\nMervin,cat,security,treats and pets,the Barn")
    print(array)   

