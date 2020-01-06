import random
class Grid():
    def __init__(self, rows, cols, live = "*", dead = "^"):
        self.rows = rows
        self.cols = cols
        self.live = live
        self.dead = dead
        self.grid = []

    def generate(self):
        """ generates the grid 
        ex of how grid will look:
        [[*, *, *, *, *],
         [*, *, *, *, *],
         [*, *, *, *, *]]"""
         # generates a completely dead cell base
        for row in range(self.rows):
            # this will generate each row within the column and fill them with empty lists
            temp_col = []
            for col in range(self.cols):
                temp_col.append(self.dead)
            self.grid.append(temp_col)
    
    def show(self):
        """ displays the grid
            * = live cell
            ^ = dead cell """
        # making sure that there's no empty grid
        if len(self.grid) == 0:
            self.generate()
        # prints each grid separated by a space
        for row in self.grid:
            for item in row:
                print(item, end = " ")
            print()

    def update(self, row, col, state=True):
        """ updates the row and column of a cell """
        # updating a single cell to anything (good for when you're bored)
        if state:
            self.grid[row][col] = self.live
        else:
            self.grid[row][col] = self.dead

    def set_up(self):
        """ sets up a random grid for the board """
        # this will randomize the bored through the random module
        for row in range(self.rows):
            for col in range(self.cols):
                # the state is determined on a random range from 0 to a random range of 25 to 50
                state = random.randint(0, random.randint(25, 50))
                # since three if my lucky number (33 is actually my favorite, but I can settle) so I took the 
                # state mod 3 to see if the cell will be alive or not.
                if state % 3 == 0:
                    self.update(row, col, self.live)
                else:
                    self.update(row, col, self.dead)
        
    def return_show(self):
        """...returns the grid"""
        return self.grid
