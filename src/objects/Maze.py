#!/usr/bin/python3


from src import Cell
from src.parsing import Config
from src.misc.functions import debug


#   N
# W< >E
#   S

class Maze():
    """ Maze object, containing dimensions, cells, etc. """
    def __init__(self, config: Config) -> None:
        self._width = config.width
        self._height = config.height
        self.cells = []
        self.setup_cells()

    def setup_cells(self):
        # Adding cell to the maze
        for y in range(self._height):
            current_line = []
            for x in range(self._width):
                # Top left corner
                if x == 0 and y == 0:
                    current_line.append(Cell(north=1, west=1, south=0, east=0))

                # Top right corner
                elif x == self._width - 1 and y == 0:
                    current_line.append(Cell(north=1, west=0, south=0, east=1))

                # Bottom left corner
                elif x == 0 and y == self._height - 1:
                    current_line.append(Cell(north=0, west=1, south=1, east=0))

                # Bottom right corner
                elif x == self._width - 1 and y == self._height - 1:
                    current_line.append(Cell(north=0, west=0, south=1, east=1))

                # Top
                elif y == 0:
                    current_line.append(Cell(north=1, west=0, south=0, east=0))

                # Bottom
                elif y == self._height - 1:
                    current_line.append(Cell(north=0, west=0, south=1, east=0))

                # Left
                elif x == 0:
                    current_line.append(Cell(north=0, west=1, south=0, east=0))

                # Right
                elif x == self._width - 1:
                    current_line.append(Cell(north=0, west=0, south=0, east=1))

                # Default (void)
                else:
                    current_line.append(Cell(0, 0, 0, 0))
                x += 1
            self.cells.append(current_line)
            y += 1

        for cell_line in self.cells:
            for cell in cell_line:
                print(cell.get_hex_value(), end='')
            print('')
