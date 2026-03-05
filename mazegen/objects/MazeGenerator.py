from mazegen import Maze
import random
from mazegen.parsing import Config


class MazeGenerator():
    def __init__(self, config: Config, visualize: bool = True) -> None:
        self.visulalize = visualize
        self.config = config
        self.maze = Maze(self.config)

    def create_maze(self):
        self.maze = Maze(self.config)
        return None

    def generate_existing_maze(self, yield_maze: bool = False):
        x = self.maze.config.entry_coords['x']
        y = self.maze.config.entry_coords['y']
        origin_x = x
        origin_y = y

        available_cells = self.maze.get_neighbours_cells(x, y)
        random_cell = random.choice(available_cells)
        self.maze.break_wall(x, y, random_cell['direction'])
        x = random_cell['x']
        y = random_cell['y']
        stack = []
        stack.append({'x': x, 'y': y})
        while ([origin_x, origin_y] != [x, y] and len(stack) != 0):

            # While there are cells to visit
            x = stack[-1]['x']
            y = stack[-1]['y']
            stack.pop()
            while (len(self.maze.get_neighbours_cells(x, y)) != 0):
                stack.append({'x': x, 'y': y})
                available_cells = self.maze.get_neighbours_cells(x, y)
                random_cell = random.choice(available_cells)
                self.maze.break_wall(x, y, random_cell['direction'])
                x = random_cell['x']
                y = random_cell['y']
                stack.append({'x': x, 'y': y})
                if yield_maze:
                    yield self.maze
        return self.maze
