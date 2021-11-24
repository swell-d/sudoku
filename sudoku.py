import unittest

import openpyxl as openpyxl


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
    return int(count / 27) * 3 + int((get_column(count) + 2) / 3)


def find_options(data):
    result = []
    for count, value in enumerate(data):
        if value is not None:
            result.append(value)
            continue
        options = [i for i in range(1, 10)]
        for i in range(1, 10):
            if i in get_row_values(data, get_row(count)) or i in get_column_values(data, get_column(count)) or i in get_square_values(data, get_square(count)):
                options.remove(i)
        result.append(options)
    print(result)
    return result



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

    def test_get_row_values_return_something(self):
        self.assertIsNotNone(get_row_values(self.sample_data, 1))

    def test_get_row_values_return_9_numbers(self):
        self.assertEqual(len(get_row_values(self.sample_data, 1)), 9)

    def test_get_row_values_return_part_of_sample(self):
        self.assertEqual(get_row_values(self.sample_data, 1), self.sample_data[0:9])
        self.assertEqual(get_row_values(self.sample_data, 2), self.sample_data[9:18])
        self.assertEqual(get_row_values(self.sample_data, 3), self.sample_data[18:27])
        self.assertEqual(get_row_values(self.sample_data, 4), self.sample_data[27:36])
        self.assertEqual(get_row_values(self.sample_data, 5), self.sample_data[36:45])
        self.assertEqual(get_row_values(self.sample_data, 6), self.sample_data[45:54])
        self.assertEqual(get_row_values(self.sample_data, 7), self.sample_data[54:63])
        self.assertEqual(get_row_values(self.sample_data, 8), self.sample_data[63:72])
        self.assertEqual(get_row_values(self.sample_data, 9), self.sample_data[72:81])

    def test_get_column_values_return_something(self):
        self.assertIsNotNone(get_column_values(self.sample_data, 1))

    def test_get_column_values_return_9_numbers(self):
        self.assertEqual(len(get_column_values(self.sample_data, 1)), 9)

    def test_get_column_values_return_part_of_sample(self):
        self.assertEqual(get_column_values(self.sample_data, 1), self.sample_data[0:81:9])
        self.assertEqual(get_column_values(self.sample_data, 2), self.sample_data[1:81:9])
        self.assertEqual(get_column_values(self.sample_data, 3), self.sample_data[2:81:9])
        self.assertEqual(get_column_values(self.sample_data, 4), self.sample_data[3:81:9])
        self.assertEqual(get_column_values(self.sample_data, 5), self.sample_data[4:81:9])
        self.assertEqual(get_column_values(self.sample_data, 6), self.sample_data[5:81:9])
        self.assertEqual(get_column_values(self.sample_data, 7), self.sample_data[6:81:9])
        self.assertEqual(get_column_values(self.sample_data, 8), self.sample_data[7:81:9])
        self.assertEqual(get_column_values(self.sample_data, 9), self.sample_data[8:81:9])

    def test_get_square_values_return_something(self):
        self.assertIsNotNone(get_square_values(self.sample_data, 1))

    def test_get_square_values_return_9_numbers(self):
        self.assertEqual(len(get_square_values(self.sample_data, 1)), 9)

    def test_get_square_values_return_part_of_sample(self):
        self.assertEqual(get_square_values(self.sample_data, 1),
                         self.sample_data[0:3] + self.sample_data[9:12] + self.sample_data[18:21])
        self.assertEqual(get_square_values(self.sample_data, 2),
                         self.sample_data[3:6] + self.sample_data[12:15] + self.sample_data[21:24])
        self.assertEqual(get_square_values(self.sample_data, 3),
                         self.sample_data[6:9] + self.sample_data[15:18] + self.sample_data[24:27])
        self.assertEqual(get_square_values(self.sample_data, 4),
                         self.sample_data[27:30] + self.sample_data[36:39] + self.sample_data[45:48])
        self.assertEqual(get_square_values(self.sample_data, 5),
                         self.sample_data[30:33] + self.sample_data[39:42] + self.sample_data[48:51])
        self.assertEqual(get_square_values(self.sample_data, 6),
                         self.sample_data[33:36] + self.sample_data[42:45] + self.sample_data[51:54])
        self.assertEqual(get_square_values(self.sample_data, 7),
                         self.sample_data[54:57] + self.sample_data[63:66] + self.sample_data[72:75])
        self.assertEqual(get_square_values(self.sample_data, 8),
                         self.sample_data[57:60] + self.sample_data[66:69] + self.sample_data[75:78])
        self.assertEqual(get_square_values(self.sample_data, 9),
                         self.sample_data[60:63] + self.sample_data[69:72] + self.sample_data[78:81])

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


    def test_find_options(self):
        self.assertIsNotNone(find_options(self.sample_data))


if __name__ == '__main__':
    unittest.main()

#   0   1	2	3	4	5	6	7	8
#   9   10	11	12	13	14	15	16	17
#   18	19	20	21	22	23	24	25	26
#   27	28	29	30	31	32	33	34	35
#   36	37	38	39	40	41	42	43	44
#   45	46	47	48	49	50	51	52	53
#   54	55	56	57	58	59	60	61	62
#   63	64	65	66	67	68	69	70	71
#   72	73	74	75	76	77	78	79	80
