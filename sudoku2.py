import unittest


class Cell:
    def __init__(self, count, row_number, column_number, square):
        self.count = count  # from 1 to 81
        self.row_number = row_number  # from 1 to 9
        self.column_number = column_number  # from 1 to 9
        self.square = square  # from 1 to 9
        self.value = None  # from 1 to 9
        self.options = []


class Field:
    def __init__(self):
        self.field = []

    def create_field(self):
        for i in range(1, 82):
            self.field.append(Cell(count=i,
                                   row_number=self.get_row(i),
                                   column_number=self.get_column(i),
                                   square=self.get_square(i)))

    @staticmethod
    def get_row(count):
        return int((count - 1) / 9) + 1

    @staticmethod
    def get_column(count):
        return (count - 1) % 9 + 1

    def get_square(self, count):
        #   1   2	3
        #   4   5	6
        #   7	8	9
        return int((count - 1) / 27) * 3 + int((self.get_column(count) + 2) / 3)


class FieldTests(unittest.TestCase):
    def test_get_row(self):
        self.assertEqual(1, Field().get_row(1))
        self.assertEqual(1, Field().get_row(9))
        self.assertEqual(2, Field().get_row(10))
        self.assertEqual(2, Field().get_row(18))
        self.assertEqual(3, Field().get_row(19))
        self.assertEqual(9, Field().get_row(81))

    def test_get_column(self):
        self.assertEqual(1, Field().get_column(1))
        self.assertEqual(2, Field().get_column(2))
        self.assertEqual(8, Field().get_column(8))
        self.assertEqual(9, Field().get_column(9))
        self.assertEqual(1, Field().get_column(10))
        self.assertEqual(9, Field().get_column(18))
        self.assertEqual(1, Field().get_column(19))
        self.assertEqual(9, Field().get_column(81))

    def test_get_square(self):
        self.assertEqual(1, Field().get_square(1))
        self.assertEqual(1, Field().get_square(2))
        self.assertEqual(1, Field().get_square(3))
        self.assertEqual(1, Field().get_square(10))
        self.assertEqual(1, Field().get_square(11))
        self.assertEqual(1, Field().get_square(12))
        self.assertEqual(1, Field().get_square(19))
        self.assertEqual(1, Field().get_square(20))
        self.assertEqual(1, Field().get_square(21))
        self.assertEqual(5, Field().get_square(31))
        self.assertEqual(5, Field().get_square(41))
        self.assertEqual(5, Field().get_square(51))
        self.assertEqual(9, Field().get_square(61))
        self.assertEqual(9, Field().get_square(71))
        self.assertEqual(9, Field().get_square(81))


A = Field()
