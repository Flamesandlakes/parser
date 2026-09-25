# CSV String Parser

Python script for converting texts and files (adherring to a CSV-format) to an JSON array of objects [^1]  

## Description

All of the necessary functionality is tied to the Parser class as methods.
The Parser assumes that the input (be it a file or a text string) is in a CSV-format [^2].
 
## Getting Started

You must first import the Parser class and instantiate a Parser class object
- Import Parser class.  

```
from csvparser.main import Parser
```

- Initialize a Parser class oject

```
parserObj = Parser()
```

<p>
The parser object provides two primary methods for working with CSV-formatted text.<br>
    - <i>.text_to_array_of_dicts()</i><br>
    - <i>.parse_to_JSON()</i><br>
</p>

Parser<i>.text_to_array_of_dicts</i>: Parse a CSV-formatted string and convert it to an array of dictionaries (without exporting it).
* Run the .text_to_array_of_dicts method.
    - You must pass a string as the first argument.<br>
    - Optionally, you may add headers (under the assumption there is no existing line with headers in the file) by passing a list of strings. Not used by default.<br>
    - Optionally, you may define the character to be used to seperate on, by passing a string. Comma (",") is used by default.<br>
    - Optionally, you may define what characters are read as quotation marks. Single and double quotes (["'", '""]) are used by default.<br>

```
array = parserObj.text_to_array_of_dicts(<string in CSV-format>)
```


Parser<i>.parse_to_JSON</i>: If you want to directly convert a file to its corresponding JSON array (in the fewest possible steps) in Python:
* Run the .parse_to_JSON method. 
    - You must pass the following two arguments: The path to the input file (as a string), the path for the output JSON-file including its file name (as a string).
    - In addition, you have the same three optional arguments as for the .text_to_array_of_dicts method.
    
```
parserObj.parse_to_JSON(<input file location>, <output file destination>)
```
## Software overview

![Class UML for the Parser and its inheritance](https://github.com/Flamesandlakes/parser/blob/main/images/UML_Class_diagram_for_Parser_class.png)

The Parser class inherits methods pertaining to file handling and basic string operations.

### Dependencies

* Python 3.13.15
* Packages: 
    - coverage>=7.16.1

### Installing

* Download or clone this repository [^3].
* Place the csvparser subdirectory in your work environment of choice. 
* Your "main.py"-file must be stored in the same directory as your "fileHandling.py" and "stringHandling.py"-files, like they are in this directory by default [^4].
* 

[^1]: A list of dictionaries in Python.
[^2]: However other seperators besides commas can be used, as long as they are passed to the 'seperator' argument. The case of multiple different seperators within the same file and/or text is NOT supported. 
[^3]: It might be possible to install as a package in the future. However if so, expect this section to be updated accordingly.
[^4]: You may choose to disregard the tests subdirectory. However it may confirm whether everything runs as intended.


## Version History
For now, refer to the commit history.



