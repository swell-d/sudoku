import sudoku

if __name__ == '__main__':
    field = sudoku.Field()
    field.read_xlsx(r'expert.xlsx')
    field.find_answer()

    field.find_options3()
    # field.print_values(field.get_options())

    matrix = field.find_options2(3)
    matrix.print_field()
