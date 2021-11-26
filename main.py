import sudoku

if __name__ == '__main__':
    field = sudoku.Field()
    field.read_xlsx(r'2021-11-26.xlsx')
    field.find_answer()
