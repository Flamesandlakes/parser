import unittest
import coverage
import prototype


class TestParser(unittest.TestCase):
    def test_load_file(self):
        # simple case
        parser = prototype.Parser("data/test_data_001.csv")
        parser.load_file()
        self.assertEqual(parser.file_content, "x,y,z")

    def test_load_file_with_unique_characters(self):
        # unique characters
        parser = prototype.Parser("data/test_data_002.csv")
        parser.load_file()
        self.assertEqual(parser.file_content, "region,område,præst,mødested")

    def test_load_file_with_no_file(self):
        # no file
        parser = prototype.Parser("data/DoesNotExist.csv")
        with self.assertRaises(FileNotFoundError):
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

    # test to json

    # test stringify

    # test parse method

    # test Parser class

if __name__ == "__main__":
    unittest.main()