#!/usr/bin/python3


import random
import time
import sys
from pynput import keyboard  # type: ignore[import-untyped]
from itertools import cycle
from termios import TCIFLUSH, tcflush

from src import Cell
from src.parsing import Config, get_parsed_config
from src.misc.arguments import get_args
from typing import Any
import math


class Maze():
    """ Maze object, containing dimensions, cells, etc. """
    def __init__(self, config: Config) -> None:
        self._width = config.width
        self._height = config.height
        self.cells: list[list[Cell]] = []
        self.setup_cells()
        self.config = config
        self.control = Controller()
        self.control.start_listener()
        self.shortest_path = ''

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

        # Security if the 2 is touching the border: return nothing
        if (x + 4 >= self.config.width):
            return (self.get_protected_cells(x + 1, y))

        return protected_cells

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
            f.write(self.shortest_path)
        return None

    def make_maze_perfect(self, flag: bool) -> None:
        if flag is False:
            full_maze_done = False
            breakable_walls: list[dict[str, Any]] = []
            while not full_maze_done:
                y_pos = 0
                x_pos = 0
                for lines in self.cells:
                    for cells in lines:
                        if (x_pos >= 0 and x_pos < self.config.width - 1
                           and y_pos >= 1 and y_pos < self.config.height - 1):
                            # Vertical break
                            if (self.cells[y_pos][x_pos].directions()
                                ['east'] == 1
                                and self.cells[y_pos - 1][x_pos].directions()
                                ['east'] == 1
                                and self.cells
                                [y_pos + 1][x_pos].directions()['east'] == 1
                                and not self.is_protected_cell
                                (x_pos + 1, y_pos)
                                and not self.is_protected_cell
                                    (x_pos, y_pos)):
                                breakable_walls.append({'x': x_pos, 'y': y_pos,
                                                        'direction': 'east'})
                                # self.break_wall(x_pos, y_pos, 'east')
                                # print('breaking wall vertical')
                        if (x_pos >= 1 and x_pos < self.config.width - 1
                            and y_pos >= 0 and y_pos <
                                self.config.height - 1):
                            # Horizontal break
                            if (self.cells[y_pos][x_pos].directions()
                                ['south'] == 1
                                and self.cells[y_pos][x_pos - 1].directions()
                                ['south'] == 1
                                and self.cells[y_pos][x_pos + 1].directions()
                                ['south'] == 1
                                and not self.is_protected_cell
                                (x_pos, y_pos + 1)
                                and not self.is_protected_cell
                                    (x_pos, y_pos)):
                                breakable_walls.append({'x': x_pos,
                                                        'y': y_pos,
                                                        'direction': 'south'})
                                # self.break_wall(x_pos, y_pos, 'south')
                                # print('breaking wall hor')
                        x_pos += 1
                    y_pos += 1
                    x_pos = 0
                full_maze_done = True
            for wall in random.choices(breakable_walls,
                                       k=(1 + int(math.sqrt
                                                  (self.config.width
                                                   + self.config.height)))):
                self.break_wall(wall['x'], wall['y'], wall['direction'])


class MazeVisualizer():
    def visualize(maze: Maze) -> None:
        time.sleep(maze.control.speed)
        print("\033[H\033[J", end="")
        buffer = ""
        if maze.control.stop is True:
            return
        y = 0
        x = 0
        for line in maze.cells:
            line_1 = ""
            line_2 = ""
            line_3 = ""
            for char in line:
                l_1, l_2, l_3 = "", "", ""
                if (x == maze.config.entry_coords['x']
                   and y == maze.config.entry_coords['y']):
                    center_char = '🏠'
                elif (x == maze.config.exit_coords['x']
                      and y == maze.config.exit_coords['y']):
                    center_char = '🚀'
                else:
                    center_char = '  '
                match char.get_hex_value():
                    case "0":
                        l_1, l_2, l_3 = \
                            "      ", f"  {center_char}  ", "      "
                    case "1":
                        l_1, l_2, l_3 = \
                            "▔▔▔▔▔▔", f"  {center_char}  ", "      "
                    case "2":
                        l_1, l_2, l_3 = \
                            "     ▕", f"  {center_char} ▕", "     ▕"
                    case "3":
                        l_1, l_2, l_3 = \
                            "▔▔▔▔▔🭾", f"  {center_char} ▕", "     ▕"
                    case "4":
                        l_1, l_2, l_3 = \
                            "      ", f"  {center_char}  ", "▁▁▁▁▁▁"
                    case "5":
                        l_1, l_2, l_3 = \
                            "▔▔▔▔▔▔", f"  {center_char}  ", "▁▁▁▁▁▁"
                    case "6":
                        l_1, l_2, l_3 = \
                            "     ▕", f"  {center_char} ▕", "▁▁▁▁▁🭿"
                    case "7":
                        l_1, l_2, l_3 = \
                            "▔▔▔▔▔🭾", f"  {center_char} ▕", "▁▁▁▁▁🭿"
                    case "8":
                        l_1, l_2, l_3 = \
                            "▏     ", f"▏ {center_char}  ", "▏     "
                    case "9":
                        l_1, l_2, l_3 = \
                            "🭽▔▔▔▔▔", f"▏ {center_char}  ", "▏     "
                    case "A":
                        l_1, l_2, l_3 = \
                            "▏    ▕", f"▏ {center_char} ▕", "▏    ▕"
                    case "B":
                        l_1, l_2, l_3 = \
                            "🭽▔▔▔▔🭾", f"▏ {center_char} ▕", "▏    ▕"
                    case "C":
                        l_1, l_2, l_3 = \
                            "▏     ", f"▏ {center_char}  ", "🭼▁▁▁▁▁"
                    case "D":
                        l_1, l_2, l_3 = \
                            "🭽▔▔▔▔▔", f"▏ {center_char}  ", "🭼▁▁▁▁▁"
                    case "E":
                        l_1, l_2, l_3 = \
                            "▏    ▕", f"▏ {center_char} ▕", "🭼▁▁▁▁🭿"
                    case "F":
                        # l_1, l_2, l_3 = "🭽▔▔▔▔🭾", "▏ 🟧 ▕", "🭼▁▁▁▁🭿"
                        l_1, l_2, l_3 = f"{maze.control.color}██████"\
                                        f"{maze.control.color}", \
                                        f"{maze.control.color}██████"\
                                        f"{maze.control.color}", \
                                        f"{maze.control.color}██████"\
                                        f"{maze.control.color}"
                line_1 += l_1
                line_2 += l_2
                line_3 += l_3
                x += 1
            x = 0
            y += 1
            buffer += line_1 + "\n"
            buffer += line_2 + "\n"
            buffer += line_3 + "\n"
            # print(f"\033[0;36m{line_1}\033[0;0m")
            # print(f"\033[0;36m{line_2}\033[0;0m")
        print(f"{maze.control.color}{buffer}\033[0;0m")
        tcflush(sys.stdin.fileno(), TCIFLUSH)


class MazeGenerator():
    def __init__(self, flag):
        self.visulalize = flag
        self.maze = None

    def generate(self, maze: Maze) -> None:
        maze.control.stop = False
        x = maze.config.entry_coords['x']
        y = maze.config.entry_coords['y']
        origin_x = x
        origin_y = y

        available_cells = maze.get_neighbours_cells(x, y)
        random_cell = random.choice(available_cells)
        maze.break_wall(x, y, random_cell['direction'])
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
            while (len(maze.get_neighbours_cells(x, y)) != 0):
                stack.append({'x': x, 'y': y})
                available_cells = maze.get_neighbours_cells(x, y)
                random_cell = random.choice(available_cells)
                maze.break_wall(x, y, random_cell['direction'])
                x = random_cell['x']
                y = random_cell['y']
                stack.append({'x': x, 'y': y})
                if self.visulalize is True:
                    MazeVisualizer.visualize(maze)
                if maze.control.stop is True:
                    maze.__dict__.update(self.new_maze().__dict__)
                    self.maze = maze
                    return None
                while maze.control.pause is True:
                    value = input("[PAUSED] - Press ENTER to continue...")
                    if value == '':
                        maze.control.pause = False
        if self.visulalize is True:
            MazeVisualizer.visualize(maze)
        self.maze = maze
        return None

    def get_generated_maze(self):
        return self.maze

    def get_solution(self):
        from src import PathFinder
        return PathFinder.find_path(self.maze)

    def new_maze(self) -> Maze:
        args = get_args()

        config = get_parsed_config(args['config'])
        maze = Maze(config)
        MazeGenerator(self.visulalize).generate(maze)
        return maze


class Controller():
    def __init__(self):
        self.listener = keyboard.Listener(on_press=self._on_press)
        self.speed = 0.1
        self.colors = ['\033[0;31m',
                       '\033[1;32m',
                       '\033[1;33m',
                       '\033[1;35m',
                       '\033[0;35m',
                       '\033[0;34m',
                       '\033[0;36m']
        self.color_cycle = cycle(self.colors)
        self.color = self.colors[6]
        self.stop = False
        self.pause = False

    def _on_press(self, key: Any) -> None:
        try:
            if key.char == "+":
                self.speed = max(0.03, self.speed - 0.01)
            elif key.char == "-":
                self.speed = min(0.8, self.speed + 0.01)
            elif key.char == "c":
                self.color = next(self.color_cycle)
            elif key.char == "r":
                self.stop = True
            elif key.char == "p":
                self.pause = True
        except AttributeError:
            pass

    def start_listener(self) -> None:
        self.listener.start()

    def stop_listener(self) -> None:
        self.listener.stop()
