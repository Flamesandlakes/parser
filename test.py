import unittest
#import coverage
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
    

    

    # test to json
    ## headerless csv

    # test stringify
    def test_stringify_entries(self):
        parser = prototype.Parser()
        self.assertEqual(parser.stringify_entries([{"a": 1, "b": 2}, {"a": 3, "b": 4}]), 
                         '[{"a": 1, "b": 2}, {"a": 3, "b": 4}]')

        self.assertEqual(parser.stringify_entries([{"slægt": "O'Malley"}]), 
                         '[{"slægt": "O\'Malley"}]')

        self.assertEqual(parser.stringify_entries({"example": {'dictionary': 'British edition'}}), 
                         '["example": {"dictionary": "British edition"}]')

        # self.assertEqual(parser.stringify_entries({"example": 'dictionary: British edition'}), '[{"example": "dictionary: British edition"}]')



    # test parse method (eller måske ikke nødv hvis load og to_json er testet)

    ## 

    # test Parser class

if __name__ == "__main__":
    unittest.main()