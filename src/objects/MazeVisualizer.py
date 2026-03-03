
from termios import TCIFLUSH, tcflush
from src import Maze
import time
import sys

class MazeVisualizer():
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
                    center_char = '🏠'
                elif (x == maze.config.exit_coords['x']
                      and y == maze.config.exit_coords['y']):
                    center_char = '🚀'
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

