import unittest


def read_xlsx(file_path):
    return [None] * 9 * 9


class SudokuTests(unittest.TestCase):
    def test_read_xlsx_return_81_numbers(self):
        self.assertEqual(len(read_xlsx(None)), 81)


if __name__ == '__main__':
    unittest.main()
