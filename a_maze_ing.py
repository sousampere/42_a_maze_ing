#!/usr/bin/python3


from src import Maze, get_parsed_config
from src import get_args
from src import debug


def main() -> None:
    print("Hello from a-maze-ing!")


if __name__ == "__main__":
    args = get_args()
    debug(args)

    config = get_parsed_config(args['config'])
    maze = Maze(config)
    # maze.debug()
    debug(maze)
    # maze.apply_forty_two()
    # maze.fill_cells()
    # maze.break_wall(0, 0, 'east')
    maze.generate()

    maze.visualize()
    maze.output_maze('output_maze.txt')
    print(maze.config)
    import sys
    main()
