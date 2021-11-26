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

    def fill(self, data):
        for i in range(81):
            self.field[i].value = data[i]

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

    def return_values(self):
        result = []
        for each in self.field:
            result.append(each.value)
        return result

    def get_row_values(self, row):
        result = []
        for each in self.field:
            if each.row == row:
                result.append(each.value)
        return result

    def get_column_values(self, column):
        result = []
        for each in self.field:
            if each.column == column:
                result.append(each.value)
        return result

    def get_square_cells(self, square):
        result = []
        for each in self.field:
            if each.square == square:
                result.append(each)
        return result

    def get_square_values(self, square):
        result = []
        for each in self.field:
            if each.square == square:
                result.append(each.value)
        return result

    def find_options1(self):
        for each in self.field:
            if each.value is not None:
                each.options.append(each.value)
                continue
            each.options = [i for i in range(1, 10)]
            for i in range(1, 10):
                if i in self.get_row_values(each.row) or \
                        i in self.get_column_values(each.column) or \
                        i in self.get_square_values(each.square):
                    each.options.remove(i)

    def return_options(self):
        result = []
        for each in self.field:
            result.append(each.options)
        return result

    def find_options2(self, value):
        result = []
        for each in self.field:
            if each.value is not None or \
                    value in self.get_row_values(each.row) or \
                    value in self.get_column_values(each.column) or \
                    value in self.get_square_values(each.square):
                result.append(0)
            else:
                result.append(value)
        return result

    @staticmethod
    def check_answer_in_square(matrix_values, square):
        matrix = Field()
        matrix.fill(matrix_values)
        if matrix.get_square_values(square).count(0) != 8:
            return False
        for each in matrix.get_square_cells(square):
            if each.value != 0:
                return each.count


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

    def test_get_row_values_return_something(self):
        field = Field()
        field.fill(self.sample_data)
        self.assertIsNotNone(field.get_row_values(1))

    def test_get_row_values_return_9_numbers(self):
        field = Field()
        field.fill(self.sample_data)
        self.assertEqual(9, len(field.get_row_values(1)))

    def test_get_row_values_return_part_of_sample(self):
        field = Field()
        field.fill(self.sample_data)
        self.assertEqual(self.sample_data[0:9], field.get_row_values(1))
        self.assertEqual(self.sample_data[72:81], field.get_row_values(9))

    def test_get_column_values_return_something(self):
        field = Field()
        field.fill(self.sample_data)
        self.assertIsNotNone(field.get_column_values(1))

    def test_get_column_values_return_9_numbers(self):
        field = Field()
        field.fill(self.sample_data)
        self.assertEqual(9, len(field.get_column_values(1)))

    def test_get_column_values_return_part_of_sample(self):
        field = Field()
        field.fill(self.sample_data)
        self.assertEqual(self.sample_data[0:81:9], field.get_column_values(1))
        self.assertEqual(self.sample_data[8:81:9], field.get_column_values(9))

    def test_get_square_values_return_something(self):
        field = Field()
        field.fill(self.sample_data)
        self.assertIsNotNone(field.get_square_values(1))

    def test_get_square_values_return_9_numbers(self):
        field = Field()
        field.fill(self.sample_data)
        self.assertEqual(9, len(field.get_square_values(1)))

    def test_get_square_values_return_part_of_sample(self):
        field = Field()
        field.fill(self.sample_data)
        self.assertEqual(self.sample_data[0:3] + self.sample_data[9:12] + self.sample_data[18:21],
                         field.get_square_values(1))
        self.assertEqual(self.sample_data[60:63] + self.sample_data[69:72] + self.sample_data[78:81],
                         field.get_square_values(9))

    def test_find_options1(self):
        field = Field()
        field.fill(self.sample_data)
        field.find_options1()
        self.assertEqual(
            [[2, 6, 9], [2, 7, 9], [2, 6, 7], [4, 5, 6, 7], [3, 4, 5, 6], [1], [3, 6, 7, 9], [8], [3, 4, 6, 7, 9], [5],
             [7, 9], [4], [6, 7, 8], [2], [6, 7, 8, 9], [3, 6, 7, 9], [1], [3, 6, 7, 9], [1, 6, 8, 9], [1, 7, 9], [3],
             [4, 6, 7, 8], [4, 6, 8], [4, 6, 7, 8, 9], [2], [5], [4, 6, 7, 9], [4], [5], [1, 2, 6], [9], [6, 8],
             [2, 6, 8], [1, 3, 6, 7], [3, 6, 7], [1, 3, 6, 7, 8], [7], [3], [6], [1], [6, 8], [5], [4], [2], [6, 8, 9],
             [1, 2, 6, 9], [8], [1, 2, 6], [3], [7], [2, 4, 6], [1, 5, 6, 9], [6, 9], [1, 6, 9], [1, 3], [1, 7],
             [1, 5, 7], [4, 5, 6, 7], [9], [4, 6, 7], [8], [3, 4, 6, 7], [2], [1, 2], [4], [8], [2, 5, 6, 7], [1, 5, 6],
             [3], [1, 6, 7, 9], [6, 7, 9], [1, 6, 7, 9], [1, 2, 3], [6], [9], [2, 4, 7, 8], [1, 4, 8], [2, 4, 7, 8],
             [1, 3, 7], [3, 4, 7], [5]], field.return_options())

    def test_find_options2(self):
        field = Field()
        field.fill(self.sample_data)
        self.assertEqual(
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 1,
             0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 1, 0, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 1, 0, 1,
             1, 0, 0, 0, 1, 0, 1, 0, 0], field.find_options2(1))
        self.assertEqual(
            [9, 9, 0, 0, 0, 0, 9, 0, 9, 0, 9, 0, 0, 0, 9, 9, 0, 9, 9, 9, 0, 0, 0, 9, 0, 0, 9, 0, 0, 0, 0, 0, 0, 0, 0, 0,
             0, 0, 0, 0, 0, 0, 0, 0, 9, 9, 0, 0, 0, 0, 0, 9, 9, 9, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 9, 9, 9,
             0, 0, 0, 0, 0, 0, 0, 0, 0], field.find_options2(9))

    def test_check_answer_in_square(self):
        self.assertFalse(Field().check_answer_in_square(
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
             0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
             0, 0, 0, 0, 0, 0, 0, 0, 0], 1))
        self.assertEqual(2, Field().check_answer_in_square(
            [0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
             0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
             0, 0, 0, 0, 0, 0, 0, 0, 0], 1))


#   1   2	3
#   4   5	6
#   7	8	9

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
