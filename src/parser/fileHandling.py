
class FileHandler():
    
    def __init__(self, input_file_path:str = None, 
                     output_file_path:str = None):
        
        self.input_file_path = input_file_path
        self.output_file_path = output_file_path
        
    def set_file_paths(self, input_file_path, output_file_path): # method to update the input file path if the input argument is valid
            # NOTE: Pass None to either argument to not update it.
            if input_file_path is not None:
                self.input_file_path = input_file_path
            
            if output_file_path is not None:
                 self.output_file_path = output_file_path

    def load_file(self, input_file_path:str=None):
        # update the input_file_path if provided as an argument
        
        self.set_file_paths(input_file_path, None)

        if self.input_file_path is None:
            raise ValueError("Input file path is not set. Please provide a valid input file path.")  

        with open(self.input_file_path, "r", encoding = "utf-8") as file:
            content = file.read()
            self.file_content = content
            
    def export_string(self, content:str, output_file_path:str = None): 
    
            self.set_file_paths(None, output_file_path)
            
            with open(self.output_file_path, "w", encoding = "utf-8") as file:
                file.write(content)