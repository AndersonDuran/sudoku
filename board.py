class GameBoard():

    def __init__(self, initializer):
        rows = 'ABCDEFGHI'
        cols = '123456789'

        self.squares = self.__cross__(rows, cols)
        self.initializer = initializer

        cols_constraints = [self.__cross__(rows, c) for c in cols]
        rows_constraints = [self.__cross__(r, cols) for r in rows]
        self.unit_constraints = [self.__cross__(x, y) for x in ['ABC', 'DEF', 'GHI'] for y in ['123', '456', '789']]

        constraints = cols_constraints
        constraints.extend(rows_constraints)
        constraints.extend(self.unit_constraints)
        
        self.constraints = constraints

        self.peers = {k:self.__build_units__(k) for k in self.squares}
        self.values = dict(zip(self.squares, initializer))

        self.units = {k:v for k in self.squares for v in self.unit_constraints if k in v}

    def getInitializer(self):
        return self.initializer

    def getValues(self):
        return self.values

    def setValues(self, values):
        self.values = values

    def getPeers(self, square):
        return self.peers[square.upper()]
    
    def getUnits(self, square):
        return self.units[square]

    def getUnitsList(self):
        return self.unit_constraints

    def __cross__(self, l1, l2):
        return [a+b for a in l1 for b in l2]

    def __build_units__(self, square):
        square = square.upper()
        units_list = [const for const in self.constraints if square in const]
        units_set = set(units_list[0] + units_list[1] + units_list[2])
        units_set.remove(square)
        return units_set