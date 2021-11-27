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
    def __init__(self, data=None):
        self.cells = []
        self.found = 0
        self.create_field()
        if data is not None:
            self.fill(data)

    def __eq__(self, other):
        return [each.value for each in self.cells] == [each.value for each in other.cells]

    def create_field(self):
        for row in range(1, 10):
            for column in range(1, 10):
                self.cells.append(
                    Cell(count=len(self.cells) + 1,
                         row=row, column=column,
                         square=int((row - 1) / 3) * 3 + int((column - 1) / 3) + 1))

    def fill(self, data):
        for i in range(81):
            self.cells[i].value = data[i]
        self.check_found()

    @staticmethod
    def print_values(values):
        for row in range(0, 9):
            for column in range(0, 9):
                value = values[row * 9 + column]
                print(str(value) if value else '*', end=' ')
                if column in [2, 5]:
                    print('|', end=' ')
                if column == 8:
                    print('')
                if column == 8 and row in [2, 5]:
                    print('------+-------+------')

    def print_field(self):
        self.print_values(self.get_all_values())

    def read_xlsx(self, filename):
        import openpyxl
        sheet = openpyxl.load_workbook(filename).active
        for each in self.cells:
            each.value = sheet.cell(row=each.row, column=each.column).value
        self.check_found()

    def get_all_values(self):
        return [each.value for each in self.cells]

    def get_row_cells(self, row):
        return [each for each in self.cells if each.row == row]

    def get_row_values(self, row):
        return [each.value for each in self.cells if each.row == row]

    def get_column_cells(self, column):
        return [each for each in self.cells if each.column == column]

    def get_column_values(self, column):
        return [each.value for each in self.cells if each.column == column]

    def get_square_cells(self, square):
        return [each for each in self.cells if each.square == square]

    def get_square_values(self, square):
        return [each.value for each in self.cells if each.square == square]

    def get_options(self):
        return [each.options for each in self.cells]

    def find_options1(self):
        for each in self.cells:
            if each.value is not None:
                each.options.append(each.value)
                continue
            each.options = [i for i in range(1, 10)]
            for i in range(1, 10):
                if i in self.get_row_values(each.row) or \
                        i in self.get_column_values(each.column) or \
                        i in self.get_square_values(each.square):
                    each.options.remove(i)

    def find_options2(self, value):
        result = []
        for each in self.cells:
            if each.value is not None or \
                    value in self.get_row_values(each.row) or \
                    value in self.get_column_values(each.column) or \
                    value in self.get_square_values(each.square):
                result.append(0)
            else:
                result.append(value)
        return Field(result)

    @staticmethod
    def check_answer_in_square(matrix, square):
        if matrix.get_square_values(square).count(0) != 8:
            return False
        for each in matrix.get_square_cells(square):
            if each.value != 0:
                return each.count

    @staticmethod
    def check_answer_in_row(matrix, row):
        if matrix.get_row_values(row).count(0) != 8:
            return False
        for each in matrix.get_row_cells(row):
            if each.value != 0:
                return each.count

    @staticmethod
    def check_answer_in_column(matrix, column):
        if matrix.get_column_values(column).count(0) != 8:
            return False
        for each in matrix.get_column_cells(column):
            if each.value != 0:
                return each.count

    def find_answer_in_square(self, matrix, value):
        for square_number in range(1, 10):
            answer_in_square = self.check_answer_in_square(matrix, square_number)
            if answer_in_square:
                self.cells[answer_in_square - 1].value = value

    def find_answer_in_row(self, matrix, value):
        for row in range(1, 10):
            answer_in_row = self.check_answer_in_row(matrix, row)
            if answer_in_row:
                self.cells[answer_in_row - 1].value = value

    def find_answer_in_column(self, matrix, value):
        for column in range(1, 10):
            answer_in_column = self.check_answer_in_column(matrix, column)
            if answer_in_column:
                self.cells[answer_in_column - 1].value = value

    def make_search(self):
        for value in range(1, 10):
            matrix = self.find_options2(value)
            self.find_answer_in_square(matrix, value)
            self.find_answer_in_row(matrix, value)
            self.find_answer_in_column(matrix, value)

    def find_answer(self):
        i = 0
        break_text = ''
        while self.found != 81:
            i += 1
            found_before = self.found
            self.make_search()
            self.check_found()
            if found_before == self.found:
                break_text = f'found {self.found} from 81\n'
                break
        self.print_field()
        print(f'{break_text}found with {i} steps')

    def check_found(self):
        self.found = sum([1 for each in self.cells if each.value is not None])


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
        cell = field.cells[0]
        self.assertEqual(1, cell.count)
        self.assertEqual(1, cell.row)
        self.assertEqual(1, cell.column)
        self.assertEqual(1, cell.square)
        self.assertEqual(None, cell.value)

        cell = field.cells[27]
        self.assertEqual(28, cell.count)
        self.assertEqual(4, cell.row)
        self.assertEqual(1, cell.column)
        self.assertEqual(4, cell.square)
        self.assertEqual(None, cell.value)

        cell = field.cells[80]
        self.assertEqual(81, cell.count)
        self.assertEqual(9, cell.row)
        self.assertEqual(9, cell.column)
        self.assertEqual(9, cell.square)
        self.assertEqual(None, cell.value)

    def test_read_xlsx_return_something(self):
        field = Field()
        field.read_xlsx(r'2021-11-23.xlsx')
        self.assertIsNotNone(field.get_all_values())

    def test_read_xlsx_return_81_numbers(self):
        field = Field()
        field.read_xlsx(r'2021-11-23.xlsx')
        self.assertEqual(81, len(field.get_all_values()))

    def test_read_xlsx_return_sample(self):
        field = Field()
        field.read_xlsx(r'2021-11-23.xlsx')
        self.assertEqual(self.sample_data.copy(), field.get_all_values())

    def test_get_row_values_return_something(self):
        field = Field(self.sample_data)
        self.assertIsNotNone(field.get_row_values(1))

    def test_get_row_values_return_9_numbers(self):
        field = Field(self.sample_data)
        self.assertEqual(9, len(field.get_row_values(1)))

    def test_get_row_values_return_part_of_sample(self):
        field = Field(self.sample_data)
        self.assertEqual(self.sample_data[0:9], field.get_row_values(1))
        self.assertEqual(self.sample_data[72:81], field.get_row_values(9))

    def test_get_column_values_return_something(self):
        field = Field(self.sample_data)
        self.assertIsNotNone(field.get_column_values(1))

    def test_get_column_values_return_9_numbers(self):
        field = Field(self.sample_data)
        self.assertEqual(9, len(field.get_column_values(1)))

    def test_get_column_values_return_part_of_sample(self):
        field = Field(self.sample_data)
        self.assertEqual(self.sample_data[0:81:9], field.get_column_values(1))
        self.assertEqual(self.sample_data[8:81:9], field.get_column_values(9))

    def test_get_square_values_return_something(self):
        field = Field(self.sample_data)
        self.assertIsNotNone(field.get_square_values(1))

    def test_get_square_values_return_9_numbers(self):
        field = Field(self.sample_data)
        self.assertEqual(9, len(field.get_square_values(1)))

    def test_get_square_values_return_part_of_sample(self):
        field = Field(self.sample_data)
        self.assertEqual(self.sample_data[0:3] + self.sample_data[9:12] + self.sample_data[18:21],
                         field.get_square_values(1))
        self.assertEqual(self.sample_data[60:63] + self.sample_data[69:72] + self.sample_data[78:81],
                         field.get_square_values(9))

    def test_find_options1(self):
        field = Field(self.sample_data)
        field.find_options1()
        self.assertEqual(
            [[2, 6, 9], [2, 7, 9], [2, 6, 7], [4, 5, 6, 7], [3, 4, 5, 6], [1], [3, 6, 7, 9], [8], [3, 4, 6, 7, 9], [5],
             [7, 9], [4], [6, 7, 8], [2], [6, 7, 8, 9], [3, 6, 7, 9], [1], [3, 6, 7, 9], [1, 6, 8, 9], [1, 7, 9], [3],
             [4, 6, 7, 8], [4, 6, 8], [4, 6, 7, 8, 9], [2], [5], [4, 6, 7, 9], [4], [5], [1, 2, 6], [9], [6, 8],
             [2, 6, 8], [1, 3, 6, 7], [3, 6, 7], [1, 3, 6, 7, 8], [7], [3], [6], [1], [6, 8], [5], [4], [2], [6, 8, 9],
             [1, 2, 6, 9], [8], [1, 2, 6], [3], [7], [2, 4, 6], [1, 5, 6, 9], [6, 9], [1, 6, 9], [1, 3], [1, 7],
             [1, 5, 7], [4, 5, 6, 7], [9], [4, 6, 7], [8], [3, 4, 6, 7], [2], [1, 2], [4], [8], [2, 5, 6, 7], [1, 5, 6],
             [3], [1, 6, 7, 9], [6, 7, 9], [1, 6, 7, 9], [1, 2, 3], [6], [9], [2, 4, 7, 8], [1, 4, 8], [2, 4, 7, 8],
             [1, 3, 7], [3, 4, 7], [5]], field.get_options())

    def test_find_options2(self):
        field = Field(self.sample_data)
        matrix1 = Field(
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 1,
             0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 1, 0, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 1, 0, 1,
             1, 0, 0, 0, 1, 0, 1, 0, 0])
        matrix2 = Field(
            [9, 9, 0, 0, 0, 0, 9, 0, 9, 0, 9, 0, 0, 0, 9, 9, 0, 9, 9, 9, 0, 0, 0, 9, 0, 0, 9, 0, 0, 0, 0, 0, 0, 0, 0, 0,
             0, 0, 0, 0, 0, 0, 0, 0, 9, 9, 0, 0, 0, 0, 0, 9, 9, 9, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 9, 9, 9,
             0, 0, 0, 0, 0, 0, 0, 0, 0])
        self.assertEqual(matrix1, field.find_options2(1))
        self.assertEqual(matrix2, field.find_options2(9))

    def test_check_answer_in_square(self):
        field = Field(
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
             0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
             0, 0, 0, 0, 0, 0, 0, 0, 0])
        self.assertFalse(Field().check_answer_in_square(field, 1))
        field = Field(
            [0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
             0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
             0, 0, 0, 0, 0, 0, 0, 0, 0])
        self.assertEqual(2, Field().check_answer_in_square(field, 1))

    def test_find_answer(self):
        field = Field(self.sample_data)
        field.find_answer()
        self.assertEqual(
            [6, 2, 7, 5, 3, 1, 9, 8, 4, 5, 9, 4, 8, 2, 7, 6, 1, 3, 8, 1, 3, 6, 4, 9, 2, 5, 7, 4, 5, 1, 9,
             6, 2, 3, 7, 8, 7, 3, 6, 1, 8, 5, 4, 2, 9, 9, 8, 2, 3, 7, 4, 5, 6, 1, 1, 7, 5, 4, 9, 6, 8, 3,
             2, 2, 4, 8, 7, 5, 3, 1, 9, 6, 3, 6, 9, 2, 1, 8, 7, 4, 5], field.get_all_values())

    def test_check_found(self):
        field = Field(self.sample_data)
        self.assertEqual(30, field.found)

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
