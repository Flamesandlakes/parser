from csvparser.fileHandling import FileHandler
from csvparser.stringHandling import StringHandler
class Parser(FileHandler, StringHandler):
    seperator_placeholders = ["|", "//", "***", "[P]", "[PH]", "[_UNIQUE__PLACEHOLDER_]",
                              "gxOzlNQvKr","qkz08JWUIr","GC09mxT537","hsJzOlFHFu","QGwFStDLWH","xxemaNuMRL","a2GywH2k7E","KOomQhm0LO"]

    
    def __init__(self, input_file_path:str = None, 
                 output_file_path:str = None, 
                 added_headers:list = [] 
                 ):
        # input_file_path is the path to the input file (including file name and type)
        # output_file_path is the path where the resulting file will be saved (without file name)
        # added_headers is a list of strings to use for each column. Passing anything but None or an empty list makes this program assumes there is no header.
    

        self.input_file_path = input_file_path
        self.output_file_path = output_file_path
        self.added_headers = added_headers
  

    def text_to_array_of_dicts(self, content:str = None, added_headers = [], seperator = ",", quotation_marks = ["'", '"']):
        # content is the string that will be parsed and converted to an array of dictionaries.
        # added_headers is a list of strings that will be used as the keys in the dictionaries within the array.
        # NOTE: by passing a list to the added_headers argument, it is assumed that there is no existing header in the data itself
        # seperator 
        
        if content is None:
            content = self.file_content
        
        if added_headers:
            self.added_headers = added_headers    

        if self.added_headers: # if added_headers, assign them
            headers = self.added_headers
            rows = [line for line in content.splitlines() if line] # and assume that all lines in the original text are entries/values (ie. non-headers)
        else: # otherwise assign the first row as the headers
            headers = [head.strip() for head in self._informed_seperation(content.splitlines()[0], seperator, quotation_marks)]
            rows = [line for line in content.splitlines()[1:] if line]

        if not rows:
            rows = [",".join([str(None) for _ in headers])]

        entries = [] # init list til at holde entries
        
        for _, row in enumerate(rows):
            values = {head: value for head, value in zip(headers, self._informed_seperation(row, seperator, quotation_marks))} # find værdierne for det givne index, opstillet som dict
            entries.append(values)
    
        return entries

    def _content_seperator_marking(self, string:str, seperator:str, quotation_marks:list):
        # takes a string, embeds it with points of seperation, and return this marked string alongside the marker used to indicate points of seperation

        string = self._clean_string_as_csv(string, seperator)

        unique_placeholder = None
        for sp in Parser.seperator_placeholders: # check the local "library" of seperation markers, and choose the first to not occur in the original string itself
            if sp not in string:
                unique_placeholder = sp
                break
        else: # if all of them occur at least once, raise an error
            raise NotImplementedError("Error: All unique placeholders appear at least once within the input string.")


        # loop through the string
        # and keep track of quotation (and how that may affect the seperator)  
        current_mark = None
        
        marked_string = ""
        quote_string = ""
        
        for chr in string:
            if chr not in quotation_marks and chr != seperator: # eval the most common condition first
                if current_mark == None:
                    marked_string += chr
                    
                else:
                    quote_string += chr

            elif current_mark is None: # outside of quote
                if chr == seperator:
                    marked_string += unique_placeholder

                elif chr in quotation_marks: # beginning of quotation (criteria check)
                    #if last_chr == seperator or last_chr is None: # tillad kun quote hvis forrige karakter var en seperator /eller det er den første karakter
                    current_mark = chr
                    quote_string += chr
                    

                else: # pragma: cover
                    print("Error: The condition for this print statement should never be met. #A") # error catcher

            else: # (chr in quotation_marks or chr == seperator) and current_mark != None, ie. inside quote
                if chr == seperator:
                    quote_string += unique_placeholder

                elif chr in quotation_marks:
                    if chr == current_mark: # end of quotation
                        current_mark = None
                        quote_string = quote_string.replace(unique_placeholder, seperator)
                        #quote_string = quote_string.replace('"', '\"')
                        
                        marked_string += quote_string
                        quote_string = ""
                        marked_string += chr
                    else: # quotation mark but not for current quote
                        quote_string += chr
                else: # pragma: cover
                    print("Error: The condition for this print statement should never be met. #B") # error catcher
        
        marked_string += quote_string # if the quote was never closed, assume it wasnt a quote
        marked_string = marked_string.replace('"', '\"')

        return marked_string, unique_placeholder
        
    def _informed_seperation(self, string:str, seperator:str, quotation_marks:list) -> list: 
        # read a (marked) file alongside the seperation marker, then split the string on the marker, and return the resulting list

        marked_string, unique_placeholder = self._content_seperator_marking(string, seperator, quotation_marks) # take the marked string and the selected placeholder

        return marked_string.split(unique_placeholder) # and split the string on the placeholder used at the prior step

                
    def parse_to_JSON(self, input_file_path = None, output_file_path = None, added_headers = [], seperator = ",", quotation_marks = ["'", '"']):
        # take a file path, load the corresponding file, convert it to an array of dicts, export the array as a JSON file. 

        self.set_file_paths(input_file_path, output_file_path)

        self.load_file()
        entries = self.text_to_array_of_dicts(self.file_content, added_headers, seperator, quotation_marks)
        entries_str = self._stringify_entries(entries)
        self.export_string(entries_str)#NOTE: this method relies on the output path already saved in the object

        
            
if __name__ == "__main__": # pragma: cover # sørger for at koden ikke executes når den blot importeres som modul
    parser = Parser()
    array = parser.text_to_array_of_dicts('name,species,department,salary\nOl\'MacDonald,human,production\nMervin,cat,security,treats and pets,the Barn')
    print(array)
