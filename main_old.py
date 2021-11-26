import sudoku_old

if __name__ == '__main__':
    data = sudoku_old.read_xlsx(r'2021-11-25.xlsx')
    new_data = sudoku_old.find_answer(data)
    for _ in range(30):
        new_data = sudoku_old.find_answer(new_data)
    sudoku_old.print_data_81(new_data)
