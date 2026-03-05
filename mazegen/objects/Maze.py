#!/usr/bin/python3


import random

from mazegen import Cell
from mazegen.parsing import Config
from typing import Any
import math

from mazegen.objects.Controller import Controller


class Maze():
    """ Maze object, containing dimensions, cells, etc. """
    def __init__(self, config: Config) -> None:
        self._width = config.width
        self._height = config.height
        self.cells: list[list[Cell]] = []
        self.setup_cells()
        self.config = config
        self.control = Controller(self.config)
        self.control.start_listener()
        self.shortest_path = ''

    def setup_cells(self) -> None:
        """ Setup the cells of the maze as F cells """
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
        """Return the neighbours cells around the current x,y cell

        Returns:
            list: cells around the current cell
        """
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
        """ Know if a particular cell (x,y) is protected or not """
        for cell in self.get_protected_cells():
            if cell['x'] == x and cell['y'] == y:
                return True
        return False

    def break_wall(self, x: int, y: int, wall: str) -> None:
        """Break a wall of the current cell if possible

        Args:
            x (int): cell x coord
            y (int): cell y coord
            wall (str): direction (north, south, ...)
        """
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
        """Output the maze in the give file

        Args:
            output_file (str): file to output to

        Returns:
            None: None
        """
        from mazegen import PathFinder
        PathFinder.find_path(self)
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
            f.write('\n')
        return None

    def make_maze_perfect(self, flag: bool) -> None:
        """ Break random walls in the maze if flag is false """
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
                x = self.config.entry_coords['x']
                y = self.config.entry_coords['y']
                if (self.cells[y][x].directions()['east'])\
                        and x + 1 != self.config.width:
                    breakable_walls.append({'x': x, 'y': y,
                                            'direction': 'east'})
                if (self.cells[y][x].directions()['north']) and y - 1 != -1:
                    breakable_walls.append({'x': x, 'y': y,
                                            'direction': 'north'})
                if (self.cells[y][x].directions()['west']) and x - 1 != -1:
                    breakable_walls.append({'x': x, 'y': y,
                                            'direction': 'west'})
                if (self.cells[y][x].directions()['south'])\
                        and y + 1 != self.config.height:
                    breakable_walls.append({'x': x, 'y': y,
                                            'direction': 'south'})
            for wall in random.choices(breakable_walls,
                                       k=(1 + int(math.sqrt
                                                  (self.config.width
                                                   + self.config.height)))):
                self.break_wall(wall['x'], wall['y'], wall['direction'])

    def get_path_cells(self) -> list[dict[str, Any]]:
        """ Return a list of cells that are on the
         shortest possible path from the pathfinding. """
        path_cells = []
        x = self.config.entry_coords['x']
        y = self.config.entry_coords['y']
        for char in range(len(self.shortest_path) - 1):
            if self.shortest_path[char] == 'S':
                y += 1
            if self.shortest_path[char] == 'N':
                y -= 1
            if self.shortest_path[char] == 'E':
                x += 1
            if self.shortest_path[char] == 'W':
                x -= 1

            if self.shortest_path[char + 1] == 'S':
                emoji = ' ↓'
            if self.shortest_path[char + 1] == 'N':
                emoji = ' ↑'
            if self.shortest_path[char + 1] == 'E':
                emoji = ' →'
            if self.shortest_path[char + 1] == 'W':
                emoji = ' ←'

            path_cells.append({'x': x,
                               'y': y,
                               'emoji': emoji})
        return path_cells

    def is_path_cell(self, x: int, y: int) -> dict[str, str | bool | None]:
        """ Return True if a cell is on the shortest path possible,
         according to the cell's coordinates x and y """
        for cell in self.get_path_cells():
            if cell['x'] == x and cell['y'] == y:
                return {'status': True, 'emoji': cell['emoji']}
        return {'status': False, 'emoji': None}
