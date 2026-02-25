#!/usr/bin/python3


import random
from traceback import print_tb
from turtle import st

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
        self.config = config

    def setup_cells(self):
        # Adding cell to the maze
        for y in range(self._height):
            current_line = []
            for x in range(self._width):
                current_line.append(Cell(1, 1, 1, 1))
                x += 1
            self.cells.append(current_line)
            y += 1
    
    def get_neighbours_cells(self, x: int, y: int) -> list[dict[str, int|str]]:
        """ Return the cells around the given coords, that are breakable
         and unvisited. """
        neighbours_cells = []
        # East
        if (x + 1 != self.config.width
            and self.cells[y][x + 1].get_hex_value() == 'F'
            and not self.is_protected_cell(x + 1, y)):
            neighbours_cells.append({'x': x + 1, 'y': y, 'direction': 'east'})

        # West
        if (x - 1 != -1 and
            self.cells[y][x - 1].get_hex_value() == 'F'
            and not self.is_protected_cell(x - 1, y)):
            neighbours_cells.append({'x': x - 1, 'y': y, 'direction': 'west'})

        # South
        if (y + 1 != self.config.height and
            self.cells[y + 1][x].get_hex_value() == 'F'
            and not self.is_protected_cell(x, y + 1)):
            neighbours_cells.append({'x': x, 'y': y + 1, 'direction': 'south'})

        # North
        if (y - 1 != -1 and
            self.cells[y - 1][x].get_hex_value() == 'F'
            and not self.is_protected_cell(x, y - 1)):
            neighbours_cells.append({'x': x, 'y': y - 1, 'direction': 'north'})

        return neighbours_cells

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
    
    def is_protected_cell(self, x: int, y: int) -> bool:
        """ Know if a particular cell is protected or not """
        for cell in self.get_protected_cells():
            if cell['x'] == x and cell['y'] == y:
                return True
        return False

    def fill_cells(self):
        choices = ['0', '1', '2', '3',
                   '4', '5', '6', '7',
                   '8', '9', 'A', 'B',
                   'C', 'D', 'E',]
        random.seed(self.config.seed)

        for y in range(self._height):
            for x in range(self._width):
                if not self.is_protected_cell(x=x, y=y):
                    self.cells[y][x] = Cell.convert_hex_to_cell(random.choice(choices))
    
    def break_wall(self, x: int, y: int, wall: str) -> None:
        match wall:
            case 'north':
                self.cells[y][x].set_direction('north', 0)
                self.cells[y - 1][x].set_direction('south', 0)
            case 'east':
                self.cells[y][x].set_direction('east', 0)
                self.cells[y][x + 1].set_direction('west', 0)
            case 'south':
                self.cells[y][x].set_direction('south', 0)
                self.cells[y + 1][x].set_direction('north', 0)
            case 'west':
                self.cells[y][x].set_direction('west', 0)
                self.cells[y][x - 1].set_direction('east', 0)

    def generate(self) -> str:
        x = self.config.entry_coords['x']
        y = self.config.entry_coords['y']
        origin_x = x
        origin_y = y

        available_cells = self.get_neighbours_cells(x, y)
        random_cell = random.choice(available_cells)
        self.break_wall(x, y, random_cell['direction'])
        x = random_cell['x']
        y = random_cell['y']
        stack = []

        # print(x, y)
        # print(origin_x, origin_y)
        # self.debug()
        stack.append({'x': x, 'y': y})

        while ([origin_x, origin_y] != [x, y] and len(stack) != 0):
            # While there are cells to visit
            # print('Cells', self.get_neighbours_cells(x, y))
            x = stack[-1]['x']
            y = stack[-1]['y']
            stack.pop()
            while (len(self.get_neighbours_cells(x, y)) != 0):
                stack.append({'x': x, 'y': y})
                available_cells = self.get_neighbours_cells(x, y)
                random_cell = random.choice(available_cells)
                self.break_wall(x, y, random_cell['direction'])
                x = random_cell['x']
                y = random_cell['y']
                stack.append({'x': x, 'y': y})
