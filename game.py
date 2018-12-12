from board import GameBoard
from collections import OrderedDict
import pdb 
import time

class SudokuSolver():

    def __init__(self, board):
        self.board = board
        self.options = dict(self.board.getValues())
        for key in self.options:
            if self.options[key] == '.':
                self.options[key] = '123456789'

    def solve(self, verbose=False):
        if verbose:
            print('ORIGINAL GRID')
            self.display(self.options)

        start = time.time()
        self.propagateConstraints(self.options)
        if self.testSolution(self.options):
            if verbose:
                print('PURE CSP SOLUTION')
                self.display(self.options)
            return ('pure csp', time.time() - start)
        else:
            grid = self.search(self.options)
            if not grid:
                if verbose:
                    print('NO SOLUTION WAS FOUND')
                return ('no solution', time.time() - start)
            else:
                if verbose:
                    print('CSP AND SEARCH SOLUTION')
                    self.display(grid)
                return ('csp and search', time.time() - start)

    def assign(self, grid, square, value):
        grid[square] = value

        if self.propagateConstraints(grid):
            return grid
        return False

    def search(self, options):
        if options is False:
            return False
        
        if self.testSolution(options):
            return options

        _, square = min((len(options[s]), s) for s in options.keys() if len(options[s]) > 1)

        for value in options[square]:
            result = self.search(self.assign(options.copy(), square, value))        
            if result:
                return result

    def some(self, l):
        for e in l:
            if e:
                return e
        return False

    def testSolution(self, options): 
        return all(len(options[key]) == 1 for key in options)

    def propagateConstraints(self, options):
        if self.eliminateOptions(options):
            if self.assignOptions(options):
                return self.propagateConstraints(options)
            return True
        return False

    def eliminateOptions(self, options):
        for square in options.keys():
            value = options[square]
            if len(value) == 1:
                peers = self.board.getPeers(square)
                for peer in peers:
                    if value in options[peer]:
                        options[peer] = options[peer].replace(value, '')
                        if len(options[peer]) == 0:
                            return False
        return True

    def assignOptions(self, options):
        units = self.board.getUnitsList()
        for unit in units:
            for value in range(1,10):
                places = [sq for sq in unit if str(value) in options[sq]]
                if len(places) == 0:
                    return False
                elif len(places) == 1 and len(options[places[0]]) > 1:
                    options[places[0]] = str(value)
                    return True
        return False

    def display(self, options, hide_options = False):
        line = ''
        col_count = 0
        row_count = 0

        rows = 'ABCDEFGHI'
        cols = '123456789'

        print('-------------------------------------+--------------------------------------+-------------------------------------')
        for row in rows:
            for col in cols:
                value = options[row+col]
                if hide_options:
                    if len(value) != 1:
                        value = '.'
                value = value.center(11, ' ')
                line = line + value + ' '    
                col_count += 1
                if col_count == 3 or col_count == 6:
                    line = line + ' | '
                if col_count == 9:
                    print(line)
                    line = ''
                    col_count = 0
                    row_count += 1
                if row_count == 3 or row_count == 7:
                    print('-------------------------------------+--------------------------------------+-------------------------------------')
                    row_count += 1
        print('-------------------------------------+--------------------------------------+-------------------------------------')