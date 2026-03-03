#!/usr/bin/python3


from src import Maze, get_parsed_config, PathFinder, Controller, \
    MazeGenerator, MazeVisualizer
from src import get_args
from src.misc.constants import Colors
import sys
from src.parsing import ConfigError, ParsingError
from pydantic import ValidationError
from termios import TCIFLUSH, tcflush


def main() -> None:
    # Getting prompt arguments
    try:
        args = get_args()
    except Exception:
        print(f'{Colors.RED}Could not get your arguments.'
              f' Please use a valid argument.{Colors.END}', file=sys.stderr)
        exit(1)

    # Config object setup
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
    except FileNotFoundError:
        print(f'{Colors.RED}Your configuration file was'
              f' not found.{Colors.END}', file=sys.stderr)
        exit(1)
    # Maze preparation
    maze = Maze(config)
    maze_generator = MazeGenerator(config.animation)
    sys.stdout.write("\033[?25l")

    # Maze generation
    maze_generator.generate(maze)
    Controller().stop_listener()  # Stop the keys listening
    # Place the cursor at the start of the terminal
    sys.stdout.write("\033[?25h")

    # Apply holes in the walls to make it unperfect
    maze.make_maze_perfect(maze.config.perfect)

    # Path finding
    PathFinder.find_path(maze)
    tcflush(sys.stdin.fileno(), TCIFLUSH)

    # Visualization with holes + shortest path
    MazeVisualizer.visualize(maze)

    # Output the maze to the output file
    try:
        maze.output_maze(config.output_file)
    except PermissionError:
        print(f'{Colors.RED}Could not open your output file: '
              f'no permissions.{Colors.END}', file=sys.stderr)
        exit(1)
    except Exception:
        print(f'{Colors.RED}Could not write your output file: '
              f'Please use a valid one.{Colors.END}', file=sys.stderr)
        exit(1)

    # Display an error message if displaying the 42 logo is impossible
    if len(maze.get_protected_cells()) == 0 and config.display_ft_pattern:
        print(f'{Colors.RED}Your configuration made displaying '
              f'the 42 pattern impossible.{Colors.END}', file=sys.stderr)

    while True:
        MazeVisualizer.visualize(maze)


if __name__ == "__main__":
    try:
        main()
        exit(0)
    except (KeyboardInterrupt):
        tcflush(sys.stdin.fileno(), TCIFLUSH)
        print('\033[H\033[J')
        print(f'{Colors.RED}Aborted a_maze_ing. See you soon :D '
              f'{Colors.END}', file=sys.stderr)
        exit(1)
    except (Exception) as e:
        print(f'{Colors.RED}Something went wrong with the maze: '
              f'{e}{Colors.END}', file=sys.stderr)
    finally:
        # Place the cursor at the start of the terminal
        sys.stdout.write("\033[?25h")
    exit(1)
