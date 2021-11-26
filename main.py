import sudoku

if __name__ == '__main__':
    field = sudoku.Field()
    field.read_xlsx(r'2021-11-25.xlsx')
    for _ in range(11):
        field.find_answer()
    field.print_field()
