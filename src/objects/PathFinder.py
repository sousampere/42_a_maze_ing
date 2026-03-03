

from typing import Any

from src import Maze


class PathFinder():
    @staticmethod
    def find_path(maze: Any) -> Any:
        if maze is None:
            return ''
        entry_x, entry_y = \
            maze.config.entry_coords['x'], maze.config.entry_coords['y']
        exit_x, exit_y = \
            maze.config.exit_coords['x'], maze.config.exit_coords['y']

        previous_cells: list[dict[str, Any]] = []
        previous_cells.append({
            'coords': {'x': entry_x, 'y': entry_y},
            'history': '',
            })
        absolute_cell_history = []

        # Loop until path found
        while (True):
            new_previous_cells = []
            for cell in previous_cells:
                neighbours_cells = PathFinder.get_neighbours_open_cells(
                    maze, cell['coords']['x'], cell['coords']['y'])
                for neighbour in neighbours_cells:
                    direction = ''
                    match neighbour['direction']:
                        case 'east':
                            direction = 'E'
                        case 'north':
                            direction = 'N'
                        case 'south':
                            direction = 'S'
                        case 'west':
                            direction = 'W'
                    add_cell = True
                    if (add_cell and len(cell['history']) > 0):
                        add_cell = False if cell['history'][-1] == 'E' \
                            and direction == 'W' else True
                    if (add_cell and len(cell['history']) > 0):
                        add_cell = False if cell['history'][-1] == 'W' \
                            and direction == 'E' else True
                    if (add_cell and len(cell['history']) > 0):
                        add_cell = False if cell['history'][-1] == 'S' \
                            and direction == 'N' else True
                    if (add_cell and len(cell['history']) > 0):
                        add_cell = False if cell['history'][-1] == 'N' \
                            and direction == 'S' else True
                    if add_cell:
                        if {'x': neighbour['x'], 'y': neighbour['y']}\
                           not in absolute_cell_history:
                            new_previous_cells.append({
                                'coords': {'x': neighbour['x'],
                                           'y': neighbour['y']},
                                'history': cell['history'] + direction
                            })

            for cell in new_previous_cells:
                if (cell['coords']['x'] == exit_x
                   and cell['coords']['y'] == exit_y):
                    maze.shortest_path = cell['history']
                    return cell['history']
            for cell in previous_cells:
                absolute_cell_history.append(cell['coords'])
            previous_cells = new_previous_cells

    @staticmethod
    def get_neighbours_open_cells(maze: Maze, x: int, y: int) ->\
            list[dict[str, Any]]:
        """ Return the cells open around the given coords """
        neighbours_cells = []
        # East
        try:
            if (x + 1 != maze.config.width
                    and maze.cells[y][x].directions()['east'] != 1):
                neighbours_cells.append({'x': x + 1, 'y': y,
                                         'direction': 'east'})
        except Exception:
            pass

        # West
        try:
            if (x - 1 != -1 and maze.cells[y][x].directions()['west'] != 1):
                neighbours_cells.append({'x': x - 1, 'y': y,
                                         'direction': 'west'})
        except Exception:
            pass

        # South
        try:
            if (y + 1 != maze.config.height
               and maze.cells[y][x].directions()['south'] != 1):
                neighbours_cells.append({'x': x, 'y': y + 1,
                                         'direction': 'south'})
        except Exception:
            pass

        # North
        try:
            if (y - 1 != -1 and maze.cells[y][x].directions()['north'] != 1):
                neighbours_cells.append({'x': x, 'y': y - 1,
                                         'direction': 'north'})
        except Exception:
            pass

        return neighbours_cells
