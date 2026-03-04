
from selectors import SelectorKey
from typing import Any, Generator


from mazegen import MazeVisualizer, Maze
import random
from mazegen import get_args
from mazegen import get_parsed_config
from mazegen.parsing import Config


class MazeGenerator():
    def __init__(self, config: Config, visualize: bool = True) -> None:
        self.visulalize = visualize
        self.config = config
        self.maze = Maze(self.config)

    def create_maze(self):
        random.seed(self.config.seed)
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

    def generate(self, maze: Maze) -> Generator:
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
        return None

    def get_generated_maze(self) -> Maze | None:
        return self.maze

    def get_solution(self) -> Any:
        from mazegen import PathFinder
        return PathFinder.find_path(self.maze)

    def new_maze(self) -> Maze:
        args = get_args()

        config = get_parsed_config(args['config'])
        maze = Maze(config)
        MazeGenerator(self.visulalize).generate(maze)
        return maze
