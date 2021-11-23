import unittest

import openpyxl as openpyxl


def read_xlsx(filename):
    if filename is None:
        return [None] * 9 * 9
    sheet = openpyxl.load_workbook(filename).active
    return sheet


class SudokuTests(unittest.TestCase):
    def test_read_xlsx_return_81_numbers(self):
        self.assertEqual(len(read_xlsx(None)), 81)

    def test_read_xlsx_read_file(self):
        self.assertIsNotNone(read_xlsx(r'2021-11-23.xlsx'))


if __name__ == '__main__':
    unittest.main()
