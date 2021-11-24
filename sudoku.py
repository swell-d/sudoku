import unittest

import openpyxl as openpyxl


def print_data_9(data):
    result = ''
    for i in range(0, 3):
        for j in range(0, 3):
            result += str(data[i * 3 + j]) + ' '
        result += '\n'
    print(result)


def print_data_81(data):
    result = ''
    for i in range(0, 9):
        for j in range(0, 9):
            result += str(data[i * 9 + j]) + ' '
            if j in [2, 5]:
                result += '| '
        result += '\n'
        if i in [2, 5]:
            result += '------+-------+------\n'
    result += '\n'
    print(result)


def read_xlsx(filename):
    result = []
    sheet = openpyxl.load_workbook(filename).active
    for row in range(1, 10):
        for column in range(1, 10):
            result.append(sheet.cell(row=row, column=column).value)
    return result


def get_row_values(data, row):
    return data[9 * row - 9: 9 * row]


def get_column_values(data, column):
    return data[column - 1: 81: 9]


def get_square_values(data, square):
    #   1   2	3
    #   4   5	6
    #   7	8	9
    factor = (square + 2) % 3
    add = 3 * factor
    if square in [4, 5, 6]:
        add += 27
    elif square in [7, 8, 9]:
        add += 54
    return data[add + 0: add + 3] + data[add + 9: add + 12] + data[add + 18: add + 21]


def get_row(count):
    return int(count / 9) + 1


def get_column(count):
    return count % 9 + 1


def get_square(count):
    #   1   2	3
    #   4   5	6
    #   7	8	9
    return int(count / 27) * 3 + int((get_column(count) + 2) / 3)


def find_options1(data):
    result = []
    for count, value in enumerate(data):
        if value is not None:
            result.append(value)
            continue
        options = [i for i in range(1, 10)]
        for i in range(1, 10):
            if i in get_row_values(data, get_row(count)) or \
                    i in get_column_values(data, get_column(count)) or \
                    i in get_square_values(data, get_square(count)):
                options.remove(i)
        result.append(options)
    return result


def find_options2(data):
    result = []
    for i in range(1, 10):
        options = []
        for count, value in enumerate(data):
            if value is not None or \
                    i in get_row_values(data, get_row(count)) or \
                    i in get_column_values(data, get_column(count)) or \
                    i in get_square_values(data, get_square(count)):
                options.append(0)
            else:
                options.append(i)
        result.append(options)
    return result


def check_answer_in_square(square):
    if square.count(0) == 8:
        for i in range(0, 9):
            if square[i] != 0:
                return i + 1
    return False


def return_count_from_square(square, i):
    add = 0
    if square in [4, 5, 6]:
        add += 27
    elif square in [7, 8, 9]:
        add += 54
    return add + (square + 2) % 3 * 3 + int((i - 1) / 3) * 9 + (i - 1) % 3


def find_answer(data):
    for i, matrix in enumerate(find_options2(data)):
        for square_number in range(1, 10):
            square = get_square_values(matrix, square_number)
            answer_in_square = check_answer_in_square(square)
            if answer_in_square:
                count = return_count_from_square(square_number, answer_in_square)
                data[count] = i + 1
    return data


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
        self.assertEqual(read_xlsx(r'2021-11-23.xlsx'), self.sample_data.copy())

    def test_get_row_values_return_something(self):
        self.assertIsNotNone(get_row_values(self.sample_data.copy(), 1))

    def test_get_row_values_return_9_numbers(self):
        self.assertEqual(len(get_row_values(self.sample_data.copy(), 1)), 9)

    def test_get_row_values_return_part_of_sample(self):
        self.assertEqual(get_row_values(self.sample_data.copy(), 1), self.sample_data.copy()[0:9])
        self.assertEqual(get_row_values(self.sample_data.copy(), 2), self.sample_data.copy()[9:18])
        self.assertEqual(get_row_values(self.sample_data.copy(), 3), self.sample_data.copy()[18:27])
        self.assertEqual(get_row_values(self.sample_data.copy(), 4), self.sample_data.copy()[27:36])
        self.assertEqual(get_row_values(self.sample_data.copy(), 5), self.sample_data.copy()[36:45])
        self.assertEqual(get_row_values(self.sample_data.copy(), 6), self.sample_data.copy()[45:54])
        self.assertEqual(get_row_values(self.sample_data.copy(), 7), self.sample_data.copy()[54:63])
        self.assertEqual(get_row_values(self.sample_data.copy(), 8), self.sample_data.copy()[63:72])
        self.assertEqual(get_row_values(self.sample_data.copy(), 9), self.sample_data.copy()[72:81])

    def test_get_column_values_return_something(self):
        self.assertIsNotNone(get_column_values(self.sample_data.copy(), 1))

    def test_get_column_values_return_9_numbers(self):
        self.assertEqual(len(get_column_values(self.sample_data.copy(), 1)), 9)

    def test_get_column_values_return_part_of_sample(self):
        self.assertEqual(get_column_values(self.sample_data.copy(), 1), self.sample_data.copy()[0:81:9])
        self.assertEqual(get_column_values(self.sample_data.copy(), 2), self.sample_data.copy()[1:81:9])
        self.assertEqual(get_column_values(self.sample_data.copy(), 3), self.sample_data.copy()[2:81:9])
        self.assertEqual(get_column_values(self.sample_data.copy(), 4), self.sample_data.copy()[3:81:9])
        self.assertEqual(get_column_values(self.sample_data.copy(), 5), self.sample_data.copy()[4:81:9])
        self.assertEqual(get_column_values(self.sample_data.copy(), 6), self.sample_data.copy()[5:81:9])
        self.assertEqual(get_column_values(self.sample_data.copy(), 7), self.sample_data.copy()[6:81:9])
        self.assertEqual(get_column_values(self.sample_data.copy(), 8), self.sample_data.copy()[7:81:9])
        self.assertEqual(get_column_values(self.sample_data.copy(), 9), self.sample_data.copy()[8:81:9])

    def test_get_square_values_return_something(self):
        self.assertIsNotNone(get_square_values(self.sample_data.copy(), 1))

    def test_get_square_values_return_9_numbers(self):
        self.assertEqual(len(get_square_values(self.sample_data.copy(), 1)), 9)

    def test_get_square_values_return_part_of_sample(self):
        self.assertEqual(get_square_values(self.sample_data.copy(), 1),
                         self.sample_data.copy()[0:3] + self.sample_data.copy()[9:12] + self.sample_data.copy()[18:21])
        self.assertEqual(get_square_values(self.sample_data.copy(), 2),
                         self.sample_data.copy()[3:6] + self.sample_data.copy()[12:15] + self.sample_data.copy()[21:24])
        self.assertEqual(get_square_values(self.sample_data.copy(), 3),
                         self.sample_data.copy()[6:9] + self.sample_data.copy()[15:18] + self.sample_data.copy()[24:27])
        self.assertEqual(get_square_values(self.sample_data.copy(), 4),
                         self.sample_data.copy()[27:30] + self.sample_data.copy()[36:39] + self.sample_data.copy()[
                                                                                           45:48])
        self.assertEqual(get_square_values(self.sample_data.copy(), 5),
                         self.sample_data.copy()[30:33] + self.sample_data.copy()[39:42] + self.sample_data.copy()[
                                                                                           48:51])
        self.assertEqual(get_square_values(self.sample_data.copy(), 6),
                         self.sample_data.copy()[33:36] + self.sample_data.copy()[42:45] + self.sample_data.copy()[
                                                                                           51:54])
        self.assertEqual(get_square_values(self.sample_data.copy(), 7),
                         self.sample_data.copy()[54:57] + self.sample_data.copy()[63:66] + self.sample_data.copy()[
                                                                                           72:75])
        self.assertEqual(get_square_values(self.sample_data.copy(), 8),
                         self.sample_data.copy()[57:60] + self.sample_data.copy()[66:69] + self.sample_data.copy()[
                                                                                           75:78])
        self.assertEqual(get_square_values(self.sample_data.copy(), 9),
                         self.sample_data.copy()[60:63] + self.sample_data.copy()[69:72] + self.sample_data.copy()[
                                                                                           78:81])

    def test_get_row(self):
        self.assertEqual(get_row(0), 1)
        self.assertEqual(get_row(8), 1)
        self.assertEqual(get_row(9), 2)
        self.assertEqual(get_row(17), 2)
        self.assertEqual(get_row(18), 3)
        self.assertEqual(get_row(80), 9)

    def test_get_column(self):
        self.assertEqual(get_column(0), 1)
        self.assertEqual(get_column(1), 2)
        self.assertEqual(get_column(7), 8)
        self.assertEqual(get_column(8), 9)
        self.assertEqual(get_column(9), 1)
        self.assertEqual(get_column(17), 9)
        self.assertEqual(get_column(18), 1)
        self.assertEqual(get_column(80), 9)

    def test_get_square(self):
        self.assertEqual(get_square(0), 1)
        self.assertEqual(get_square(1), 1)
        self.assertEqual(get_square(2), 1)
        self.assertEqual(get_square(9), 1)
        self.assertEqual(get_square(10), 1)
        self.assertEqual(get_square(11), 1)
        self.assertEqual(get_square(18), 1)
        self.assertEqual(get_square(19), 1)
        self.assertEqual(get_square(20), 1)
        self.assertEqual(get_square(30), 5)
        self.assertEqual(get_square(40), 5)
        self.assertEqual(get_square(50), 5)
        self.assertEqual(get_square(60), 9)
        self.assertEqual(get_square(70), 9)
        self.assertEqual(get_square(80), 9)

    def test_find_options1(self):
        self.assertEqual(find_options1(self.sample_data.copy()),
                         [[2, 6, 9], [2, 7, 9], [2, 6, 7], [4, 5, 6, 7], [3, 4, 5, 6], 1, [3, 6, 7, 9], 8,
                          [3, 4, 6, 7, 9], 5, [7, 9], 4, [6, 7, 8], 2, [6, 7, 8, 9], [3, 6, 7, 9], 1, [3, 6, 7, 9],
                          [1, 6, 8, 9], [1, 7, 9], 3, [4, 6, 7, 8], [4, 6, 8], [4, 6, 7, 8, 9], 2, 5, [4, 6, 7, 9], 4,
                          5, [1, 2, 6], 9, [6, 8], [2, 6, 8], [1, 3, 6, 7], [3, 6, 7], [1, 3, 6, 7, 8], 7, 3, [6], 1,
                          [6, 8], 5, 4, 2, [6, 8, 9], [1, 2, 6, 9], 8, [1, 2, 6], 3, 7, [2, 4, 6], [1, 5, 6, 9], [6, 9],
                          [1, 6, 9], [1, 3], [1, 7], [1, 5, 7], [4, 5, 6, 7], 9, [4, 6, 7], 8, [3, 4, 6, 7], 2, [1, 2],
                          4, 8, [2, 5, 6, 7], [1, 5, 6], 3, [1, 6, 7, 9], [6, 7, 9], [1, 6, 7, 9], [1, 2, 3], 6, 9,
                          [2, 4, 7, 8], [1, 4, 8], [2, 4, 7, 8], [1, 3, 7], [3, 4, 7], 5])

    def test_find_options2(self):
        self.assertEqual(find_options2(self.sample_data.copy()),
                         [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1,
                           0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0,
                           0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 1, 0, 1, 1, 1, 1, 0, 0, 0,
                           0, 0, 0, 1, 0, 0, 0, 1, 0, 1, 0, 1, 1, 0, 0, 0, 1, 0, 1, 0,
                           0], [
                              2, 2, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                              0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 2, 0, 0, 0, 0, 0,
                              0, 0, 0, 0, 0, 0, 0, 2, 0, 2, 0, 0, 2, 0, 0, 0, 0, 0, 0,
                              0, 0, 0, 0, 0, 0, 2, 0, 0, 2, 0, 0, 0, 0, 0, 2, 0, 0, 2,
                              0, 2, 0, 0, 0], [
                              0, 0, 0, 0, 3, 0, 3, 0, 3, 0, 0, 0, 0, 0, 0, 3, 0, 3, 0,
                              0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3, 3, 3, 0, 0,
                              0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3, 0, 0,
                              0, 0, 0, 0, 3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3, 0, 0, 0,
                              0, 0, 3, 3, 0], [
                              0, 0, 0, 4, 4, 0, 0, 0, 4, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                              0, 0, 4, 4, 4, 0, 0, 4, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                              0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 4, 0, 0, 0, 0, 0, 0,
                              4, 0, 4, 0, 4, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 4,
                              4, 4, 0, 4, 0], [
                              0, 0, 0, 5, 5, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                              0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                              0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 5, 0, 0, 0, 0, 5,
                              5, 0, 0, 0, 0, 0, 0, 0, 0, 5, 5, 0, 0, 0, 0, 0, 0, 0, 0,
                              0, 0, 0, 0, 0], [
                              6, 0, 6, 6, 6, 0, 6, 0, 6, 0, 0, 0, 6, 0, 6, 6, 0, 6, 6,
                              0, 0, 6, 6, 6, 0, 0, 6, 0, 0, 6, 0, 6, 6, 6, 6, 6, 0, 0,
                              6, 0, 6, 0, 0, 0, 6, 6, 0, 6, 0, 0, 6, 6, 6, 6, 0, 0, 0,
                              6, 0, 6, 0, 6, 0, 0, 0, 0, 6, 6, 0, 6, 6, 6, 0, 0, 0, 0,
                              0, 0, 0, 0, 0], [
                              0, 7, 7, 7, 0, 0, 7, 0, 7, 0, 7, 0, 7, 0, 7, 7, 0, 7, 0,
                              7, 0, 7, 0, 7, 0, 0, 7, 0, 0, 0, 0, 0, 0, 7, 7, 7, 0, 0,
                              0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 7, 7,
                              7, 0, 7, 0, 7, 0, 0, 0, 0, 7, 0, 0, 7, 7, 7, 0, 0, 0, 7,
                              0, 7, 7, 7, 0], [
                              0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 8, 0, 8, 0, 0, 0, 8,
                              0, 0, 8, 8, 8, 0, 0, 0, 0, 0, 0, 0, 8, 8, 0, 0, 8, 0, 0,
                              0, 0, 8, 0, 0, 0, 8, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                              0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 8,
                              8, 8, 0, 0, 0], [
                              9, 9, 0, 0, 0, 0, 9, 0, 9, 0, 9, 0, 0, 0, 9, 9, 0, 9, 9,
                              9, 0, 0, 0, 9, 0, 0, 9, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                              0, 0, 0, 0, 0, 0, 9, 9, 0, 0, 0, 0, 0, 9, 9, 9, 0, 0, 0,
                              0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 9, 9, 9, 0, 0, 0, 0,
                              0, 0, 0, 0, 0]])

    def test_check_answer_in_square(self):
        self.assertFalse(check_answer_in_square([0, 0, 0, 0, 0, 0, 0, 0, 0]))
        self.assertEqual(check_answer_in_square([0, 5, 0, 0, 0, 0, 0, 0, 0]), 2)
        self.assertEqual(check_answer_in_square([0, 0, 0, 0, 0, 0, 0, 0, 9]), 9)

    def test_return_count_from_square(self):
        self.assertEqual(return_count_from_square(1, 1), 0)
        self.assertEqual(return_count_from_square(1, 2), 1)
        self.assertEqual(return_count_from_square(2, 2), 4)
        self.assertEqual(return_count_from_square(5, 5), 40)
        self.assertEqual(return_count_from_square(7, 7), 72)
        self.assertEqual(return_count_from_square(9, 9), 80)

    def test_find_answer(self):
        new_data = find_answer(self.sample_data.copy())
        for _ in range(12):
            new_data = find_answer(new_data)
        self.assertEqual(new_data,
                         [6, 2, 7, 5, 3, 1, 9, 8, 4, 5, 9, 4, 8, 2, 7, 6, 1, 3, 8, 1, 3, 6, 4, 9, 2, 5, 7, 4, 5, 1, 9,
                          6, 2, 3, 7, 8, 7, 3, 6, 1, 8, 5, 4, 2, 9, 9, 8, 2, 3, 7, 4, 5, 6, 1, 1, 7, 5, 4, 9, 6, 8, 3,
                          2, 2, 4, 8, 7, 5, 3, 1, 9, 6, 3, 6, 9, 2, 1, 8, 7, 4, 5])

#   0   1	2	3	4	5	6	7	8
#   9   10	11	12	13	14	15	16	17
#   18	19	20	21	22	23	24	25	26
#   27	28	29	30	31	32	33	34	35
#   36	37	38	39	40	41	42	43	44
#   45	46	47	48	49	50	51	52	53
#   54	55	56	57	58	59	60	61	62
#   63	64	65	66	67	68	69	70	71
#   72	73	74	75	76	77	78	79	80
