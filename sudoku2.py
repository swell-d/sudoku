import unittest


class Cell:
    def __init__(self, count, row, column, square, value=None):
        self.count = count  # from 1 to 81
        self.row = row  # from 1 to 9
        self.column = column  # from 1 to 9
        self.square = square  # from 1 to 9
        self.value = value  # from 1 to 9
        self.options = []


class Field:
    def __init__(self):
        self.field = []
        self.create_field()

    def create_field(self):
        for row in range(1, 10):
            for column in range(1, 10):
                self.field.append(
                    Cell(count=len(self.field) + 1,
                         row=row,
                         column=column,
                         square=int((row - 1) / 3) * 3 + int((column - 1) / 3) + 1))

    def return_values(self):
        result = []
        for each in self.field:
            result.append(each.value)
        return result

    def print_data_81(self):
        for each in self.field:
            print(each.value if each.value is not None else '*', end=' ')
            if each.column in [3, 6]:
                print('|', end=' ')
            if each.column == 9:
                print('')
            if each.column == 9 and each.row in [3, 6]:
                print('------+-------+------')

    def read_xlsx(self, filename):
        import openpyxl
        sheet = openpyxl.load_workbook(filename).active
        for each in self.field:
            each.value = sheet.cell(row=each.row, column=each.column).value


class FieldTests(unittest.TestCase):
    sample_data = [None, None, None, None, None, 1, None, 8, None,
                   5, None, 4, None, 2, None, None, 1, None,
                   None, None, 3, None, None, None, 2, 5, None,
                   4, 5, None, 9, None, None, None, None, None,
                   7, 3, None, 1, None, 5, 4, 2, None,
                   None, 8, None, 3, 7, None, None, None, None,
                   None, None, None, None, 9, None, 8, None, 2,
                   None, 4, 8, None, None, 3, None, None, None,
                   None, 6, 9, None, None, None, None, None, 5]

    def test_cell(self):
        cell = Cell(count=1, row=2, column=3, square=4, value=5)
        self.assertEqual(1, cell.count)
        self.assertEqual(2, cell.row)
        self.assertEqual(3, cell.column)
        self.assertEqual(4, cell.square)
        self.assertEqual(5, cell.value)

    def test_field(self):
        field = Field()
        cell = field.field[0]
        self.assertEqual(1, cell.count)
        self.assertEqual(1, cell.row)
        self.assertEqual(1, cell.column)
        self.assertEqual(1, cell.square)
        self.assertEqual(None, cell.value)

        cell = field.field[27]
        self.assertEqual(28, cell.count)
        self.assertEqual(4, cell.row)
        self.assertEqual(1, cell.column)
        self.assertEqual(4, cell.square)
        self.assertEqual(None, cell.value)

        cell = field.field[80]
        self.assertEqual(81, cell.count)
        self.assertEqual(9, cell.row)
        self.assertEqual(9, cell.column)
        self.assertEqual(9, cell.square)
        self.assertEqual(None, cell.value)

    def test_read_xlsx_return_something(self):
        field = Field()
        field.read_xlsx(r'2021-11-23.xlsx')
        self.assertIsNotNone(field.return_values())

    def test_read_xlsx_return_81_numbers(self):
        field = Field()
        field.read_xlsx(r'2021-11-23.xlsx')
        self.assertEqual(81, len(field.return_values()))

    def test_read_xlsx_return_sample(self):
        field = Field()
        field.read_xlsx(r'2021-11-23.xlsx')
        self.assertEqual(self.sample_data.copy(), field.return_values())


# 1  2  3  | 4  5  6  | 7  8  9
# 10 11 12 | 13 14 15 | 16 17 18
# 19 20 21 | 22 23 24 | 25 26 27
# ---------+----------+---------
# 28 29 30 | 31 32 33 | 34 35 36
# 37 38 39 | 40 41 42 | 43 44 45
# 46 47 48 | 49 50 51 | 52 53 54
# ---------+----------+---------
# 55 56 57 | 58 59 60 | 61 62 63
# 64 65 66 | 67 68 69 | 70 71 72
# 73 74 75 | 76 77 78 | 79 80 81
