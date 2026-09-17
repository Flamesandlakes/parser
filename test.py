import unittest
import coverage
import prototype


class TestParser(unittest.TestCase):
    def test_load_file(self):
        # simple case
        parser = prototype.Parser("data/test_data_001.csv")
        parser.load_file()
        self.assertEqual(parser.file_content, "x,y,z")

    def test_load_file_with_special_characters(self):
        # unique characters
        parser = prototype.Parser("data/test_data_002.csv")
        parser.load_file()
        self.assertEqual(parser.file_content, "region,område,præst,mødested")

    def test_load_file_with_no_file(self):
        # no file
        parser = prototype.Parser("data/DoesNotExist.csv")
        with self.assertRaises(FileNotFoundError):
            parser.load_file()

    def test_load_with_no_file_defined(self):
        # no file defined
        parser = prototype.Parser()
        with self.assertRaises(ValueError):
            parser.load_file()

    def test_load_with_text_file(self):
        # text file
        parser = prototype.Parser("data/test_data_003.txt")
        parser.load_file()
        self.assertEqual(parser.file_content, "lopus segnum le terra roma via ve e")

    def test_load_with_empty_file(self):
        # empty file
        parser = prototype.Parser("data/test_data_004.csv")
        parser.load_file()
        self.assertEqual(parser.file_content, "")

    def test_load_file_with_foreign_alphabets(self):
        parser = prototype.Parser("data/test_data_005.csv")
        parser.load_file()
        self.assertEqual(parser.file_content, "simpel kinesisk: 汉字, traditionel kinesisk: 漢字, japansk kanji: 漢字, koreansk hanja: 漢字, koreansk hangul: 한자, bulgarisk (pythonslange): питон, arabisk (pythonslange): بايثون")
    
    # test to 
    ## headerless csv

    
    def test_to_array_of_dicts(self):
        ## unequal length
        parser = prototype.Parser()
        array = parser.to_array_of_dicts("name,species,department,salary,office\nOl'MacDonald,human,production,38000,The Farmhouse")
        self.assertEqual(array, [{"name":"Ol'MacDonald", "species":"human", "department":"production","salary":'38000',"office":"The Farmhouse"}])

        ## unequal length across multiple entries (both too few, and too many values)
        array = parser.to_array_of_dicts("name,species,department,salary\nOl'MacDonald,human,production\nMervin,cat,security,treats and pets,the Barn")
        self.assertEqual(array, [{"name":"Ol'MacDonald", "species":"human", "department":"production"}, 
                                 {"name":"Mervin", "species":"cat", "department":"security", "salary":"treats and pets"}]) 

    # test stringify
    def test_stringify_entries(self):
        parser = prototype.Parser()
        self.assertEqual(parser.stringify_entries([{"a": 1, "b": 2}, {"a": 3, "b": 4}]), 
                         '[{"a": 1, "b": 2}, {"a": 3, "b": 4}]')

        # special characters + apostrophe
        self.assertEqual(parser.stringify_entries([{"slægt": "O'Malley"}]), 
                         '[{"slægt": "O\'Malley"}]')

        # nested dict
        self.assertEqual(parser.stringify_entries({"example": {'dictionary': 'British edition'}}), 
                         '["example": {"dictionary": "British edition"}]')

        # pseudo-nested dict
        self.assertEqual(parser.stringify_entries({"example": 'dictionary: British edition'}), 
                         '["example": "dictionary: British edition"]')
        # '[{"example": "dictionary: British edition"}]')



    # test parse method (eller måske ikke nødv hvis load og to_json er testet)

    ## 

    # test Parser class

if __name__ == "__main__":
    unittest.main()

    # parser = prototype.Parser()
    # array = parser.to_array_of_dicts("name,species,department,office\nOl'MacDonald,human,production\nMuffin,dog,support,treats,Yard,England")
    # print(array)
    #print([{"name":"Ol'MacDonald", "species":"human", "department":"production","salary":'38000',"office":"The Farmhouse"}])
