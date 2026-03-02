*This project has been created as part of the 42 curriculum by gtourdia, lbonnet*

# 42_a_maze_ing

Personnal group implementation of the A_Maze_Ing project of school 42.

## Description

### Configuration file parsing

On this project, we first need to parse informations from a configuration file. This implies ignoring comments and invalid flags.

|Type|Flag|Expected value|Format|Description|
|---|---|---|---|---|
|Mandatory|WIDTH|int >= 2|WIDTH=20|Maze width
|Mandatory|HEIGHT|int >= 2|HEIGHT=20|Maze height
|Mandatory|ENTRY|x & y within available dimensions|ENTRY=1,2|Entry point for path-finding
|Mandatory|EXIT|x & y within available dimensions|EXIT=4,6|Exit point for path-finding
|Mandatory|OUTPUT_FILE|string|OUTPUT_FILE=maze.txt|Output file path
|Mandatory|PERFECT|bool|PERFECT=True|If the maze has one wall or more
|Mandatory|SEED|string|SEED=laurent|Generation seed
|Mandatory|DISPLAY_FT_PATTERN|bool|DISPLAY_FT_PATTERN=False|Add/remove the 42 logo in the center

### Maze generation

Next step is the generation of a maze following the requirements in the config file. While it is not asked in the subject, we included a generation animation as a bonus in the project.

<img src="https://i.ibb.co/MDt7DtHy/image.png" alt="Maze 1" width="300">
<img src="https://i.ibb.co/s96hJX2Y/image.png" alt="Maze 2" width="300">



### Python package creation

The second goal of the a-maze-ing project is to create a Python package from our work, reusable in a future project. This python package will make us enable to generate a Maze using the MazeGenerator object.

## 🚀 Authors

- [gtourdia / @sousampere](https://github.com/sousampere)
- [lbonnet / @kletsol](https://github.com/kletsol)

![Logo](/home/gtourdia/Pictures/zzlatkov.jpg)