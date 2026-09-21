# CSV String Parser

Python script for converting texts and files (adherring to a CSV dataformat) to an JSON array of objects (in Python: a list of dictionaries)  

## Description

All of the necessary functionality is tied to the Parser class as methods.
The Parser assumes that the input (be it a file or a text string) is in a CSV format (however other seperators besides commas can be used).
 
## Getting Started
If you want to directly convert a file to its corresponding JSON array (in the fewest possible steps) in Python:
* Import Parser class from prototype.py. Your "prototype.py"-file must also be stored in the same directory as your "stringHandling.py"-file. 
```
from prototype import Parser
```
* Initialize a Parser class oject
```
parser = Parser()
```
* Run the .parse_to_JSON method. 
** You must pass the following two arguments: The path to the input file (as a string), the path for the output JSON-file including its file name (as a string).
** Optionally, you may assign headers (assuming there is none in the file itself) by passing a list of strings. Not used by default.
** Optionally, you may define the character to be used to seperate on, by passing a string. Comma (",") is used by default.
** Optionally, you may define what characters are read as quotation marks. Single and double quotes (["'", '""]) by default.
```
parser.parse_to_JSON(<input file location>, <output file destination>)
```

### Dependencies

* Python 3.13.15

### Installing

* How/where to download your program
* Any modifications needed to be made to files/folders

### Executing program

* How to run the program
* Step-by-step bullets
```
code blocks for commands
```

## Help

Any advise for common problems or issues.
```
command to run if program contains helper info
```

## Version History
For now, refer to the commit history.

## License

This project is licensed under the [NAME HERE] License - see the LICENSE.md file for details
