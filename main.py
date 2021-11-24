import sudoku

if __name__ == '__main__':
    data = sudoku.read_xlsx(r'2021-11-24.xlsx')
    new_data = sudoku.find_answer(data)
    for _ in range(22):
        new_data = sudoku.find_answer(new_data)
    sudoku.print_data_81(new_data)
