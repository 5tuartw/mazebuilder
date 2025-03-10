This is a personal project developing ideas from the <a href="https://www.boot.dev/">Boot.dev</a> Maze Solver course.

# Maze Generator (Work in Progress)

This project is a maze solver application built using Python and Tkinter. It generates and solves mazes using different algorithms and displays them in a graphical window, giving you visual and statistical information about the maze complexity.

## Features

- Generate mazes using different algorithms (Backtracking, Prim's, Kruskal's, and more to come)
- Solve mazes and display the solution path
- Visualize multiple mazes on the same canvas
- See diversions from the main path coloured by who large a detour they cause
- saves configurations
![screenshot](https://github.com/5tuartw/mazebuilder/blob/maze-variations/screenshot2.png)

## Maze generating algorithms
- Recursive backtracking:
Starts at the entrance and moves to a random neighbour until it can't move any more, then backtracks to the previous cell that had unvisited neighbours and repeats. Tends to have long solutions, but also long diversions
- Prim's algorithm:
Starts in a random cell keeps a list of its walls that haven't been knocked down. Chooses a random wall and 'visits' the new cell, then adds its walls to a list of walls to attempt. Repeats until all cells have been visited. More cells are junctions of multiple routes, so has a shorter solution and diversions also tend to be short.
- Kruskal's method:
Each cell is a member of its own set, and as walls are broken down between cells their sets are combined, until there is only one set. This algorithm ensures there is only one path between any two cells in the maze. The patterns tend to be more interesting (few straight corridors) and the solutions can be long and short.

## Idea for development ##
I would like to develop:
- settings panel to change the number of rows/columns in each maze and the colours
- improvements to the stats window, with some visualisations and mouse-over details
- allow people to play the mazes to compare completion times with the complexity data to see which metrics correlate with maze difficulty

## Requirements

- Python 3.x
- Tkinter (included with standard Python installations)

## Contributing
## 🤝 Contributing

### Clone the repo

```bash
git clone https://github.com/5tuartw/mazebuilder
cd mazebuilder
```

### Run the project

```bash
python3 main.py
```

### Submit a pull request

If you'd like to contribute, please fork the repository and open a pull request to the `main` branch.
