import sudoku2

if __name__ == '__main__':
    field = sudoku2.Field()
    field.read_xlsx(r'2021-11-23.xlsx')
    field.print_data_81()
