import unittest


class Cell:
    def __init__(self, pos, row, column, square, value=None):
        self.i = pos - 1  # from 0 to 80
        self.pos = pos  # from 1 to 81
        self.row = row  # from 1 to 9
        self.column = column  # from 1 to 9
        self.square = square  # from 1 to 9
        self.value = value  # from 1 to 9
        self.options = []
        self.possible_options_row = set()
        self.possible_options_column = set()
        self.impossible_options = set()


class Field:
    def __init__(self, data=None):
        self.cells = []
        self.found = 0
        self.create_field()
        if data is not None:
            self.fill(data)

    def __eq__(self, other):
        return self.get_all_values() == other.get_all_values()

    def create_field(self):
        for row in range(1, 10):
            for column in range(1, 10):
                self.cells.append(
                    Cell(pos=len(self.cells) + 1,
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
                print(str(value) if value is not None else '.', end=' ')
                if column in [2, 5]:
                    print('|', end=' ')
                if column == 8:
                    print('')
                if column == 8 and row in [2, 5]:
                    print('------+-------+------')
        print('')

    def print_field(self):
        self.print_values(self.get_all_values())

    def read_xlsx(self, filename):
        print(f'load {filename}')
        import openpyxl
        sheet = openpyxl.load_workbook(filename).active
        for each in self.cells:
            each.value = sheet.cell(row=each.row, column=each.column).value
        self.check_found()
        self.print_field()
        print(f'{self.found} filled cells at the start\n')

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

    def get_possible_options_row(self):
        return [each.possible_options_row for each in self.cells]

    def get_possible_options_column(self):
        return [each.possible_options_column for each in self.cells]

    def get_impossible_options(self):
        return [each.impossible_options for each in self.cells]

    def find_options1(self):
        self.clear_options()
        for each in self.cells:
            if each.value is not None:
                each.options.append(each.value)
                continue
            each.options = [i for i in range(1, 10)]
            for i in range(1, 10):
                if i in self.get_row_values(each.row) or \
                        i in self.get_column_values(each.column) or \
                        i in self.get_square_values(each.square) or \
                        i in each.impossible_options:
                    each.options.remove(i)

    def get_matrix(self, value):
        matrix = Field(self.get_matrix_values(value))
        matrix.matrix_optimize()
        return matrix

    def get_matrix_values(self, value):
        result = []
        for each in self.cells:
            if each.value is not None:
                result.append(None)
            elif value in self.get_row_values(each.row) or \
                    value in self.get_column_values(each.column) or \
                    value in self.get_square_values(each.square):
                result.append(None)
            else:
                if len(each.possible_options_row) == 3 and value not in each.possible_options_row:
                    result.append(None)
                elif len(each.possible_options_column) == 3 and value not in each.possible_options_column:
                    result.append(None)
                elif value in each.impossible_options:
                    result.append(None)
                else:
                    result.append(value)
        return result

    def find_options3(self):
        self.clear_options()
        for value in range(1, 10):
            for matrix_cell in self.get_matrix(value).cells:
                if value in self.cells[matrix_cell.i].impossible_options:
                    continue
                if self.cells[matrix_cell.i].value:
                    self.cells[matrix_cell.i].options = [self.cells[matrix_cell.i].value]
                    continue
                if matrix_cell.value:
                    self.cells[matrix_cell.i].options.append(value)

    def clear_options(self):
        for cell in self.cells:
            cell.options = []

    def clear_possible_options(self):
        for cell in self.cells:
            cell.possible_options_row = set()
            cell.possible_options_column = set()

    @staticmethod
    def cell_with_value_pos(cells):
        return [each.pos for each in cells if each.value][0]

    @staticmethod
    def check_sum(values):
        return sum([1 for each in values if each]) != 1

    def check_answer_in_square(self, matrix, square):
        if self.check_sum(matrix.get_square_values(square)):
            return False
        return self.cell_with_value_pos(matrix.get_square_cells(square))

    def check_answer_in_row(self, matrix, row):
        if self.check_sum(matrix.get_row_values(row)):
            return False
        return self.cell_with_value_pos(matrix.get_row_cells(row))

    def check_answer_in_column(self, matrix, column):
        if self.check_sum(matrix.get_column_values(column)):
            return False
        return self.cell_with_value_pos(matrix.get_column_cells(column))

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
            self.only_possible_values()
            matrix = self.get_matrix(value)

            self.find_answer_in_square(matrix, value)
            self.find_answer_in_row(matrix, value)
            self.find_answer_in_column(matrix, value)

    def matrix_optimize_check_row(self, cells_with_value):
        if len(set([cell.row for cell in cells_with_value])) == 1:
            row = self.get_row_cells(cells_with_value[0].row)
            for cell in cells_with_value:
                row.remove(cell)
            for cell in row:
                cell.value = None

    def matrix_optimize_check_column(self, cells_with_value):
        if len(set([cell.column for cell in cells_with_value])) == 1:
            column = self.get_column_cells(cells_with_value[0].column)
            for cell in cells_with_value:
                column.remove(cell)
            for cell in column:
                cell.value = None

    def matrix_optimize(self):
        # if the value possible only in one row/column in square, then remove this value in other cells in row/column
        for square in range(1, 10):
            square_cells = self.get_square_cells(square)
            cells_with_value = [cell for cell in square_cells if cell.value]
            self.matrix_optimize_check_row(cells_with_value)
            self.matrix_optimize_check_column(cells_with_value)

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

    def self_check(self):
        for i in range(1, 10):
            for value in range(1, 10):
                if self.get_row_values(i).count(value) > 1 or \
                        self.get_column_values(i).count(value) > 1 or \
                        self.get_square_values(i).count(value) > 1:
                    return False
        return True

    def only_possible_values(self):
        self.clear_possible_options()
        for value in range(1, 10):
            matrix = self.get_matrix(value)
            for square_number in range(1, 10):
                square = matrix.get_square_cells(square_number)

                rows_in_square = [[square[0], square[1], square[2]],
                                  [square[3], square[4], square[5]],
                                  [square[6], square[7], square[8]]]
                modified_rows = []
                for row_in_square in rows_in_square:
                    modified_rows.append(sum([1 for each in row_in_square if each.value is not None]))
                if modified_rows[0] > 0 and modified_rows[1] == 0 and modified_rows[2] == 0:
                    self.fill_possible_impossible_values_row(matrix, square_number, rows_in_square, value, 0)
                elif modified_rows[0] == 0 and modified_rows[1] > 0 and modified_rows[2] == 0:
                    self.fill_possible_impossible_values_row(matrix, square_number, rows_in_square, value, 1)
                elif modified_rows[0] == 0 and modified_rows[1] == 0 and modified_rows[2] > 0:
                    self.fill_possible_impossible_values_row(matrix, square_number, rows_in_square, value, 2)

                columns_in_square = [[square[0], square[3], square[6]],
                                     [square[1], square[4], square[7]],
                                     [square[2], square[5], square[8]]]
                modified_columns = []
                for column_in_square in columns_in_square:
                    modified_columns.append(sum([1 for each in column_in_square if each.value is not None]))
                if modified_columns[0] > 0 and modified_columns[1] == 0 and modified_columns[2] == 0:
                    self.fill_possible_impossible_values_column(matrix, square_number, columns_in_square, value, 0)
                elif modified_columns[0] == 0 and modified_columns[1] > 0 and modified_columns[2] == 0:
                    self.fill_possible_impossible_values_column(matrix, square_number, columns_in_square, value, 1)
                elif modified_columns[0] == 0 and modified_columns[1] == 0 and modified_columns[2] > 0:
                    self.fill_possible_impossible_values_column(matrix, square_number, columns_in_square, value, 2)

    def fill_possible_impossible_values_row(self, matrix, square_number, rows, value, local_row):
        row_number = rows[local_row][0].row
        row_values = matrix.get_row_cells(row_number)
        all_values_in_same_square = sum([1 for each in row_values if
                                         (each.square == square_number or each.value is None)]) == 9
        if all_values_in_same_square:
            for matrix_cell in rows[local_row]:
                self.cells[matrix_cell.i].possible_options_row.add(value)
            for cell in self.get_square_cells(square_number):
                if cell.row != row_number:
                    cell.impossible_options.add(value)

    def fill_possible_impossible_values_column(self, matrix, square_number, columns, value, local_column):
        column_number = columns[local_column][0].column
        column_values = matrix.get_column_cells(column_number)
        all_values_in_same_square = sum([1 for each in column_values if
                                         (each.square == square_number or each.value is None)]) == 9
        if all_values_in_same_square:
            for matrix_cell in columns[local_column]:
                self.cells[matrix_cell.i].possible_options_column.add(value)
            for cell in self.get_square_cells(square_number):
                if cell.column != column_number:
                    cell.impossible_options.add(value)


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
        cell = Cell(pos=1, row=2, column=3, square=4, value=5)
        self.assertEqual(1, cell.pos)
        self.assertEqual(2, cell.row)
        self.assertEqual(3, cell.column)
        self.assertEqual(4, cell.square)
        self.assertEqual(5, cell.value)

    def test_field(self):
        field = Field()
        cell = field.cells[0]
        self.assertEqual(1, cell.pos)
        self.assertEqual(1, cell.row)
        self.assertEqual(1, cell.column)
        self.assertEqual(1, cell.square)
        self.assertEqual(None, cell.value)

        cell = field.cells[27]
        self.assertEqual(28, cell.pos)
        self.assertEqual(4, cell.row)
        self.assertEqual(1, cell.column)
        self.assertEqual(4, cell.square)
        self.assertEqual(None, cell.value)

        cell = field.cells[80]
        self.assertEqual(81, cell.pos)
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

    def test_get_matrix(self):
        field = Field(self.sample_data)
        matrix1 = Field(
            [None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None,
             1, 1, None, None, None, None, None, None, None, None, None, 1, None, None, None, 1, None, 1, None, None,
             None, None, None, None, None, None, None, 1, None, 1, None, None, None, 1, None, 1, 1, 1, 1, None, None,
             None, None, None, None, 1, None, None, None, 1, None, 1, None, 1, 1, None, None, None, 1, None, 1, None,
             None])
        matrix2 = Field(
            [None, 9, None, None, None, None, 9, None, None, None, 9, None, None, None, 9, 9, None, None, None, 9, None,
             None, None, 9, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None,
             None, None, None, None, None, 9, 9, None, None, None, None, None, None, None, None, None, None, None, None,
             None, None, None, None, None, None, None, None, None, None, None, 9, 9, None, None, None, None, None, None,
             None, None, None, None])
        self.assertEqual(matrix1, field.get_matrix(1))
        self.assertEqual(matrix2, field.get_matrix(9))

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

    def test_self_check(self):
        field = Field(self.sample_data)
        self.assertTrue(field.self_check())
        field.cells[0].value = 1
        self.assertFalse(field.self_check())

    def test_exper_level(self):
        field = Field()
        field.read_xlsx(r'expert.xlsx')
        field.find_answer()
        self.assertEqual(81, field.found)
        self.assertTrue(field.self_check())

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
