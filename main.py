import sudoku

if __name__ == '__main__':
    field = sudoku.Field()
    field.read_xlsx(r'expert2.xlsx')
    field.find_answer()

    # print(field.get_impossible_options())

    field.find_options()
    field.print_values(field.get_options())
