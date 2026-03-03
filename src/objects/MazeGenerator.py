
from src import MazeVisualizer, Maze
import random
from src import get_args
from src import get_parsed_config


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
