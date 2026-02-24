#!/usr/bin/python3


from turtle import width

from src import Cell
from src.parsing import Config


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


    def apply_forty_two(self) -> None:
        """ Add the 42 logo in the center """
        if (self._width >= 9 and self._height >= 6):
            for cell in self.get_protected_cells():
                self.cells[cell['y']][cell['x']] = Cell(1,1,1,1)

    def get_protected_cells(self) -> list[dict[str, int]]:
        """ Return the cells of the 42 logo """
        center_x = int(self._width / 2)
        center_y = int(self._height / 2)
        protected_cells = []

        if (self._width % 2 == 0):
            center_x -= 1

        # Number 4
        protected_cells.append({'x': center_x - 1, 'y': center_y})
        protected_cells.append({'x': center_x - 2, 'y': center_y})
        protected_cells.append({'x': center_x - 3, 'y': center_y})
        protected_cells.append({'x': center_x - 3, 'y': center_y - 1})
        protected_cells.append({'x': center_x - 3, 'y': center_y - 2})
        protected_cells.append({'x': center_x - 1, 'y': center_y})
        protected_cells.append({'x': center_x - 1, 'y': center_y + 1})
        protected_cells.append({'x': center_x - 1, 'y': center_y + 2})

        if (self._width % 2 == 0):
            center_x += 1

        # Number 2
        protected_cells.append({'x': center_x + 1, 'y': center_y})
        protected_cells.append({'x': center_x + 2, 'y': center_y})
        protected_cells.append({'x': center_x + 3, 'y': center_y})
        protected_cells.append({'x': center_x + 3, 'y': center_y - 1})
        protected_cells.append({'x': center_x + 3, 'y': center_y - 2})
        protected_cells.append({'x': center_x + 1, 'y': center_y - 2})
        protected_cells.append({'x': center_x + 2, 'y': center_y - 2})
        protected_cells.append({'x': center_x + 1, 'y': center_y + 1})
        protected_cells.append({'x': center_x + 1, 'y': center_y + 2 })
        protected_cells.append({'x': center_x + 2, 'y': center_y + 2})
        protected_cells.append({'x': center_x + 3, 'y': center_y + 2})

        return protected_cells

    def debug(self):
        for cell_line in self.cells:
            for cell in cell_line:
                print(cell.get_hex_value(), end='')
            print('')

    def visualize(self):
        for line in self.cells:
            line_1 = ""
            line_2 = ""
            line_3 = ""
            for char in line:
                l_1, l_2, l_3 = "", "", ""
                match char.get_hex_value():
                    case "0":
                        l_1, l_2, l_3 = "      ", "      ", "      "
                    case "1":
                        l_1, l_2, l_3 = "▔▔▔▔▔▔", "      ", "      "
                    case "2":
                        l_1, l_2, l_3 = "     ▕", "     ▕", "     ▕"
                    case "3":
                        l_1, l_2, l_3 = "▔▔▔▔▔🭾", "     ▕", "     ▕"
                    case "4":
                        l_1, l_2, l_3 = "      ", "      ", "▁▁▁▁▁▁"
                    case "5":
                        l_1, l_2, l_3 = "▔▔▔▔▔▔", "      ", "▁▁▁▁▁▁"
                    case "6":
                        l_1, l_2, l_3 = "     ▕", "     ▕", "▁▁▁▁▁🭿"
                    case "7":
                        l_1, l_2, l_3 = "▔▔▔▔▔🭾", "     ▕", "▁▁▁▁▁🭿"
                    case "8":
                        l_1, l_2, l_3 = "▏     ", "▏     ", "▏     "
                    case "9":
                        l_1, l_2, l_3 = "🭽▔▔▔▔▔", "▏     ", "▏     "
                    case "A":
                        l_1, l_2, l_3 = "▏    ▕", "▏    ▕", "▏    ▕"
                    case "B":
                        l_1, l_2, l_3 = "🭽▔▔▔▔🭾", "▏    ▕", "▏    ▕"
                    case "C":
                        l_1, l_2, l_3 = "▏     ", "▏     ", "🭼▁▁▁▁▁"
                    case "D":
                        l_1, l_2, l_3 = "🭽▔▔▔▔▔", "▏     ", "🭼▁▁▁▁▁"
                    case "E":
                        l_1, l_2, l_3 = "▏    ▕", "▏    ▕", "🭼▁▁▁▁🭿"
                    case "F":
                        l_1, l_2, l_3 = "🭽▔▔▔▔🭾", "▏ 🟧 ▕", "🭼▁▁▁▁🭿"

                line_1 += l_1
                line_2 += l_2
                line_3 += l_3
            print(f"\033[0;36m{line_1}\033[00;0m")
            print(f"\033[0;36m{line_2}\033[00;0m")
            print(f"\033[0;36m{line_3}\033[00;0m")