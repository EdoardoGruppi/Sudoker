
# Description of the project

[Project](https://github.com/EdoardoGruppi/Sudoker) 

This project enables to generate, play as well as automatically solve Sudoku puzzles. It provides a user-friendly Graphic User Interface from which users can select the dimension of the sudoku (4x4, 9x9 or 16x16) along with the difficulty of the game ('Very Easy', 'Easy', 'Medium', 'Difficult', 'Extreme'). Additionally, the player can decide also to generate sudoku which do not have a single solution. The main advantage related to this choice resides in a faster generation process that in particular regards the 16x16 sudoku puzzles.

The sudoku grids are created and solved exploiting the same methodology, namely the backtracking algorithm. The code intentionally showcases its functioning to enhance its understanding. During the process that automatically completes the sudoku, the backtracking algorithm is preceeds by a method finalised to fill  the empty cells in the grid that accept only a single valid number. 

## How to start

The packages required for the execution of the code along with the role of each file and the software used are described
in the Sections below.

Once all the necessary packages have been installed you can run the code by typing this line on the terminal or by means of the dedicated command on the IDE.

```
python main.py
```

Below a gif displaying how a sudoku puzzle is generated.

UPDATE gif generation

Hereafter, the functioning of the backtracking algorithm is depicted.

UPDATE gif functioning

## Packages required

A comprehensive overview of the packages needed to run the project is provided in the file [requirements.txt](https://github.com/EdoardoGruppi/Sudoker/blob/main/requirements.txt). The latter can also be directly used to install the packages by typing the specific command on the terminal. 

## Role of each file

**main.py** is the starting point of the entire project. It defines the order in which instructions are realised. 

**game.py** contains all the functions useful to set up the game and run the sudoku logic.

**menu.py** includes all the methods aimed to generate the main menu, and the setting or the instructions pages.

## Software used

> <img src="https://financesonline.com/uploads/2019/08/PyCharm_Logo1.png" width="200" alt="pycharm">

PyCharm is an integrated development environment (IDE) for Python programmers: it was chosen because it is one of the
most advanced working environments and for its ease of use.
