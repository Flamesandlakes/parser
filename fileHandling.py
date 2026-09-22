
class FileHandler():
    
    def __init__(self, input_file_path:str = None, 
                     output_file_path:str = None):
        
        self.input_file_path = input_file_path
        self.output_file_path = output_file_path
        
    def update_file_input(self, input_file_path): # method to update the input file path if the input argument is valid
            if input_file_path is not None:
                self.input_file_path = input_file_path
    
    def update_file_output(self, output_file_path): # method to update the output file path if the input argument is valid
            if output_file_path is not None:
                self.output_file_path = output_file_path


    def load_file(self, input_file_path:str=None):
        # update the input_file_path if provided as an argument
        
        self.update_file_input(input_file_path)

        if self.input_file_path is None:
            raise ValueError("Input file path is not set. Please provide a valid input file path.")  

        with open(self.input_file_path, "r", encoding = "utf-8") as file:
            content = file.read()
            self.file_content = content