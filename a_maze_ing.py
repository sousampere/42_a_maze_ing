#!/usr/bin/python3

from src import Maze, get_parsed_config, PathFinder
from src import get_args
from src.misc.constants import Colors
import sys
from src.parsing import ConfigError, ParsingError
from pydantic import ValidationError
from termios import TCIFLUSH, tcflush


def main() -> None:
    """Main script:
    - Parsing
    - Maze setup
    - Maze visualization
    - Path finding
    - Result output
    """
    # Arguments setup
    args = get_args()

    # Configuration Parsing
    try:
        config = get_parsed_config(args['config'])
    except (ConfigError, ParsingError) as e:
        print(f'{Colors.RED}{e}{Colors.END}', file=sys.stderr)
        exit(0)
    except ValidationError as e:
        print(f'{Colors.RED}Configuration error for {e.errors()[0]['loc'][0]}:'
              f' {e.errors()[0]['msg']}, got {e.errors()[0]['input']}.'
              f'{Colors.END}', file=sys.stderr)
        exit(0)

    # Maze initialization
    maze = Maze(config)
    maze.generate()  # Generate holes in the filled maze
    maze.make_maze_perfect(maze.config.perfect)  # Generate a non-perfect

    # Visualizing final maze
    maze.visualize()

    # Path-finder
    path_finder = PathFinder()
    path_finder.find_path(maze)

    # Emptying key-control buffer
    tcflush(sys.stdin.fileno(), TCIFLUSH)

    # Display error message if needed
    if len(maze.get_protected_cells()) == 0:
        print(f'{Colors.RED}Your configuration made displaying '
              f'the 42 pattern impossible.{Colors.END}', file=sys.stderr)
    
    # Output data
    try:
        maze.output_maze(maze.output)
    except PermissionError:
        print(f'{Colors.RED}Could not open your output file: '
              f'no permissions.{Colors.END}', file=sys.stderr)
    except Exception as e:
        print(f'{Colors.RED}Could write the output: '
              f'{e}.{Colors.END}', file=sys.stderr)
        exit(1)

    exit(0)


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f'{Colors.RED}An error occured: '
              f'{e}{Colors.END}', file=sys.stderr)
        exit(0)
