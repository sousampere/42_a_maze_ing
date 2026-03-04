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
|Optional|ANIMATION|bool|ANIMATION=True|Animate the maze generation
|Optional|SHOW_PATH|bool|SHOW_PATH=True|Displays the shortest path when the maze is generated

### Maze generation

Next step is the generation of a maze following the requirements in the config file. While it is not asked in the subject, we included a generation animation as a bonus in the project.

### Maze animation

We decided to use the terminal to visualize our maze :

<img src="https://i.ibb.co/MDt7DtHy/image.png" alt="Maze 1" width="300">
<img src="https://i.ibb.co/s96hJX2Y/image.png" alt="Maze 2" width="300">

### Generation algorithm

We used the recursive backtracker algorithm to generate the maze: A stack is created where each visited cell is added to the stack. The algorythm starts at the entry point, and visit a random neighbouring cell (based on the seed) that is breakable (ignoring the protected cells like the 42 logo cells, and the maze's border cells). The previous cell is added to the stack, and the program continues to select a random neighbouring cell until it reaches a dead end. In this case, it goes back in the stack, cell by cell, until it finds one with a neighbouring cell that he hasn't visited yet. This process will automatically create a perfect maze, so we have to break random walls to make it imperfect. [See a visual explanation here](https://www.jamisbuck.org/presentations/rubyconf2011/index.html#recursive-backtracker). 

We chose this algorithm because it's easy to understand and well known.

### Path-Finding algorithm

After talking with @luflores, we implemented a simple "propagation" algorithm. Starting from the entry, all neighbouring cells become "active cells" and check their own neighbouring cells, repeating this process until the exit is found. The propagation history of the final cell is then the shortest path.

### Interactive control keys

During the execution of our project, it is possible to interact with it with the following keys:

|Key|Interaction|
|---|---|
|c|Change color|
|r|Regenerate the maze|
|-|Decrease animation speed|
|+|Increase animation speed|
|p|Pause animation|
|Enter ↩|Resume animation|

### Result output

The resut maze, its entry/exit coordinates and its shortest path are saved in the given output file (OUTPUT_FILE flag in the config.txt) in the following format :

- Hexadecimal representation of the cells where each digit encodes which walls are closed, following this principle:

    |Bit|Direction|
    |---|---|
    |0 (LSB)|North|
    |1|East|
    |2|South|
    |3|West|
        A closed wall is a bit to 1, so 1010 means that east and west are closed.

- Entry coords: (x,y)
- Exit coords: (x,y)
- The shortest path to solve the maze, with each move corresponding to a direction to go to (N=north, E=east, ...)

### Python package creation

The second goal of the a-maze-ing project is to create a Python package from our work, reusable in a future project. This python package will make us enable to generate a Maze using the MazeGenerator object.

## 🚀 Authors

- [gtourdia / @sousampere](https://github.com/sousampere)
- [lbonnet / @kletsol](https://github.com/kletsol)

![Logo](/home/gtourdia/Pictures/zzlatkov.jpg)
