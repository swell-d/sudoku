import sudoku


def try_every_option(field):
    field.find_options()
    for i, options in enumerate(field.get_options()):
        if len(options) == 1:
            continue
        for option in options:
            # print(f'{i} {option}')
            option_field = sudoku.Field(field.get_all_values())
            option_field.cells[i].value = option
            option_field.find_answer(hard=False)
            if option_field.found == 81:
                return option_field


if __name__ == '__main__':
    field = sudoku.Field()
    field.read_xlsx(r'expert2.xlsx')
    field.find_answer(print_info=True)

    if field.found != 81:
        result = try_every_option(field)
        print('')
        result.print_field()
