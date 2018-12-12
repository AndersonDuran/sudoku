from board import GameBoard
from game import SudokuSolver

if __name__ == '__main__':
    
    with open('easy.txt', 'r') as easy:
        for line in easy:
            b = GameBoard(line)
            sudoku = SudokuSolver(b)
            response, elapsed = sudoku.solve()
            print(f'Sudoku {line} solution: {response} in {elapsed}s')

    with open('hard.txt', 'r') as easy:
        for line in easy:
            b = GameBoard(line)
            sudoku = SudokuSolver(b)
            response, elapsed = sudoku.solve(True)
            print(f'Sudoku {line} solution: {response} in {elapsed}s')

