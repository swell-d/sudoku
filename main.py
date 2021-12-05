import sudoku

if __name__ == '__main__':
    field = sudoku.Field()
    field.read_xlsx(r'expert.xlsx')
    field.find_answer()
