class Cell():
    def __init__(self, grid, random = True):
        self.grid = grid
        self.rows = self.grid.rows
        self.cols = self.grid.cols
        if len(self.grid.grid) == 0:
            self.grid.generate()
            if random == True:
                self.grid.set_up()
        # print("eyyyyyyyyyyy") debugging ya know 
    
    def check_all(self):
        """ checks all the the points to make sure that they are valid """
        # creating an alternate grid so that the grid correctly mutates
        tempFull_grid = []
        for row in self.grid.grid:
            temp_row = []
            for col in row:
                temp_row.append(col)
            tempFull_grid.append(temp_row)

        # checks through each row and column to mutate each cell
        for row in range(self.rows):
            for col in range(self.cols):
                tempFull_grid[row][col] = self.status_check(row, col)
        self.grid.grid = tempFull_grid[:]
        
    def status_check(self, row, col):
        """ Checks if the cell will stay alive """
        # gets the 3x3 grid around the cell to check if the status
        temp_grid = self.cell_check(row, col)

        # checks if the cell is already alive and if it shall stay alive
        if self.grid.grid[row][col] == self.grid.live:
            if self.keep_alive(temp_grid, row, col):
                return self.grid.live
        else:
            # if the cell is dead, it checks if it can be born
            if self.birth(temp_grid):
                return self.grid.live
        
        # if it won't stay alive nor will be born then it will stay dead
        return self.grid.dead
    
    def keep_alive(self, temp_grid, row, col):
        """ Checks the surrounding cells for 
        two or three other living cells """
        # keeps a count of the living cells
        live = 0
        # in the temporary grid, generated in the status_check function, 
        # it'll check how many surrounding cells are actually living cells
        for temp_row in temp_grid:
            for temp_col in temp_row:
                if temp_col == self.grid.live:
                    live += 1
        # subtracts one from itself if the main cell happens to be alive
        if self.grid.grid[row][col] == self.grid.live:
            # print("alive")
            live -= 1
        # due to the rules being that the cell must have two or three neighbors to be alive,
        # that will be the only time that True will be returned
        return True if live == 2 or live == 3 else False

    def birth(self, temp_grid):
        """ Checks the surrounding cells for 
        three other living cells """
        # just live the keep_alive function, this will keep track of nearby living cells
        live = 0
        # finds the number of surrounding cells that are actually alive near this dead cell
        for temp_row in temp_grid:
            for temp_col in temp_row:
                if temp_col == self.grid.live:
                    live += 1
        # for a cell to be reborn, it must have only three living neighbors
        return True if live == 3 else False
    
    def cell_check(self, row, col):
        """ returns a 3x3 grid of cells """
        # the starting column of the nearby cells
        start_col = col - 1 if col != 0 else 0
        # end column for nearby cells
        end_col = col + 1 if col != self.cols else self.cols
        # starting column for nearby cells
        start_row = row - 1 if row != 0 else 0
        # end column for nearby cells
        end_row = row + 1 if row != self.rows else self.rows
        # creating the new grid
        # this will be used to check the amount of living cells to determine living cells
        temp_grid = []
        for temp_row in self.grid.grid[start_row:end_row+1]:
            # print(temp_row)
            temp_grid.append(temp_row[start_col:end_col+1])
        return temp_grid