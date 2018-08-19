"""
Loyd's Fifteen puzzle - solver and visualizer
Note that solved configuration has the blank (zero) tile in upper left
Use the arrows key to swap this tile with its neighbors
"""

import poc_fifteen_gui

CIRCLES = {"LEFT_CIRCLE": "lddru",
          "UP_CIRCLE": "urrdl",
          "DOWN_CIRCLE": "drrul",
          "DOWN_LEFT_CIRCLE": "dllur",
          "UP_LEFT_CIRCLE": "ulldr",
          "RIGHT_CIRCLES": "rdlu"}

class Puzzle:
    """
    Class representation for the Fifteen puzzle
    """

    def __init__(self, puzzle_height, puzzle_width, initial_grid=None):
        """
        Initialize puzzle with default height and width
        Returns a Puzzle object
        """
        self._height = puzzle_height
        self._width = puzzle_width
        self._grid = [[col + puzzle_width * row
                       for col in range(self._width)]
                      for row in range(self._height)]

        if initial_grid != None:
            for row in range(puzzle_height):
                for col in range(puzzle_width):
                    self._grid[row][col] = initial_grid[row][col]

    def __str__(self):
        """
        Generate string representaion for puzzle
        Returns a string
        """
        ans = ""
        for row in range(self._height):
            ans += str(self._grid[row])
            ans += "\n"
        return ans

    #####################################
    # GUI methods

    def get_height(self):
        """
        Getter for puzzle height
        Returns an integer
        """
        return self._height

    def get_width(self):
        """
        Getter for puzzle width
        Returns an integer
        """
        return self._width

    def get_number(self, row, col):
        """
        Getter for the number at tile position pos
        Returns an integer
        """
        return self._grid[row][col]

    def set_number(self, row, col, value):
        """
        Setter for the number at tile position pos
        """
        self._grid[row][col] = value

    def clone(self):
        """
        Make a copy of the puzzle to update during solving
        Returns a Puzzle object
        """
        new_puzzle = Puzzle(self._height, self._width, self._grid)
        return new_puzzle

    ########################################################
    # Core puzzle methods

    def current_position(self, solved_row, solved_col):
        """
        Locate the current position of the tile that will be at
        position (solved_row, solved_col) when the puzzle is solved
        Returns a tuple of two integers        
        """
        solved_value = (solved_col + self._width * solved_row)

        for row in range(self._height):
            for col in range(self._width):
                if self._grid[row][col] == solved_value:
                    return (row, col)
        assert False, "Value " + str(solved_value) + " not found"

    def update_puzzle(self, move_string):
        """
        Updates the puzzle state based on the provided move string
        """
        zero_row, zero_col = self.current_position(0, 0)
        for direction in move_string:
            if direction == "l":
                assert zero_col > 0, "move off grid: " + direction
                self._grid[zero_row][zero_col] = self._grid[zero_row][zero_col - 1]
                self._grid[zero_row][zero_col - 1] = 0
                zero_col -= 1
            elif direction == "r":
                assert zero_col < self._width - 1, "move off grid: " + direction
                self._grid[zero_row][zero_col] = self._grid[zero_row][zero_col + 1]
                self._grid[zero_row][zero_col + 1] = 0
                zero_col += 1
            elif direction == "u":
                assert zero_row > 0, "move off grid: " + direction
                self._grid[zero_row][zero_col] = self._grid[zero_row - 1][zero_col]
                self._grid[zero_row - 1][zero_col] = 0
                zero_row -= 1
            elif direction == "d":
                assert zero_row < self._height - 1, "move off grid: " + direction
                self._grid[zero_row][zero_col] = self._grid[zero_row + 1][zero_col]
                self._grid[zero_row + 1][zero_col] = 0
                zero_row += 1
            else:
                assert False, "invalid direction: " + direction

    ##################################################################
    # Phase one methods
    
    def lower_row_invariant(self, target_row, target_col):
        """
        Check whether the puzzle satisfies the specified invariant
        at the given position in the bottom rows of the puzzle (target_row > 1)
        Returns a boolean
        """
        # Tile zero is positioned at (i,j).
        # All tiles in rows i+1 or below are positioned at their solved location.
        # All tiles in row i to the right of position (i,j) are positioned at their solved location.
        solved_lower = False
        solved_grid = [[col + self.get_width() * row
                       for col in range(self.get_width())]
                      for row in range(self._height)]
        if self._grid[target_row][target_col] == 0:
            solved_lower = True
            
        for row in range(target_row + 1, self._height):
            for col in range(self._width):
                if self._grid[row][col] != solved_grid[row][col]:
                    solved_lower = False
                    
        for col in range(target_col + 1, self._width):
                if self._grid[target_row][col] != solved_grid[target_row][col]:
                    solved_lower = False
                    
        return solved_lower

    def solve_interior_tile(self, target_row, target_col):
        """
        Place correct tile at target position
        Updates puzzle and returns a move string
        Our solution strategy will be to move the zero tile up 
        and across to the target tile. 
        Then we will move the target tile back to the target position 
        by applying a series of cyclic moves to the zero tile 
        that move the target tile back to the target position 
        one position at a time.
        """
        assert self._grid[target_row][target_col] == 0
        moves_str = ""
        target_current_row, target_current_col = self.current_position(target_row, target_col)
        
        moves_str += self.position_tile(target_row, target_col, target_current_row, target_current_col)        
        
        self.update_puzzle(moves_str)
        print "solve_interior_tile"
        print moves_str
        print self._grid
        return moves_str
    
    def position_tile(self, target_row, target_col, current_row, current_col):
        """
        Reposition the target tile to position (i-1,1)
        and the zero tile to position (i-1,0)
        """
        moves_str = ""
        # current target is on the upper of 0
        if current_col == target_col and current_row < target_row:
            ups = target_row - current_row
            for dummy_u in range(ups):
                moves_str += "u"
            for dummy_cycle in range(ups - 1):
                moves_str += CIRCLES["LEFT_CIRCLE"]
            moves_str += "ld"
        # current target is on the left of 0
        elif current_row == target_row and current_col < target_col:
            lefts = target_col - current_col
            for dummy_l in range(lefts):
                moves_str += "l"
            for dummy_cycle in range(lefts - 1):
                moves_str += CIRCLES["UP_CIRCLE"]
        # current target is on the upperleft of 0
        elif current_row < target_row and current_col < target_col:
            ups = target_row - current_row
            for dummy_u in range(ups):
                moves_str += "u"
            lefts = target_col - current_col
            for dummy_l in range(lefts):
                moves_str += "l"
            for dummy_cycle in range(lefts - 1):
                if current_row <= 0: # can not go up
                    moves_str += CIRCLES["DOWN_CIRCLE"]
                else:
                    moves_str += CIRCLES["UP_CIRCLE"]
            moves_str += "dru"
            for dummy_cycle in range(ups - 1):
                moves_str += CIRCLES["LEFT_CIRCLE"]
            moves_str += "ld"
        # current target is on the upperright of 0
        elif current_col > target_col and current_row < target_row:
            ups = target_row - current_row
            for dummy_u in range(ups):
                moves_str += "u"
            rights = current_col - target_col
            for dummy_r in range(rights):
                moves_str += "r"
            for dummy_cycle in range(rights - 1):
                if current_row <= 0: # can not go up
                    moves_str += CIRCLES["DOWN_LEFT_CIRCLE"]
                else:
                    moves_str += CIRCLES["UP_LEFT_CIRCLE"]        
            moves_str += "dlu"
            for dummy_cycle in range(ups - 1):
                    moves_str += CIRCLES["LEFT_CIRCLE"]
            moves_str += "ld"
        # current target is on the right of 0
        elif current_col > target_col and current_row == target_row:
            rights = current_col - target_col
            for dummy_r in range(rights):
                moves_str += "r"
            for dummy_cycle in range(rights - 1):
                if current_row <= 0: # can not go up
                    moves_str += CIRCLES["DOWN_LEFT_CIRCLE"]
                else:
                    moves_str += CIRCLES["UP_LEFT_CIRCLE"]   
            moves_str += "ulld"
        return moves_str
        
    def solve_col0_tile(self, target_row):
        """
        Solve tile in column zero on specified row (> 1)
        Updates puzzle and returns a move string
        """
        moves_str = ""
        # move the zero tile from (i,0) to (i−1,1) 
        # using the move string "ur"
        moves_str += "ur"
        temp_grid = Puzzle(self._height, self._width, self._grid)
        temp_grid.update_puzzle(moves_str)
        # If the target tile is now at position (i,0)
        # you can simply move tile zero to the end of row i−1
        current_row, current_col = temp_grid.current_position(target_row, 0)
        zero_row, zero_col = temp_grid.current_position(0, 0)
        if current_row == target_row and current_col == 0:
            rights = self._width - 1 - zero_col
            for dummy_r in range(rights):
                moves_str += "r"                
        # However, if the target tile is not positioned at (i,0)
        # we suggest the following solution strategy:
        else:
            moves_str += self.position_tile(zero_row, zero_col, current_row, current_col)
            moves_str += "ruldrdlurdluurddlu"
            for dummy_r in range(self._width - 1):
                moves_str += "r"
        
        print "solve_col0_tile"
        print moves_str
        self.update_puzzle(moves_str)
        print self._grid
        return moves_str

    #############################################################
    # Phase two methods

    def row0_invariant(self, target_col):
        """
        Check whether the puzzle satisfies the row zero invariant
        at the given column (col > 1)
        Returns a boolean
        """
        
        solved_lower_right = False
        solved_grid = [[col + self.get_width() * row
                       for col in range(self.get_width())]
                      for row in range(self._height)]
        if self._grid[0][target_col] == 0:
            solved_lower_right = True
        
        for row in range(1 + 1, self._height):
            for col in range(self._width):
                if self._grid[row][col] != solved_grid[row][col]:
                    solved_lower_right = False
        
        for row in range(0, 1):
            for col in range(target_col + 1, self._width):
                if self._grid[row][col] != solved_grid[row][col]:
                    solved_lower_right = False
                    
        if self._grid[1][target_col] != solved_grid[1][target_col]:
            solved_lower_right = False
            
        return solved_lower_right

    def row1_invariant(self, target_col):
        """
        Check whether the puzzle satisfies the row one invariant
        at the given column (col > 1)
        Returns a boolean
        """
        solved_lower_right = False
        solved_grid = [[col + self.get_width() * row
                       for col in range(self.get_width())]
                      for row in range(self._height)]
        if self._grid[1][target_col] == 0:
            solved_lower_right = True
            
        for row in range(1 + 1, self._height):
            for col in range(self._width):
                if self._grid[row][col] != solved_grid[row][col]:
                    solved_lower_right = False
        
        for row in range(0, 1):
            for col in range(target_col + 1, self._width):
                if self._grid[row][col] != solved_grid[row][col]:
                    solved_lower_right = False
                    
        return solved_lower_right

    def solve_row0_tile(self, target_col):
        """
        Solve the tile in row zero at the specified column
        Updates puzzle and returns a move string
        """
        # move the zero tile from position (0,j) to (1,j−1) 
        # using the move string "ld" 
        moves_str = ""
        moves_str += "ld"
        # check whether target tile is at position (0,j).
        temp_grid = Puzzle(self._height, self._width, self._grid)
        temp_grid.update_puzzle(moves_str)        
        current_row, current_col = temp_grid.current_position(0, target_col)
        zero_row, zero_col = temp_grid.current_position(0, 0)
        
        # If target tile is not at position (0,j).
        # reposition the target tile to position (1,j−1) 
        # with tile zero in position (1,j−2).
        if current_row != 0 or current_col != target_col:
            moves_str += self.position_tile(zero_row, zero_col, current_row, current_col)
            moves_str += "urdlurrdluldrruld"
        
        self.update_puzzle(moves_str)
        print "solve_row0_tile"
        print moves_str
        print self._grid
        return moves_str

    def solve_row1_tile(self, target_col):
        """
        Solve the tile in row one at the specified column
        Updates puzzle and returns a move string
        """
        moves_str = ""
        current_row, current_col = self.current_position(1, target_col)
        zero_row, zero_col = self.current_position(0, 0)
        moves_str += self.position_tile(zero_row, zero_col, current_row, current_col)
        moves_str += "ur"
        self.update_puzzle(moves_str)
        print "solve_row1_tile"
        print moves_str
        print self._grid
        return moves_str

    ###########################################################
    # Phase 3 methods

    def solve_2x2(self):
        """
        Solve the upper left 2x2 part of the puzzle
        Updates the puzzle and returns a move string
        """
        moves_str = ""
        # move zero to the most upper left
        zero_row, zero_col = self.current_position(0, 0)
        ups = zero_row - 0
        lefts = zero_col - 0
        for dummy_u in range(ups):
            moves_str += "u"
        for dummy_l in range(lefts):
            moves_str += "l"
        
        # get zero, one, two, three positions
        self.update_puzzle(moves_str)
        zero_row, zero_col = self.current_position(0, 0)
        one_row, one_col = self.current_position(0, 1)
        two_row, two_col = self.current_position(1, 0)
        three_row, three_col = self.current_position(1, 1)
        counter = 0
        while counter <= 3 and \
              (zero_row != 0 or zero_col != 0 or \
              one_row!= 0 or one_col != 1 or \
              two_row != 1 or two_col != 0 or \
              three_row != 1 or three_col != 1):
            move = CIRCLES["RIGHT_CIRCLES"]
            moves_str += move
            self.update_puzzle(move)
            counter += 1
            zero_row, zero_col = self.current_position(0, 0)
            one_row, one_col = self.current_position(0, 1)
            two_row, two_col = self.current_position(1, 0)
            three_row, three_col = self.current_position(1, 1)
            
        print "solve_2x2"
        print moves_str
        print self._grid
        return moves_str

    def solve_puzzle(self):
        """
        Generate a solution string for a puzzle
        Updates the puzzle and returns a move string
        """
        moves_str = ""
        # move zero to the most botton right
        zero_row, zero_col = self.current_position(0, 0)
        downs = self._height - 1 - zero_row
        rights = self._width - 1 - zero_col
        for dummy_d in range(downs):
            moves_str += "d"
        for dummy_r in range(rights):
            moves_str += "r"
        self.update_puzzle(moves_str)
        # Solve the bottom m−2 rows of the puzzle 
        # in a row by row manner from bottom to top. 
        # Each individual row will be solved in a right to left order.
        if self._height > 2 and self._width > 2:
            for row in range(self._height - 1, 1, -1):
                for col in range(self._width - 1, 0, -1):
                    assert self.lower_row_invariant(row, col)
                    moves_str += self.solve_interior_tile(row, col)
                    assert self.lower_row_invariant(row, col - 1)
                assert self.lower_row_invariant(row, 0)
                moves_str += self.solve_col0_tile(row)
                assert self.lower_row_invariant(row - 1, self._width - 1)
        # Solve the rightmost n−2 columns of the top two rows
        # in a right to left order). 
        # Each column consists of two unsolved positions 
        # and will be solved in a bottom to top order.
            for col in range(self._width - 1, 1, -1):
                assert self.row1_invariant(col)
                moves_str += self.solve_row1_tile(col)
                assert self.row0_invariant(col)
                moves_str += self.solve_row0_tile(col)
                assert self.row1_invariant(col - 1)
        # Solve the upper left 2×2 portion of the puzzle directly.
            assert self.row1_invariant(1)
            moves_str += self.solve_2x2()
        
        elif self._height <=2 and self._width > 2:
            for col in range(self._width - 1, 1, -1):
                assert self.row1_invariant(col)
                moves_str += self.solve_row1_tile(col)
                assert self.row0_invariant(col)
                moves_str += self.solve_row0_tile(col)
                assert self.row1_invariant(col - 1)
        # Solve the upper left 2×2 portion of the puzzle directly.
            assert self.row1_invariant(1)
            moves_str += self.solve_2x2()
        elif self._height <= 2 and self._width <= 2:
            assert self.row1_invariant(1)
            moves_str += self.solve_2x2()
        #elif self._height > 2 and self._width <= 2:
            
        print moves_str
        print self._grid
        return moves_str

# Start interactive simulation
poc_fifteen_gui.FifteenGUI(Puzzle(4, 4,[[2,1,0,9],[5,8,4,3],[6,7,10,11],[12,13,14,15]]))
#print Puzzle(4, 4,[[2,1,0,9],[5,8,4,3],[6,7,10,11],[12,13,14,15]])
#Obj = Puzzle(3, 3, [[8, 7, 6], [5, 4, 3], [2, 1, 0]])
#print Obj
#assert Obj.lower_row_invariant(2,2)
#Obj.solve_interior_tile(2, 2)
#assert Obj.lower_row_invariant(2,2-1)
#
#Obj = Puzzle(3, 2, [[2,4], [3,1], [0,5]])
#print Obj
#assert Obj.lower_row_invariant(2, 0)
#Obj.solve_col0_tile(2) 
#assert Obj.lower_row_invariant(2 - 1, 2 - 1)
#
#obj = Puzzle(3, 3, [[3, 2, 1], [6, 5, 4], [0, 7, 8]])
#print obj
#assert obj.lower_row_invariant(2, 0)
#obj.solve_col0_tile(2)
#assert obj.lower_row_invariant(2 - 1, 3 - 1)
#
#obj = Puzzle(4, 5, [[12, 11, 10, 9, 15], [7, 6, 5, 4, 3], [2, 1, 8, 13, 14], [0, 16, 17, 18, 19]])
#print obj
#assert obj.lower_row_invariant(3, 0)
#obj.solve_col0_tile(3)
#assert obj.lower_row_invariant(3 - 1, 5 - 1)

#obj = Puzzle(4, 4, [[4,6,1,3], [5,2,0,7], [8,9,10,11], [12,13,14,15]])
#print obj
#assert obj.row1_invariant(2)
#obj.solve_row1_tile(2)
#print obj
#assert obj.row0_invariant(2)
#obj.solve_row0_tile(2)
#print obj
#assert obj.row1_invariant(2 - 1)

#obj = Puzzle(2, 3, [[3, 1, 0], [2, 4, 5]])
#print obj
#obj.solve_row0_tile(2)
#print obj

#obj = Puzzle(3, 3, [[4, 1, 0], [2, 3, 5], [6, 7, 8]])
#print obj
#obj.solve_row0_tile(2)

#obj = Puzzle(2, 2, [[0,2], [3,1]])
#print obj
#obj.solve_2x2()
#print obj

#obj = Puzzle(2, 2, [[0,3], [1,2]])
#print obj
#obj.solve_2x2()
#print obj

#obj = Puzzle(3, 3, [[8, 7, 6], [5, 4, 3], [2, 1, 0]])
#print obj
#obj.solve_puzzle() 
#print obj

#obj = Puzzle(4,4, [[5, 2, 1, 3], [7, 6, 4, 8], [0, 9, 10, 11], [12, 13, 14, 15]])
#print obj
#obj.solve_col0_tile(2)
#print obj

obj = Puzzle(2, 4, [[0, 3, 2, 7], [4, 5, 6, 1]])
print obj
obj.solve_puzzle()