#!/usr/bin/python3

from src import Maze, get_parsed_config, PathFinder
from src import get_args
from src import debug
from src.misc.constants import Colors
import sys
from src.parsing import ConfigError, ParsingError
from pydantic import ValidationError
from termios import TCIFLUSH, tcflush


def main() -> None:
    print("Hello from a-maze-ing!")


if __name__ == "__main__":
    args = get_args()

    try:
        config = get_parsed_config(args['config'])
    except (ConfigError, ParsingError) as e:
        print(f'{Colors.RED}{e}{Colors.END}', file=sys.stderr)
        exit(1)
    except ValidationError as e:
        print(f'{Colors.RED}Configuration error for {e.errors()[0]['loc'][0]}:'
              f' {e.errors()[0]['msg']}, got {e.errors()[0]['input']}.'
              f'{Colors.END}', file=sys.stderr)
        exit(1)
    maze = Maze(config)
    debug(maze)
    maze.generate()
    maze.stop_listener()

    # maze.visualize()
    if len(maze.get_protected_cells()) == 0:
        print(f'{Colors.RED}Your configuration made displaying '
              f'the 42 pattern impossible.{Colors.END}', file=sys.stderr)
    try:
        maze.output_maze('output_maze.txt')
    except PermissionError:
        print(f'{Colors.RED}Could not open your output file: '
              f'no permissions.{Colors.END}', file=sys.stderr)

    print(maze.config)
    maze.make_maze_perfect(maze.config.perfect)
    maze.visualize()
    path_finder = PathFinder()
    print(PathFinder.find_path(maze))
    main()
    tcflush(sys.stdin.fileno(), TCIFLUSH)
    try:
        maze.output_maze('output_maze.txt')
    except PermissionError:
        print(f'{Colors.RED}Could not open your output file: '
              f'no permissions.{Colors.END}', file=sys.stderr)
