# Import packages
import random
import pygame
import numpy as np


class SudokuGame:
    def __init__(self, base, clues, unique):
        # Visual variables
        self.screen, self.font1, self.font2 = None, None, None
        self.pos_x = 0
        self.pos_y = 0
        self.box_side = 50
        # Sudoku variables
        self.clues = clues
        self.base = base
        self.side = base ** 2
        self.n_cells = self.side ** 2
        # List of numbers that can be inserted in a cell
        self.list_numbers = [i for i in range(1, self.side + 1)]
        self.grid = np.zeros([self.side, self.side], dtype=np.int16)
        self.counter = 0
        # Variable used to restore the starting puzzle
        self.starting_grid = None
        # Initialize game
        self.initialise_game(unique)

    def initialise_game(self, unique=False):
        """
        Initialises the game creating the window and generating the sudoku grid.

        :param unique: boolean useful to require a sudoku with a sole solution or vice versa.
        :return:
        """
        # Initialise the pygame font
        pygame.font.init()
        # Total window
        self.screen = pygame.display.set_mode((self.box_side * self.side, self.box_side * self.side))
        # Title and Icon
        pygame.display.set_caption("Sudoku Solver")
        # Load test fonts for future use
        self.font1 = pygame.font.SysFont("comicsans", 40)
        self.font2 = pygame.font.SysFont("comicsans", 20)
        # Generate Sudoku
        self.generate()
        if not unique:
            # Generate a sudoku that may have more solutions
            # This option is pretty fast as the cell are emptied randomly.
            self.get_sudoku(clues=self.clues)
        else:
            # Generate a sudoku with only a single solution
            self.get_unique_sudoku(clues=self.clues)
        # Save a copy of the originated sudoku
        self.starting_grid = np.copy(self.grid)

    def is_valid(self, number, row, col):
        """
        Checks if a number given can be inserted in the puzzle at the passed row and column.

        :param number: value to insert in the selected cell.
        :param row: first coordinate to identify the cell in the grid on which to work.
        :param col: second coordinate to identify the cell in the grid on which to work.
        :return: False if the insertion is not valid, True otherwise.
        """
        # Execute the control on the related row and column
        if number in self.grid[row, :]:
            return False
        if number in self.grid[:, col]:
            return False
        # Find the first coordinates from which the NxN box develops
        starting_x = row // self.base * self.base
        starting_y = col // self.base * self.base
        # Execute the control on the related NxN box
        if number in self.grid[starting_x:starting_x + self.base, starting_y:starting_y + self.base]:
            return False
        return True

    def generate(self):
        """
        Generates a new fully solved sudoku table through a backtracking algorithm.

        :return: False if there is no possible solution, True when the sudoku is solved.
        """
        # Iterate over each cell in the grid
        for i in range(self.n_cells):
            row = i // self.side
            col = i % self.side
            # Find the next empty cell
            if self.grid[row][col] == 0:
                # Shuffle the numbers accepted by the game
                random.shuffle(self.list_numbers)
                for number in self.list_numbers:
                    if self.is_valid(number, row, col):
                        # For each valid number set it into the empty cell and try to solve the puzzle
                        self.grid[row][col] = number
                        # If the sudoku is finished exit
                        if 0 not in self.grid:
                            return True
                        # Try to solve the sudoku starting from the last number added
                        elif self.generate():
                            return True
                # If there is no solution from the last change, empty the cell modified and exit from the cycle
                self.grid[row][col] = 0
                break
        # If the sudoku cannot be solved return False
        return False

    def get_unique_sudoku(self, attempts=10, clues=17):
        """
        Generates a unique sudoku from an already completed grid.

        :param attempts: describes the number of attempts are tried to find a unique solution of the puzzle.
        :param clues: number of cells that are intended to remain as is.
        :return:
        """
        # Coordinates of all the non empty cells
        (indexes_x, indexes_y) = np.nonzero(self.grid)
        while attempts > 0 and len(indexes_x) > clues:
            print(f'Number of non empty cells: {len(indexes_x)}')
            # Take a tuple of coordinates by random
            idx = np.random.randint(0, len(indexes_x))
            row, col = indexes_x[idx], indexes_y[idx]
            # Temporary empty a cell
            removed_square = self.grid[row][col]
            self.grid[row][col] = 0
            # Keep a copy of the grid after the modification
            grid_copy = np.copy(self.grid)
            # Reset the counter related to the number of solutions found
            self.counter = 0
            self.fast_insert_sure_numbers()
            if 0 not in self.grid:
                self.counter = 1
            else:
                # Solve the sudoku after the deletion
                self.fast_solve()
            # In case there is not a single solution
            if self.counter != 1:
                # Reset the previous state of the grid
                self.grid = np.copy(grid_copy)
                self.grid[row][col] = removed_square
                attempts -= 1
            else:
                # Otherwise, start from the last cell removed and delete the coordinates related to it
                self.grid = np.copy(grid_copy)
                indexes_x = np.delete(indexes_x, idx)
                indexes_y = np.delete(indexes_y, idx)

    def get_sudoku(self, clues=17):
        """
        Generates a sudoku from an already completed grid.

        :param clues: number of cells to retain.
        :return:
        """
        # Coordinates of all the non empty cells
        (indexes_x, indexes_y) = np.nonzero(self.grid)
        while len(indexes_x) >= clues:
            # Take a tuple of coordinates by random
            idx = np.random.randint(0, len(indexes_x))
            row, col = indexes_x[idx], indexes_y[idx]
            # Temporary empty a cell
            self.grid[row][col] = 0
            # Delete the coordinates related to it
            indexes_x = np.delete(indexes_x, idx)
            indexes_y = np.delete(indexes_y, idx)

    def get_coordinates(self, position):
        """
        Convert the pixel coordinates into the row and the column of the selected cell.

        :param position: Pixel coordinates.
        """
        self.pos_x = position[0] // self.box_side
        self.pos_y = position[1] // self.box_side

    def draw_box(self):
        """
        Highlights the cell selected.
        """
        pygame.draw.rect(self.screen, (255, 0, 0), pygame.Rect(self.pos_x * self.box_side, self.pos_y * self.box_side,
                                                               self.box_side, self.box_side), 6)

    def draw(self):
        """
        Draws the sudoku puzzle.
        """
        # Iterate over each cell in the grid
        for i in range(self.n_cells):
            row = i // self.side
            col = i % self.side
            # Print the numbers where the cells are not empty
            if self.grid[row][col] != 0:
                # Colour only the cells belonging to the starting grid
                if self.starting_grid[row][col] != 0:
                    pygame.draw.rect(self.screen, (0, 200, 200),
                                     (col * self.box_side, row * self.box_side, self.box_side, self.box_side))
                else:
                    pygame.draw.rect(self.screen, (255, 255, 255),
                                     (col * self.box_side, row * self.box_side, self.box_side, self.box_side))
                # Fill grid with the default numbers
                text1 = self.font1.render(str(self.grid[row][col]), 1, (0, 0, 0))
                self.screen.blit(text1, (col * self.box_side + 15, row * self.box_side + 15))
        # Draw lines to form the grid
        for i in range(self.side + 1):
            # Set the thickness low of the lines depending on they separate the boxes or simply the cells
            if i % self.base == 0:
                thick = 7
            else:
                thick = 1
            # Draw both horizontally and vertically lines
            pygame.draw.line(self.screen, (0, 0, 0), (0, i * self.box_side),
                             (self.box_side * self.side, i * self.box_side), thick)
            pygame.draw.line(self.screen, (0, 0, 0), (i * self.box_side, 0),
                             (i * self.box_side, self.box_side * self.side), thick)

    def play(self):
        """
        Main function to play the game.
        """
        # Temporary variables useful in the handling of the events
        val, flag1 = 0, 0
        # Infinite loop to keep the window running
        while True:
            # White color background
            self.screen.fill((255, 255, 255))
            # Loop through the events stored in event.get()
            for event in pygame.event.get():
                # Get the mouse position and coordinates
                if event.type == pygame.MOUSEBUTTONDOWN:
                    flag1 = 1
                    pos = pygame.mouse.get_pos()
                    self.get_coordinates(pos)
                # Act in a specific way according to the key pressed
                if event.type == pygame.KEYDOWN:
                    # Management of the arrows
                    if event.key == pygame.K_LEFT:
                        self.pos_x -= 1
                        flag1 = 1
                    if event.key == pygame.K_RIGHT:
                        self.pos_x += 1
                        flag1 = 1
                    if event.key == pygame.K_UP:
                        self.pos_y -= 1
                        flag1 = 1
                    if event.key == pygame.K_DOWN:
                        self.pos_y += 1
                        flag1 = 1
                    # Management of the numbers
                    if event.key == pygame.K_1:
                        val = 1
                    if event.key == pygame.K_2:
                        val = 2
                    if event.key == pygame.K_3:
                        val = 3
                    if event.key == pygame.K_4:
                        val = 4
                    if event.key == pygame.K_5:
                        val = 5
                    if event.key == pygame.K_6:
                        val = 6
                    if event.key == pygame.K_7:
                        val = 7
                    if event.key == pygame.K_8:
                        val = 8
                    if event.key == pygame.K_9:
                        val = 9
                    # If the user press CANC delete the number in the selected cell
                    if event.key == pygame.K_DELETE:
                        self.delete_number()
                    # If the user press D restart the sudoku from the starting grid
                    if event.key == pygame.K_d:
                        self.grid = np.copy(self.starting_grid)
                    # If the user press ENTER automatically solve the sudoku
                    if event.key == pygame.K_RETURN:
                        self.insert_sure_numbers()
                        self.solve()
                    # If the user press Q quit the game
                    if event.key == pygame.K_q:
                        pygame.quit()
                    # If the user press P return to the main menu
                    if event.key == pygame.K_p:
                        return
            # If a number has been pressed...
            if val != 0:
                # And if it is valid and the selected cell is empty in the starting grid...
                if self.is_valid(val, self.pos_y, self.pos_x) and \
                        self.starting_grid[self.pos_y][self.pos_x] == 0:
                    # Set the number in the chosen cell
                    self.grid[self.pos_y][self.pos_x] = val
                    # Remove the visualisation of the cell selected
                    flag1 = 0
                val = 0
            # Draw the entire sudoku
            self.draw()
            # If True visualise the cell selected
            if flag1 == 1:
                self.draw_box()
            # Update window
            pygame.display.update()

    def delete_number(self):
        """
        Deletes the number within a cell if empty in the starting sudoku
        """
        if self.starting_grid[self.pos_y][self.pos_x] == 0:
            self.grid[self.pos_y][self.pos_x] = 0

    def solve(self):
        """
        Solves the sudoku.

        :return: True when completed, False if no solution is possible.
        """
        # Iterate over each cell in the grid
        for i in range(self.n_cells):
            row = i // self.side
            col = i % self.side
            # Find next empty cell
            if self.grid[row][col] == 0:
                # Iterate over all the numbers accepted by the game
                for number in self.list_numbers:
                    # Once, a valid value is found write it in the grid
                    if self.is_valid(number, row, col):
                        self.grid[row][col] = number
                        # Create and update the window
                        self.screen.fill((255, 255, 255))
                        self.draw()
                        self.pos_x = col
                        self.pos_y = row
                        self.draw_box()
                        pygame.display.update()
                        # Leave a delay to visualise the algorithm execution
                        pygame.time.delay(20)
                        # If the sudoku is finished return True
                        if 0 not in self.grid:
                            return True
                        # Try to solve the sudoku starting from the last number added
                        elif self.solve():
                            return True
                # If there is no solution from the last change, empty the cell modified and exit from the cycle
                self.grid[row][col] = 0
                break
        # If the sudoku cannot be solved return False
        return False

    def fast_solve(self):
        """
        Solves the sudoku in a faster way counting also the times the puzzle can be completed.

        :return: True when completed, False if no solution is possible.
        """
        # Iterate over each cell in the grid
        for i in range(self.n_cells):
            row = i // self.side
            col = i % self.side
            # Find the next empty cell
            if self.grid[row][col] == 0:
                # Iterate over all the numbers accepted by the game
                for number in self.list_numbers:
                    # Once, a valid value is found write it in the grid
                    if self.is_valid(number, row, col):
                        self.grid[row][col] = number
                        # If the sudoku is finished increase the counter and keep going
                        if 0 not in self.grid:
                            self.counter += 1
                            # If more than one solution has been found return True
                            if self.counter > 1:
                                return True
                            break
                        # Try to solve the sudoku starting from the last number added
                        elif self.fast_solve():
                            return True
                # If there is no solution from the last change, empty the cell modified and exit from the cycle
                self.grid[row][col] = 0
                break
        # If the sudoku cannot be solved return False
        return False

    def insert_sure_numbers(self):
        """
        Works with the cells in the sudoku where there is only one valid number that can be inserted.
        """
        # Iterate over all the numbers accepted by the game
        for i in range(self.n_cells):
            row = i // self.side
            col = i % self.side
            # Find the next empty cell
            if self.grid[row][col] == 0:
                # Get all the numbers that can be inserted in the empty cell
                valid_numbers = [number for number in self.list_numbers if self.is_valid(number, row, col)]
                # If only one number is valid in that position
                if len(valid_numbers) == 1:
                    print(f'ROW: {row + 1} - COL: {col + 1} - VALUE: {valid_numbers}')
                    # Insert the value in the grid
                    self.grid[row][col] = valid_numbers[0]
                    # Update window and the selection of the cell
                    self.screen.fill((255, 255, 255))
                    self.draw()
                    self.pos_x = col
                    self.pos_y = row
                    self.draw_box()
                    pygame.display.update()
                    pygame.time.delay(20)
                    # Re-execute the function again from the beginning
                    self.insert_sure_numbers()

    def fast_insert_sure_numbers(self):
        """
        Works in a rapid manner with the cells in the sudoku where there is only one valid number that can be inserted.
        """
        # Iterate over all the numbers accepted by the game
        for i in range(self.n_cells):
            row = i // self.side
            col = i % self.side
            # Find the next empty cell
            if self.grid[row][col] == 0:
                # Get all the numbers that can be inserted in the empty cell
                valid_numbers = [number for number in self.list_numbers if self.is_valid(number, row, col)]
                # If only one number is valid in that position
                if len(valid_numbers) == 1:
                    # Insert the value in the grid
                    self.grid[row][col] = valid_numbers[0]
                    # Re-execute the function again from the beginning
                    self.fast_insert_sure_numbers()
