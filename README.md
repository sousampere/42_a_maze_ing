*This project has been created as part of the 42 curriculum by gtourdia, lbonnet*

# 42_a_maze_ing

Personnal group implementation of the A_Maze_Ing project of school 42.

## Description

The goal of the project is to create and visualize a maze, randomly generated, with a 42 pattern inside of it. Given an entry and an exit coordinates, we also have to provide a path-finding algorithm that solves the shortest path from entry to exit. This result will be outputted in a given file, in an hexadecimal representation of each cell, row by row.

## Steps

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

Example of a valid configuration file :
```
# Dimensions
WIDTH=9
HEIGHT=8

# Entry/Exit coords
ENTRY=0,0
EXIT=7,7

# Maze output file path, should not contain spaces
OUTPUT_FILE=maze.txt

# Enable/disable perfect maze
PERFECT=true

# Seed-based generation
SEED=pathfinder_seed

# Enable / disable animation
ANIMATION=true

# Show/Hide the shortest path
SHOW_PATH=true

# Display the 42 patern. Default in center if entry/exit coords make it possible
DISPLAY_FT_PATTERN=True
```

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

![Demo](https://i.ibb.co/8DhLrf5Z/example.gif)

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

## Instructions

You will need to have Make, UV and python installed on your pc.

To install the venv and dependencies, use:
```bash
make install
```

To run the program, use : 
```bash
uv run python a_maze_ing.py <configuration_file_path>
```
or
```bash
make run
```

#### Make commands
|Utility|Command|
|---|---|
|Installation|```make install```|
|Running program|```make run```|
|Check norm|```make lint-strict```|
|Remove uselss files|```make clean```|
|Remove uselss files and reinstall|```make re```|
|Build package|```make build```|
|Debug (CLI)|```make debug```|

## Resources

#### Useful links
- [Maze generation algorithm](https://www.jamisbuck.org/presentations/rubyconf2011/index.html#recursive-backtracker-demo)
- [Flushing stdin](http://jamescherti.com/python-flushing-stdin-before-using-input-function/)
- [Wikipedia](https://en.wikipedia.org/wiki/Maze_generation_algorithm/)

## Additional informations

#### Reusable code
We made the program so that the MazeGenerator is reusable in another project. The user can add this object in its code by installing the package generated with the ```make build``` comand. It can then be used with this simple example:
```python

from mazegen import MazeGenerator, PathFinder, Config

def main():

    # Setup a configuration variable
    config = Config(width=8,
                    height=8,
                    entry_coords={'x': 0, 'y': 0},
                    exit_coords={'x': 7, 'y': 7},
                    output_file='test.txt',
                    perfect=False,
                    seed='laurent',
                    animation=True,
                    show_path=True,
                    display_ft_pattern=True)

    # Create a maze
    generator = MazeGenerator(config)
    generator.create_maze()

    # Generate the maze's content
    list(generator.generate_existing_maze())

    # Dig holes to make it unperfect
    generator.maze.make_maze_perfect(True)

    # Generate the shortest path
    PathFinder.find_path(generator.maze)

    # Save the maze to a file
    generator.maze.output_maze(config.output_file)

if __name__ == "__main__":
    main()

```

The Config object needed by the MazeGenerator is validated by pydantic. If you want to generate a random seed, you need to set the seed value to a random value (using random, uuid, or another randomization module).

The path finding is generated by the PathFinder.find_path() staticmethod. Give it a Maze object and it will solve it (if possible)

#### AI usage
In the realisation of this project, AI was used in various tasks, but mostly troubleshooting and research :
- Troubleshooting a yield function
- Troubleshooting strange error codes
- Various questions about how to use different modules
- Understanding package creation

#### Planification

Like the push_swap project that we did together, [lbonnet](https://github.com/kletsol) and [I](https://github.com/sousampere) saw that we didn't plan the project enough, by realising the project while reading the subject, instead of plannifying everything from the start. This made the project unstable when we discovered special requirements in the subject that we didn't plan.

We will take this in consideration for the future projects: ***<ins>Planning is not an option</ins>***. (This is not a threat.)

Otherwise, we were good at making our parts of the code work together..

#### Specific tools used

|Tool|Usage|
|---|---|
|argparse (python package)|Argument parsing|
|pynput (python package)|Keyboard keys interception|
|pydantic (python package)|Data validation for parsing|
|flake8 (python package)|Check the flake8 norm|
|mypy (python package)|Check the mypy norm|
|uv (python package manager)|Project management and package building|

## 🚀 Authors and contributions

[gtourdia / @sousampere](https://github.com/sousampere)

- Configuration, Cell and Maze objects
- Pathfinding and generation algorithm
- Package build
- Readme

[lbonnet / @kletsol](https://github.com/kletsol)

- Controller object (Maze interruption)
- MazeVisualizer object to visualize the maze
- Colors, Reset, Pause interactions
- Various bonuses
- Flake8, since [gtourdia](https://github.com/sousampere) didn't really pay attention about it ;)

Other tasks were done by the two of us.
![Logo](https://github.com/sousampere/sousampere/blob/main/42mulhouse.png?raw=true)
