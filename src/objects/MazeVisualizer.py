
from termios import TCIFLUSH, tcflush
from src import Maze
import time
import sys


class MazeVisualizer():
    """ Helper class to visualize a maze """
    @staticmethod
    def visualize(maze: Maze) -> None:
        time.sleep(maze.control.speed)
        print("\033[H\033[J", end="")
        buffer = ""
        if maze.control.stop is True:
            return
        y = 0
        x = 0
        for line in maze.cells:
            line_1 = ""
            line_2 = ""
            line_3 = ""
            for char in line:
                l_1, l_2, l_3 = "", "", ""
                if (x == maze.config.entry_coords['x']
                   and y == maze.config.entry_coords['y']):
                    center_char = MazeVisualizer.theme_selector(maze, 'entry')
                elif (x == maze.config.exit_coords['x']
                      and y == maze.config.exit_coords['y']):
                    center_char = MazeVisualizer.theme_selector(maze, 'exit')
                elif (maze.config.show_path
                      and maze.is_path_cell(x, y)['status']):
                    center_char = f'\033[1;37m\
{maze.is_path_cell(x, y)['emoji']}{maze.control.color}'
                else:
                    center_char = '  '
                match char.get_hex_value():
                    case "0":
                        l_1, l_2, l_3 = \
                            "      ", f"  {center_char}  ", "      "
                    case "1":
                        l_1, l_2, l_3 = \
                            "▔▔▔▔▔▔", f"  {center_char}  ", "      "
                    case "2":
                        l_1, l_2, l_3 = \
                            "     ▕", f"  {center_char} ▕", "     ▕"
                    case "3":
                        l_1, l_2, l_3 = \
                            "▔▔▔▔▔🭾", f"  {center_char} ▕", "     ▕"
                    case "4":
                        l_1, l_2, l_3 = \
                            "      ", f"  {center_char}  ", "▁▁▁▁▁▁"
                    case "5":
                        l_1, l_2, l_3 = \
                            "▔▔▔▔▔▔", f"  {center_char}  ", "▁▁▁▁▁▁"
                    case "6":
                        l_1, l_2, l_3 = \
                            "     ▕", f"  {center_char} ▕", "▁▁▁▁▁🭿"
                    case "7":
                        l_1, l_2, l_3 = \
                            "▔▔▔▔▔🭾", f"  {center_char} ▕", "▁▁▁▁▁🭿"
                    case "8":
                        l_1, l_2, l_3 = \
                            "▏     ", f"▏ {center_char}  ", "▏     "
                    case "9":
                        l_1, l_2, l_3 = \
                            "🭽▔▔▔▔▔", f"▏ {center_char}  ", "▏     "
                    case "A":
                        l_1, l_2, l_3 = \
                            "▏    ▕", f"▏ {center_char} ▕", "▏    ▕"
                    case "B":
                        l_1, l_2, l_3 = \
                            "🭽▔▔▔▔🭾", f"▏ {center_char} ▕", "▏    ▕"
                    case "C":
                        l_1, l_2, l_3 = \
                            "▏     ", f"▏ {center_char}  ", "🭼▁▁▁▁▁"
                    case "D":
                        l_1, l_2, l_3 = \
                            "🭽▔▔▔▔▔", f"▏ {center_char}  ", "🭼▁▁▁▁▁"
                    case "E":
                        l_1, l_2, l_3 = \
                            "▏    ▕", f"▏ {center_char} ▕", "🭼▁▁▁▁🭿"
                    case "F":
                        # l_1, l_2, l_3 = "🭽▔▔▔▔🭾", "▏ 🟧 ▕", "🭼▁▁▁▁🭿"
                        l_1, l_2, l_3 = f"{maze.control.color}██████"\
                                        f"{maze.control.color}", \
                                        f"{maze.control.color}██████"\
                                        f"{maze.control.color}", \
                                        f"{maze.control.color}██████"\
                                        f"{maze.control.color}"
                line_1 += l_1
                line_2 += l_2
                line_3 += l_3
                x += 1
            x = 0
            y += 1
            buffer += line_1 + "\n"
            buffer += line_2 + "\n"
            buffer += line_3 + "\n"
            # print(f"\033[0;36m{line_1}\033[0;0m")
            # print(f"\033[0;36m{line_2}\033[0;0m")
        print(f"{maze.control.color}{buffer}\033[0;0m")
        tcflush(sys.stdin.fileno(), TCIFLUSH)

    def theme_selector(maze: Maze, cell_type: str):
        if cell_type == 'entry':
            if (maze.control.color == '\033[1;32m'):  # green
                return ('👽')
            elif (maze.control.color == '\033[0;31m'):  # red
                return ('🏎️ ')
            elif (maze.control.color == '\033[1;33m'):  # yellow
                return ('🦜')
            elif (maze.control.color == '\033[1;35m'):  # pink
                return ('👩‍​')
            elif (maze.control.color == '\033[0;34m'):  # pink
                return ('🐝​​')
            else:
                return ('👪')
        elif cell_type == 'exit':
            if (maze.control.color == '\033[1;32m'):  # green
                return ('🚀')
            elif (maze.control.color == '\033[0;31m'):  # red
                return ('🏁')
            elif (maze.control.color == '\033[1;33m'):  # yellow
                return ('🏝️ ')
            elif (maze.control.color == '\033[1;35m'):  # pink
                return ('🐕​​')
            elif (maze.control.color == '\033[0;34m'):  # pink
                return ('🌻​​')
            else:
                return ('🏠')
