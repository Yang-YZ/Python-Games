"""
Zombie Apocalypse
"""

import random
import poc_grid
import poc_queue
import poc_zombie_gui

# global constants
EMPTY = 0 
FULL = 1
FOUR_WAY = 0
EIGHT_WAY = 1
OBSTACLE = 5
HUMAN = 6
ZOMBIE = 7


class Apocalypse(poc_grid.Grid):
    """
    Class for simulating zombie pursuit of human 
    on grid with obstacles
    """

    def __init__(self, grid_height, grid_width, obstacle_list = None, 
                 zombie_list = None, human_list = None):
        """
        Create a simulation of given size 
        with given obstacles, humans, and zombies
        """
        poc_grid.Grid.__init__(self, grid_height, grid_width)
        
        if obstacle_list != None:
            for cell in obstacle_list:
                self.set_full(cell[0], cell[1])
        
        self._zombie_list = poc_queue.Queue()
        if zombie_list != None:
            for zombie in zombie_list:
                self._zombie_list.enqueue(zombie)
        
        self._human_list = poc_queue.Queue()
        if human_list != None:
            for human in human_list:
                self._human_list.enqueue(human)
        
    def clear(self):
        """
        Reset all cells in obstacle grid to be empty
        Reset zombie and human lists to be empty
        """
        poc_grid.Grid.clear(self)
        self._zombie_list.clear()
        self._human_list.clear()
        
    def add_zombie(self, row, col):
        """
        Add zombie to the zombie list
        """
        self._zombie_list.enqueue((row, col))
                
    def num_zombies(self):
        """
        Return number of zombies
        """
        return len(self._zombie_list)
          
    def zombies(self):
        """
        Generator that yields the zombies 
        in the order they were added.
        """
        for zombie in self._zombie_list:
            yield zombie

    def add_human(self, row, col):
        """
        Add human to the human list
        """
        self._human_list.enqueue((row, col))
        
    def num_humans(self):
        """
        Return number of humans
        """
        return len(self._human_list)
    
    def humans(self):
        """
        Generator that yields the humans in the order they were added.
        """
        for human in self._human_list:
            yield human
        
    def compute_distance_field(self, entity_type):
        """
        Function computes and returns a 2D distance field
        Distance at member of entity_list is zero
        Shortest paths avoid obstacles and use four-way distances
        """
        visited = poc_grid.Grid(self._grid_height, self._grid_width)
        distance_field = [[self._grid_height * self._grid_width
                          for dummy_col in range(self._grid_width)]
                          for dummy_row in range(self._grid_height)]
        # Create a queue boundary that is a copy of 
        # either the zombie list or the human list. 
        # For cells in the queue, initialize visited to be FULL 
        # and distance_field to be zero.
        boundary = poc_queue.Queue()
        if entity_type == HUMAN:
            for human in self._human_list:
                boundary.enqueue(human)
        else:
            for zombie in self._zombie_list:
                boundary.enqueue(zombie)
            
        for cell in boundary:
            visited.set_full(cell[0],cell[1])
            distance_field[cell[0]][cell[1]] = 0
        
        while len(boundary) > 0:
            current_cell = boundary.dequeue()
            neighbors = visited.four_neighbors(current_cell[0], current_cell[1])
            for neighbor in neighbors:
                if visited.is_empty(neighbor[0], neighbor[1]) and self.is_empty(neighbor[0], neighbor[1]):
                    visited.set_full(neighbor[0], neighbor[1])
                    boundary.enqueue(neighbor)
                    distance_field[neighbor[0]][neighbor[1]] = distance_field[current_cell[0]][current_cell[1]] + 1
        return distance_field
    
    def move_humans(self, zombie_distance_field):
        """
        Function that moves humans away from zombies, 
        diagonal moves are allowed.
        This method updates the entries in the human list.
        Each human either stays in its current cell 
        or moves to a neighboring cell
        to maximize its distance from the zombies.
        """
        human_replace = []
        for human in self._human_list:
            best_neighbor = human
            max_distance = zombie_distance_field[human[0]][human[1]]
            neighbors8 = self.eight_neighbors(human[0], human[1])
            for neighbor in neighbors8:
                if self.is_empty(neighbor[0], neighbor[1]) and zombie_distance_field[neighbor[0]][neighbor[1]] > max_distance:
                    best_neighbor = neighbor
            human_replace.append(best_neighbor)
            
        for human in human_replace:
            self._human_list.dequeue()
            self._human_list.enqueue(human)
    
    def move_zombies(self, human_distance_field):
        """
        Function that moves zombies towards humans, 
        no diagonal moves are allowed.
        This method updates the entries in the zombie list.
        Each zombie either stays in its current cell 
        or moves to a neighboring cell to minimize its distance to the humans.
        """
        zombie_replace = []
        for zombie in self._zombie_list:
            best_neighbor = zombie
            min_distance = human_distance_field[zombie[0]][zombie[1]]
            neighbors4 = self.four_neighbors(zombie[0], zombie[1])
            for neighbor in neighbors4:
                if self.is_empty(neighbor[0], neighbor[1]) and human_distance_field[neighbor[0]][neighbor[1]] < min_distance:
                    best_neighbor = neighbor
            zombie_replace.append(best_neighbor)
            
        for zombie in zombie_replace:
            self._zombie_list.dequeue()
            self._zombie_list.enqueue(zombie)


poc_zombie_gui.run_gui(Apocalypse(30, 40))