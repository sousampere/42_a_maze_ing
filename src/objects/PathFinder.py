
from traceback import print_tb

from src import Maze

class PathFinder():
    @staticmethod
    def find_path(maze: Maze):
        entry_x, entry_y = maze.config.entry_coords['x'], maze.config.entry_coords['y']
        exit_x, exit_y = maze.config.exit_coords['x'], maze.config.exit_coords['y']

        previous_cells = []
        previous_cells.append({
            'coords': {'x': entry_x, 'y': entry_y},
            'history': '',
            })
        
        # Loop until path found
        while (True):
            new_previous_cells = []
            for cell in previous_cells:
                neighbours_cells = maze.get_neighbours_open_cells(cell['coords']['x'], cell['coords']['y'])
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
                        add_cell = False if cell['history'][-1] == 'E' and direction == 'W' else True
                    if (add_cell and len(cell['history']) > 0):
                        add_cell = False if cell['history'][-1] == 'W' and direction == 'E' else True
                    if (add_cell and len(cell['history']) > 0):
                        add_cell = False if cell['history'][-1] == 'S' and direction == 'N' else True
                    if (add_cell and len(cell['history']) > 0):
                        add_cell = False if cell['history'][-1] == 'N' and direction == 'S' else True
                    if add_cell:
                        new_previous_cells.append({
                            'coords': {'x': neighbour['x'], 'y': neighbour['y']},
                            'history': cell['history'] + direction
                        })
            for cell in new_previous_cells:
                if (cell['coords']['x'] == exit_x and cell['coords']['y'] == exit_y):
                    return cell['history']
            previous_cells = new_previous_cells
