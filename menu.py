# Import packages
import pygame
import pygame_menu
from game import SudokuGame


class Menu:
    def __init__(self, ):
        # Define window settings for the menu visualization
        self.windows_size = 700
        self.screen = pygame.display.set_mode((self.windows_size, self.windows_size))
        self.menu, self.settings, self.instructions = None, None, None
        # Define variables related to the sudoku puzzle
        self.clues = 30
        self.base = 3
        self.cells = self.base ** 4
        self.unique = True
        # Initialise the menu
        self.initialise()

    def initialise(self):
        """
        Initialises the game window and menu.
        """
        pygame.init()
        # Initialisation of the Settings page
        self.settings = pygame_menu.Menu('Menu', self.windows_size, self.windows_size,
                                         theme=pygame_menu.themes.THEME_DARK)
        self.settings.add.selector('Difficulty:  ', [('Very Easy', 1), ('Easy', 2), ('Medium', 3), ('Hard', 4),
                                                     ('Extreme', 5)], onchange=self.set_difficulty, default=2)
        self.settings.add.range_slider('Base', default=3, range_values=[2, 3, 4], increment=1,
                                       onchange=self.update_base)
        self.settings.add.toggle_switch('Unique', default=1, onchange=self.update_unique)
        # Initialisation of the Instructions page
        self.instructions = pygame_menu.Menu('Menu', self.windows_size, self.windows_size,
                                             theme=pygame_menu.themes.THEME_DARK)
        HELP = "Firstly, change the difficulty and the number of cells in Settings.\n\n" \
               "Once the game starts...\n Use the mouse or the arrows to move around the grid. \n" \
               "Press a number to insert a value within a cell. \n" \
               "If it is not a valid choice, it will not be added. \n\n" \
               "Press CANC to delete a number previously added. \n" \
               "Press D to delete all the previously added values. \n" \
               "Press Q to quit the game. \n" \
               "Press ENTER to auto-solve the sudoku from the ongoing status. \n" \
               "Press P to play a new game. \n"
        self.instructions.add.label(HELP, max_char=-1, font_size=20)
        # Initialisation of the main menu page
        self.menu = pygame_menu.Menu('Menu', self.windows_size, self.windows_size, theme=pygame_menu.themes.THEME_DARK)
        self.menu.add.button('Play', self.start_the_game)
        self.menu.add.button('Instructions', self.instructions)
        self.menu.add.button('Settings', self.settings)
        self.menu.add.button('Quit', pygame_menu.events.EXIT)
        # Run the Main window
        self.menu.mainloop(self.screen)

    def update_unique(self, value):
        """
        Updates the unique value.

        :param value: new value used to update the parameter.
        """
        self.unique = value

    def update_base(self, value):
        """
        Updates the base value.

        :param value: new value used to update the parameter.
        :return:
        """
        self.base = value
        # According to the new base value update the clues and the cells parameters
        if self.base == 2:
            self.clues = 8
        elif self.base == 3:
            self.clues = 31
        elif self.base == 4:
            self.clues = 130
        self.cells = self.base ** 4

    def set_difficulty(self, _, difficulty):
        """
        Sets the clues parameter according to the new difficulty level and the current base.

        :param _: empty input, not used.
        :param difficulty: new difficulty level.
        """
        if self.base == 2:
            self.clues = 7 - difficulty
        elif self.base == 3:
            self.clues = 40 - difficulty * 3
        elif self.base == 4:
            self.clues = 140 - difficulty * 5

    def start_the_game(self):
        """
        Runs the game.
        """
        # Starts a new sudoku puzzle
        game = SudokuGame(base=self.base, clues=self.clues, unique=self.unique)
        game.play()
        # When the game ends return to the main menu loop
        self.screen = pygame.display.set_mode((self.windows_size, self.windows_size))
