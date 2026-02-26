#!/usr/bin/python3


import random
import time
import sys
from pynput import keyboard

from src import Cell
from src.parsing import Config
from typing import Any


class Maze():
    """ Maze object, containing dimensions, cells, etc. """
    def __init__(self, config: Config) -> None:
        self._width = config.width
        self._height = config.height
        self.cells: list[list[Cell]] = []
        self.setup_cells()
        self.config = config
        self.speed = 0.1
        self.listener = keyboard.Listener(on_press=self._on_press)
        self.listener.start()

    def setup_cells(self) -> None:
        # Adding cell to the maze
        for y in range(self._height):
            current_line = []
            for x in range(self._width):
                current_line.append(Cell(1, 1, 1, 1))
                x += 1
            self.cells.append(current_line)
            y += 1
        return None

    def get_neighbours_cells(self, x: int, y: int) ->\
            list[dict[str, Any]]:
        """ Return the cells around the given coords, that are breakable
         and unvisited. """
        neighbours_cells = []
        # East
        try:
            if (x + 1 != self.config.width
                and self.cells[y][x + 1].get_hex_value() == 'F'
                    and not self.is_protected_cell(x + 1, y)):
                neighbours_cells.append({'x': x + 1, 'y': y,
                                         'direction': 'east'})
        except Exception:
            pass

        # West
        try:
            if (x - 1 != -1 and
                self.cells[y][x - 1].get_hex_value() == 'F'
                    and not self.is_protected_cell(x - 1, y)):
                neighbours_cells.append({'x': x - 1, 'y': y,
                                         'direction': 'west'})
        except Exception:
            pass

        # South
        try:
            if (y + 1 != self.config.height and
                self.cells[y + 1][x].get_hex_value() == 'F'
                    and not self.is_protected_cell(x, y + 1)):
                neighbours_cells.append({'x': x, 'y': y + 1,
                                         'direction': 'south'})
        except Exception:
            pass

        # North
        try:
            if (y - 1 != -1 and
                self.cells[y - 1][x].get_hex_value() == 'F'
                    and not self.is_protected_cell(x, y - 1)):
                neighbours_cells.append({'x': x, 'y': y - 1,
                                         'direction': 'north'})
        except Exception:
            pass

        return neighbours_cells

    def get_protected_cells(self,
                            x: int = -1,
                            y: int = -1) -> list[
                                dict[str, int]]:
        """ Return the cells coords of the 42 logo """
        if (not self.config.display_ft_pattern):
            return []
        display_type = 'auto'
        if x == -1 and y == -1:
            x = int(self._width / 2)
            y = int(self._height / 2)
            display_type = 'center'
        protected_cells = []

        # Impossible to print the 42 logo with current dimensions
        if (self.config.width < 9 or self.config.height < 7):
            return []

        # Shift the number 4 to the left if it can't be centered
        if (self._width % 2 == 0 and display_type == 'center'):
            x -= 1

        if (display_type == 'auto' and x + 4 >= self.config.width):
            x = 5
            y += 1
            if (y + 4 >= self.config.height):
                return []

        # Number 4
        protected_cells.append({'x': x - 1, 'y': y})
        protected_cells.append({'x': x - 2, 'y': y})
        protected_cells.append({'x': x - 3, 'y': y})
        protected_cells.append({'x': x - 3, 'y': y - 1})
        protected_cells.append({'x': x - 3, 'y': y - 2})
        protected_cells.append({'x': x - 1, 'y': y})
        protected_cells.append({'x': x - 1, 'y': y + 1})
        protected_cells.append({'x': x - 1, 'y': y + 2})

        # Shift the number 2 to the left if it can't be centered
        if (self._width % 2 == 0 and display_type == 'center'):
            x += 1

        # Number 2
        protected_cells.append({'x': x + 1, 'y': y})
        protected_cells.append({'x': x + 2, 'y': y})
        protected_cells.append({'x': x + 3, 'y': y})
        protected_cells.append({'x': x + 3, 'y': y - 1})
        protected_cells.append({'x': x + 3, 'y': y - 2})
        protected_cells.append({'x': x + 1, 'y': y - 2})
        protected_cells.append({'x': x + 2, 'y': y - 2})
        protected_cells.append({'x': x + 1, 'y': y + 1})
        protected_cells.append({'x': x + 1, 'y': y + 2})
        protected_cells.append({'x': x + 2, 'y': y + 2})
        protected_cells.append({'x': x + 3, 'y': y + 2})

        # Retur
        if (display_type == 'auto'):
            for cell in protected_cells:
                if self.config.entry_coords == cell\
                   or self.config.exit_coords == cell:
                    return (self.get_protected_cells(x + 1, y))

        for cell in protected_cells:
            if self.config.entry_coords == cell\
               or self.config.exit_coords == cell:
                return (self.get_protected_cells(1 + 4, 1 + 4))

        return protected_cells

    def debug(self) -> None:
        for cell_line in self.cells:
            for cell in cell_line:
                print(cell.get_hex_value(), end='')
            print('')
        return None

    def _on_press(self, key):
        try:
            if key.char == "+":
                self.speed = max(0.03, self.speed - 0.01)
            elif key.char == "-":
                self.speed = min(2.0, self.speed + 0.05)
            elif key.char == "c":
                pass
        except AttributeError:
            pass

    def stop_listener(self):
        self.listener.stop()

    def visualize(self):
        print(self.speed)
        time.sleep(self.speed)
        print("\033[H\033[J", end="")
        buffer = ""
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
                        # l_1, l_2, l_3 = "🭽▔▔▔▔🭾", "▏ 🟧 ▕", "🭼▁▁▁▁🭿"
                        l_1, l_2, l_3 = "\033[0;36m██████\033[0;36m", \
                            "\033[0;36m██████\033[0;36m", \
                            "\033[0;36m██████\033[0;36m"
                line_1 += l_1
                line_2 += l_2
                line_3 += l_3
            buffer += line_1 + "\n"
            buffer += line_2 + "\n"
            buffer += line_3 + "\n"
            # print(f"\033[0;36m{line_1}\033[0;0m")
            # print(f"\033[0;36m{line_2}\033[0;0m")
        print(f"\033[0;36m{buffer}\033[0;0m")
        from termios import TCIFLUSH, tcflush
        tcflush(sys.stdin.fileno(), TCIFLUSH)

    def is_protected_cell(self, x: int, y: int) -> bool:
        """ Know if a particular cell is protected or not """
        for cell in self.get_protected_cells():
            if cell['x'] == x and cell['y'] == y:
                return True
        return False

    def fill_cells(self) -> None:
        choices = ['0', '1', '2', '3',
                   '4', '5', '6', '7',
                   '8', '9', 'A', 'B',
                   'C', 'D', 'E',]
        random.seed(self.config.seed)

        for y in range(self._height):
            for x in range(self._width):
                if not self.is_protected_cell(x=x, y=y):
                    self.cells[y][x] = \
                        Cell.convert_hex_to_cell(random.choice(choices))
        return None

    def break_wall(self, x: int, y: int, wall: str) -> None:
        match wall:
            case 'north':
                try:
                    self.cells[y][x].set_direction('north', 0)
                    self.cells[y - 1][x].set_direction('south', 0)
                except Exception:
                    pass
            case 'east':
                try:
                    self.cells[y][x].set_direction('east', 0)
                    self.cells[y][x + 1].set_direction('west', 0)
                except Exception:
                    pass
            case 'south':
                try:
                    self.cells[y][x].set_direction('south', 0)
                    self.cells[y + 1][x].set_direction('north', 0)
                except Exception:
                    pass
            case 'west':
                try:
                    self.cells[y][x].set_direction('west', 0)
                    self.cells[y][x - 1].set_direction('east', 0)
                except Exception:
                    pass

    def generate(self) -> None:
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
        return None

    def output_maze(self, output_file: str) -> None:
        """ Output the maze in a hexadecimal representation """
        with open(output_file, 'w') as f:
            for line in self.cells:
                for cell in line:
                    f.write(cell.get_hex_value())
                f.write('\n')
            f.write('\n')
            f.write(f'{self.config.entry_coords['x']},'
                    f'{self.config.entry_coords['y']}')
            f.write('\n')
            f.write(f'{self.config.exit_coords['x']},'
                    f'{self.config.exit_coords['y']}')
            f.write('\n')
            f.write('THIS IS NOT OVER ! PLEASE COMPLETE ME, '
                    'PLEASE, PLEAAAAAASE L4UR3NTG45P4RD')
        return None

