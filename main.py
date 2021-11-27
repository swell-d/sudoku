import sudoku

if __name__ == '__main__':
    field = sudoku.Field()
    field.read_xlsx(r'2021-11-24.xlsx')
    field.find_answer()
    # print('')
    # field.print_values(field.find_options2(3))

