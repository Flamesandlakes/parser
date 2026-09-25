from csvparser.main import Parser

# Case with custom seperation character and custom quotation
texts_b = '''date+month+year+text\n
9+jan+2013+"I say *Hello to you, sir*"\n
10+jan+2021+"oh hi, i didnt see your message before now"\n
'''

array = Parser().text_to_array_of_dicts(texts_b, seperator="+", quotation_marks=["*"])

print(array)