import unittest

import openpyxl as openpyxl


def read_xlsx(filename):
    result = []
    sheet = openpyxl.load_workbook(filename).active
    for row in range(1, 10):
        for column in range(1, 10):
            result.append(sheet.cell(row=row, column=column).value)
    return result


def get_line(data, line):
    return data[9 * line - 9: 9 * line]


class SudokuTests(unittest.TestCase):
    sample_data = [None, None, None, None, None, 1, None, 8, None,
                   5, None, 4, None, 2, None, None, 1, None,
                   None, None, 3, None, None, None, 2, 5, None,
                   4, 5, None, 9, None, None, None, None, None,
                   7, 3, None, 1, None, 5, 4, 2, None,
                   None, 8, None, 3, 7, None, None, None, None,
                   None, None, None, None, 9, None, 8, None, 2,
                   None, 4, 8, None, None, 3, None, None, None,
                   None, 6, 9, None, None, None, None, None, 5]

    def test_read_xlsx_return_something(self):
        self.assertIsNotNone(read_xlsx(r'2021-11-23.xlsx'))

    def test_read_xlsx_return_81_numbers(self):
        self.assertEqual(len(read_xlsx(r'2021-11-23.xlsx')), 81)

    def test_read_xlsx_return_sample(self):
        self.assertEqual(read_xlsx(r'2021-11-23.xlsx'), self.sample_data)

    def test_get_line_return_something(self):
        self.assertIsNotNone(get_line(self.sample_data, 1))

    def test_get_line_return_9_numbers(self):
        self.assertEqual(len(get_line(self.sample_data, 1)), 9)

    def test_get_line_return_part_of_sample(self):
        self.assertEqual(get_line(self.sample_data, 1), self.sample_data[0:9])
        self.assertEqual(get_line(self.sample_data, 2), self.sample_data[9:18])
        self.assertEqual(get_line(self.sample_data, 3), self.sample_data[18:27])
        self.assertEqual(get_line(self.sample_data, 4), self.sample_data[27:36])
        self.assertEqual(get_line(self.sample_data, 5), self.sample_data[36:45])
        self.assertEqual(get_line(self.sample_data, 6), self.sample_data[45:54])
        self.assertEqual(get_line(self.sample_data, 7), self.sample_data[54:63])
        self.assertEqual(get_line(self.sample_data, 8), self.sample_data[63:72])
        self.assertEqual(get_line(self.sample_data, 9), self.sample_data[72:81])


if __name__ == '__main__':
    unittest.main()
