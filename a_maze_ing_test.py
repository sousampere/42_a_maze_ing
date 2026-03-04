#!/usr/bin/python3


from mazegen import Maze, get_parsed_config, PathFinder, Controller, \
    MazeGenerator, MazeVisualizer
from mazegen import get_args
from mazegen.misc.constants import Colors
import sys
from mazegen.parsing import Config, ConfigError, ParsingError
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
    config = Config(width=10,
                    height=10,
                    entry_coords={'x': 0, 'y': 0},
                    exit_coords={'x': 9, 'y': 9},
                    output_file='maze.txt',
                    perfect=True,
                    seed='TOURDIAT',
                    animation=True,
                    show_path=True,
                    display_ft_pattern=True)
    generator = MazeGenerator(config)

    generator.create_maze()

    def animate_maze():
        for maze in generator.generate_existing_maze(yield_maze=True):
            MazeVisualizer.visualize(maze)
            if maze.control.stop is True:
                generator.create_maze()
                animate_maze()
                break
            while maze.control.pause is True:
                value = input("[PAUSED] - Press ENTER to continue...")
                if value == '':
                    maze.control.pause = False
        generator.get_generated_maze().output_maze(config.output_file)
        generator.get_generated_maze().control.stop_listener()

    if (config.animation):
        animate_maze()
    else:
        list(generator.generate_existing_maze())

    if (config.show_path):
        PathFinder.find_path(generator.maze)
    MazeVisualizer.visualize(generator.get_generated_maze())
