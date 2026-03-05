#!/usr/bin/python3


from mazegen import get_parsed_config, PathFinder, \
    MazeGenerator, MazeVisualizer
from mazegen import get_args
from mazegen.misc.constants import Colors
import sys
from mazegen.parsing import ConfigError, ParsingError
from pydantic import ValidationError
from termios import TCIFLUSH, tcflush


def main() -> None:
    """Main execution script :
    - parsing
    - maze generation
    - visualization
    - output
    """
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
    except Exception:
        print(f'{Colors.RED}Error in configurating your project.'
              f'{Colors.END}', file=sys.stderr)
        exit(1)

    # Maze preparation
    generator = MazeGenerator(config)
    generator.create_maze()

    # Maze generation
    try:
        def animate_maze() -> None:
            for maze in generator.generate_existing_maze(yield_maze=True):
                MazeVisualizer.visualize(maze)
                if maze.control.stop is True:
                    generator.maze.control.stop_listener()
                    generator.create_maze()
                    animate_maze()
                    break
                while maze.control.pause is True:
                    value = input("[PAUSED] - Press ENTER to continue...")
                    if value == '':
                        maze.control.pause = False
            generator.maze.output_maze(config.output_file)
        if (config.animation):
            animate_maze()
        else:
            list(generator.generate_existing_maze())  # Execute the yield funct
    except Exception:
        print(f'{Colors.RED}Could not generate the maze.'
              f'{Colors.END}', file=sys.stderr)

    generator.maze.make_maze_perfect(generator.maze.config.perfect)

    # Output the maze to the output file
    try:
        generator.maze.output_maze(config.output_file)
    except PermissionError:
        print(f'{Colors.RED}Could not open your output file: '
              f'no permissions.{Colors.END}', file=sys.stderr)
        exit(1)
    except Exception:
        print(f'{Colors.RED}Could not write your output file: '
              f'Please use a valid one.{Colors.END}', file=sys.stderr)
        exit(1)

    try:
        while (True):
            PathFinder.find_path(generator.maze)
            MazeVisualizer.visualize(generator.maze)
            if generator.maze.control.stop is True:
                generator.maze.control.stop_listener()
                generator.create_maze()
                if (config.animation):
                    animate_maze()
                else:
                    list(generator.generate_existing_maze())
                generator.maze.make_maze_perfect(generator.maze.config.perfect)
                generator.maze.output_maze(config.output_file)
            # Display an error message if displaying the 42 logo is impossible
            if len(generator.maze.get_protected_cells()) == 0\
                    and config.display_ft_pattern:
                print(f'{Colors.RED}Your configuration made displaying '
                      f'the 42 pattern impossible.{Colors.END}',
                      file=sys.stderr)
    except (KeyboardInterrupt):
        print("", end="\r")
        print(f'{Colors.GREEN}Ended a_maze_ing. See you soon :D '
              f'{Colors.END}', file=sys.stderr)
    finally:
        generator.maze.control.stop_listener()


if __name__ == "__main__":
    try:
        main()
        exit(0)
    except (KeyboardInterrupt):
        tcflush(sys.stdin.fileno(), TCIFLUSH)
        print('\033[H\033[J')
        print(f'{Colors.GREEN}Ended a_maze_ing. See you soon :D '
              f'{Colors.END}', file=sys.stderr)
        exit(0)
    except Exception as e:
        print(f'{Colors.RED}Could not create the maze: '
              f'{e}.{Colors.END}', file=sys.stderr)
        exit(1)
