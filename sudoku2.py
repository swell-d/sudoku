import unittest


class Cell:
    def __init__(self, count, row_number, column_number, square, value=None):
        self.count = count  # from 1 to 81
        self.row_number = row_number  # from 1 to 9
        self.column_number = column_number  # from 1 to 9
        self.square = square  # from 1 to 9
        self.value = value  # from 1 to 9
        self.options = []


class Field:
    def __init__(self):
        self.field = []

    def create_field(self):
        for row in range(1, 10):
            for column in range(1, 10):
                self.field.append(
                    Cell(count=len(self.field) + 1,
                         row_number=row,
                         column_number=column,
                         square=int((row - 1) / 3) * 3 + int((column - 1) / 3) + 1))


class FieldTests(unittest.TestCase):
    pass


A = Field()
A.create_field()
