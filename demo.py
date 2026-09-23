from csvparser.main import Parser

texts = '''date,month,year,text\n
9,jan,2013,"I say 'Hello to you, sir'"\n
10,jan,2021,"oh hi, i didnt see your message before now"\n
'''

array = Parser().text_to_array_of_dicts(texts)

print(array)