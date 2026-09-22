import unittest
from unittest import mock # patch, call, mock_open
#import coverage
from prototype import Parser
from stringHandling import StringHandler


class TestParser(unittest.TestCase):
    def test_load_file_A(self):
        # simple case
        parser = Parser("data/test_data_001.csv")
        parser.load_file()
        self.assertEqual(parser.file_content, "x,y,z")

    def test_load_file_B(self):
        # unique characters
        parser = Parser("data/test_data_002.csv")
        parser.load_file()
        self.assertEqual(parser.file_content, "region,område,præst,mødested")

    def test_load_file_C(self):
        # no file
        parser = Parser("data/DoesNotExist.csv")
        with self.assertRaises(FileNotFoundError):
            parser.load_file()

    def test_load_file_D(self):
        # no file defined
        parser = Parser()
        with self.assertRaises(ValueError):
            parser.load_file()

    def test_load_file_E(self):
        # text file
        parser = Parser("data/test_data_003.txt")
        parser.load_file()
        self.assertEqual(parser.file_content, "lopus segnum le terra roma via ve e")

    def test_load_file_F(self):
        # empty file
        parser = Parser("data/test_data_004.csv")
        parser.load_file()
        self.assertEqual(parser.file_content, "")

    def test_load_file_G(self):
        # foreign characters
        parser = Parser("data/test_data_005.csv")
        parser.load_file()
        self.assertEqual(parser.file_content, "simpel kinesisk: 汉字, traditionel kinesisk: 漢字, japansk kanji: 漢字, koreansk hanja: 漢字, koreansk hangul: 한자, bulgarisk (pythonslange): питон, arabisk (pythonslange): بايثون")
    
    def test_load_file_H(self):
        # with defined path
        parser = Parser("data/test_data_001.csv")
        parser.load_file("data/test_data_002.csv")
        self.assertEqual(parser.input_file_path, "data/test_data_002.csv")
    
    # test advanced seperation
    def test_content_seperator(self):
        parser = Parser()
        test_string = "sender,msg\nMike,'Hey, let's get lunch or...'"
        self.assertEqual(parser._content_seperator_marking(test_string, ",", ["'", '"'])[0], "sender|msg\nMike|'Hey, let's get lunch or...'")

        # inactive quotation marks (ie. other mark inside quote of other marks)
        parser = Parser()
        test_string = "sender,msg\nMike,'Hejsa*, let's get lunch or... *Danish'"
        self.assertEqual(parser._content_seperator_marking(test_string, ",", ["'", '"', '*'])[0], "sender|msg\nMike|'Hejsa*, let's get lunch or... *Danish'")

        # string containing substrings otherwise used for marking
        test_string = "sender,msg\nBot,This|That // and [P]-values***"
        self.assertEqual(parser._content_seperator_marking(test_string, ",", ["'", '"'])[0], "sender[PH]msg\nBot[PH]This|That // and [P]-values***")

        test_string = '["|", "//", "***", "[P]", "[PH]", "[_UNIQUE__PLACEHOLDER_]", "gxOzlNQvKr","qkz08JWUIr","GC09mxT537","hsJzOlFHFu","QGwFStDLWH","xxemaNuMRL","a2GywH2k7E","KOomQhm0LO"] '
        with self.assertRaises(NotImplementedError):
            parser._content_seperator_marking(test_string, ",", ["'", '"'])

    def test_informed_seperator(self):
        parser = Parser()
        test_string = "sender,msg\nMike,'Hey, let's get lunch or...'"
        self.assertEqual(parser._informed_seperation(test_string, ",", ["'", '"']), ["sender","msg\nMike","'Hey, let's get lunch or...'"])

    
    # test text2array of dicts method
    def test_text_to_array_of_dicts_A(self):
        parser = Parser()
        # unequal length
        array = parser.text_to_array_of_dicts("name,species,department,salary,office\nOl'MacDonald,human,production,38000,The Farmhouse")
        self.assertEqual(array, [{"name":"Ol'MacDonald", "species":"human", "department":"production","salary":'38000',"office":"The Farmhouse"}])

    def test_text_to_array_of_dicts_B(self):
        parser = Parser()
        # unequal length across multiple entries (both too few, and too many values)
        array = parser.text_to_array_of_dicts("name,species,department,salary\nOl'MacDonald,human,production\nMervin,cat,security,treats and pets,the Barn")
        self.assertEqual(array, [{"name":"Ol'MacDonald", "species":"human", "department":"production"}, 
                                 {"name":"Mervin", "species":"cat", "department":"security", "salary":"treats and pets"}]) 

    def test_text_to_array_of_dicts_C(self):
        parser = Parser()
        # loading string from self.content (i.e. no arguments passed)
        parser = Parser()
        parser.load_file("data/test_data_055.csv")
        array = parser.text_to_array_of_dicts()
        self.assertEqual(array,
                         [{'name': "Ol'MacDonald", 'species': 'human', 'department': 'production', 'salary': '38000', 'office': 'The Farmhouse'},
                          {'name': 'Marwin', 'species': 'cat', 'department': 'security', 'salary': 'biscuits and pets', 'office': 'The Barn'},
                          {'name': 'Betty', 'species': 'cow', 'department': 'grass', 'salary': 'The Barn'},
                          {'name': 'Bob','species': 'bull', 'department': 'br (bovine resources)', 'salary': 'grass', 'office': 'The Barn'}])

    def test_text_to_array_of_dicts_D(self): 
        # using assigned_headers option
        parser = Parser()
        array = parser.text_to_array_of_dicts("Ol'MacDonald,human,production,38000,The Farmhouse", 
                                         ["navn", "art", "ansvarsområde", "løn", "opholdsområde"], quotation_marks= [""])
        self.assertEqual(array, [{"navn":"Ol'MacDonald", "art":"human", "ansvarsområde":"production","løn":'38000',"opholdsområde":"The Farmhouse"}])
        
    # test export
    def test_export_string(self):
        # path passed to method
        parser = Parser()
        with mock.patch("builtins.open") as mockery:
            parser.export_string("the very best string", "mockup.txt")
        mockery.assert_has_calls([mock.call("mockup.txt", "w", encoding="utf-8"),
                                  mock.call().__enter__(),
                                  mock.call().__enter__().write("the very best string"),
                                  mock.call().__exit__(None, None, None)])

        # path passed when initialising Parser obj
        parser = Parser("mock_source.txt", "mockup.txt")
        with mock.patch("builtins.open") as mockery:
            parser.export_string("the nearly best string")
        mockery.assert_has_calls([mock.call("mockup.txt", "w", encoding="utf-8"),
                                    mock.call().__enter__(),
                                    mock.call().__enter__().write("the nearly best string"),
                                    mock.call().__exit__(None, None, None)])
    

    # test parse method 
    def test_parse_to_JSON_A(self):
        parser = Parser("data/mock.csv", "mockup.json")
        with mock.patch("builtins.open") as mockery:
            parser.parse_to_JSON()
        mockery.assert_has_calls([
            mock.call('data/mock.csv', 'r', encoding = 'utf-8'),
            mock.call().__enter__(),
            mock.call().__enter__().read(),
            mock.call().__exit__(None, None, None),
            mock.call().__enter__().read().splitlines(),
            mock.call().__enter__().read().splitlines().__getitem__(0),
            mock.call().__enter__().read().splitlines().__getitem__().endswith(','),
            mock.call().__enter__().read().splitlines().__getitem__().endswith().__bool__(),
            mock.call().__enter__().read().splitlines().__getitem__().__contains__('|'),
            mock.call().__enter__().read().splitlines().__getitem__().__iter__(),
            mock.call().__enter__().read().splitlines(),
            mock.call().__enter__().read().splitlines().__getitem__(slice(1, None, None)),
            mock.call().__enter__().read().splitlines().__getitem__().__iter__(),
            mock.call("mockup.json", "w", encoding="utf-8"),
            mock.call().__enter__(),
            mock.call().__enter__().write('[{"": "None"}]'),
            mock.call().__exit__(None, None, None)
            ])

    def test_parse_to_JSON_B(self):
        parser = Parser("data/mock.csv", "mockup.json")
        with mock.patch("builtins.open") as mockery:
            parser.parse_to_JSON(None, "redirected_mockup.json")
        mockery.assert_has_calls([
            mock.call('data/mock.csv', 'r', encoding = 'utf-8'),
            mock.call().__enter__(),
            mock.call().__enter__().read(),
            mock.call().__exit__(None, None, None),
            mock.call().__enter__().read().splitlines(),
            mock.call().__enter__().read().splitlines().__getitem__(0),
            mock.call().__enter__().read().splitlines().__getitem__().endswith(','),
            mock.call().__enter__().read().splitlines().__getitem__().endswith().__bool__(),
            mock.call().__enter__().read().splitlines().__getitem__().__contains__('|'),
            mock.call().__enter__().read().splitlines().__getitem__().__iter__(),
            mock.call().__enter__().read().splitlines(),
            mock.call().__enter__().read().splitlines().__getitem__(slice(1, None, None)),
            mock.call().__enter__().read().splitlines().__getitem__().__iter__(),
            mock.call("redirected_mockup.json", "w", encoding="utf-8"),
            mock.call().__enter__(),
            mock.call().__enter__().write('[{"": "None"}]'),
            mock.call().__exit__(None, None, None)
            ])
    ## 
    # test stringify
    def test_stringify_entries(self):
        handler = StringHandler()
        self.assertEqual(handler._stringify_entries([{"a": 1, "b": 2}, {"a": 3, "b": 4}]), 
                            '[{"a": 1, "b": 2}, {"a": 3, "b": 4}]')

        # special characters + apostrophe
        self.assertEqual(handler._stringify_entries([{"slægt": "O'Malley"}]), 
                            '[{"slægt": "O\'Malley"}]')

        # nested dict
        self.assertEqual(handler._stringify_entries({"example": {'dictionary': 'British edition'}}), 
                            '["example": {"dictionary": "British edition"}]')

        # pseudo-nested dict
        self.assertEqual(handler._stringify_entries({"example": 'dictionary: British edition'}), 
                            '["example": "dictionary: British edition"]')


    def test_string_cleaner(self):
        handler = StringHandler()

        # multiple endings commas
        self.assertEqual(handler._clean_string_as_csv("a,b,c,,,", ","), "a,b,c")

        # only commas
        self.assertEqual(handler._clean_string_as_csv(",,,", ","), ",")




if __name__ == "__main__":
    unittest.main() # pragma: no cover
    # parser = Parser()
    # array = parser.to_array_of_dicts("Ol'MacDonald,human,production,38000,The Farmhouse", 
    #                                     ["navn", "art", "ansvarsområde", "løn", "opholdsområde"])
    # print(array)
