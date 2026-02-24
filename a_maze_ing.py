#!/usr/bin/python3


from src import Maze, get_parsed_config
from src import get_args
from src import debug


def main():
    print("Hello from a-maze-ing!")


if __name__ == "__main__":
    args = get_args()
    debug(args)

    config = get_parsed_config(args['config'])
    maze = Maze(config)
    maze.debug()
    maze.apply_forty_two()
    maze.visualize()
    main()
