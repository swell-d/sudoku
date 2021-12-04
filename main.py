import sudoku

if __name__ == '__main__':
    field = sudoku.Field()
    field.read_xlsx(r'expert.xlsx')
    field.find_answer()

    field.find_options3()
    # field.print_values(field.get_options())

    field.find_options2(1).print_field()
    field.find_options2(2).print_field()
    field.find_options2(3).print_field()
    field.find_options2(4).print_field()
    field.find_options2(7).print_field()
    field.find_options2(8).print_field()
    field.find_options2(9).print_field()

