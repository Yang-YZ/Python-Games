"""
Clone of 2048 game.
"""

import random
import poc_2048_gui

# Directions, DO NOT MODIFY
UP = 1
DOWN = 2
LEFT = 3
RIGHT = 4

# Offsets for computing tile indices in each direction.
# DO NOT MODIFY this dictionary.
OFFSETS = {UP: (1, 0),
           DOWN: (-1, 0),
           LEFT: (0, 1),
           RIGHT: (0, -1)}

def merge(line):
    """
    Function that merges a singlefor num in line:
    """
    line1 = []
    zeros = []
    line2 = []
    for num in line:
        if num != 0:
            line1.append(num)
        else:
            zeros.append(0)
    line1 = line1 + zeros
    for index in range(len(line1)-1):
        if line1[index] == line1[index+1]:
            line1[index] = 2 * line1[index]
            line1[index+1] = 0
            index =+ 1
    zeros = []
    for num in line1:
        if num != 0:
            line2.append(num)
        else:
            zeros.append(0)
    line2 = line2 + zeros
    return line2

class TwentyFortyEight:
    """
    Class to run the game logic.
    """
    def __init__(self, grid_height, grid_width):
        self._grid_height = grid_height
        self._grid_width = grid_width
        self.reset()
        self._initial_tiles = {UP: [(0, col) for col in range(self._grid_width)],
           DOWN: [(self._grid_height-1, col) for col in range(self._grid_width)],
           LEFT: [(row, 0) for row in range(self._grid_height)],
           RIGHT: [(row, self._grid_width-1) for row in range(self._grid_height)]}

    def reset(self):
        """
        Reset the game so the grid is empty except for two
        initial tiles.
        """
        self._cells = [ [0 for dummy_col in range(self._grid_width)] for dummy_row in range(self._grid_height)]        
        self.new_tile()
        self.new_tile()

    def __str__(self):
        """
        Return a string representation of the grid for debugging.
        """
        result = ""
        for line in self._cells:
            result += str(line) + "\n"
        return result

    def get_grid_height(self):
        """
        Get the height of the board.
        """
        return self._grid_height

    def get_grid_width(self):
        """
        Get the width of the board.
        """
        return self._grid_width

    def move(self, direction):
        """
        Move all tiles in the given direction and add
        a new tile if any tiles moved.
        """
        changed = False
        for init_cell in self._initial_tiles[direction]:
            init_line = []
            if direction == 1 or direction == 2:
                dim = self._grid_height
            else:
                dim = self._grid_width
            for index in range(dim):
                row = init_cell[0] + index * OFFSETS[direction][0]
                col = init_cell[1] + index * OFFSETS[direction][1]
                init_line.append(self._cells[row][col])
            merged_line = merge(init_line)
            for index in range(dim):
                row = init_cell[0] + index * OFFSETS[direction][0]
                col = init_cell[1] + index * OFFSETS[direction][1]
                if self._cells[row][col] != merged_line[index]:
                    self._cells[row][col] = merged_line[index]
                    changed = True
        if changed:
            self.new_tile()
        
    def new_tile(self):
        """
        Create a new tile in a randomly selected empty
        square.  The tile should be 2 90% of the time and
        4 10% of the time.
        """
        row = random.randint(0, self._grid_height - 1)
        col = random.randint(0, self._grid_width - 1)
        if self._cells[row][col] == 0:
            probability = 0.9
            rand_num = random.random()
            if rand_num < probability:
                self._cells[row][col] = 2
            else:
                self._cells[row][col] = 4
        else:
            self.new_tile()

    def set_tile(self, row, col, value):
        """
        Set the tile at position row, col to have the given value.
        """
        self._cells[row][col] = value

    def get_tile(self, row, col):
        """
        Return the value of the tile at position row, col.
        """
        return self._cells[row][col]

poc_2048_gui.run_gui(TwentyFortyEight(4, 4))