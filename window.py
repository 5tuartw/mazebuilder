import tkinter as tk
from tkinter import ttk
from maze import Maze
from findrect import find_best_rect
from metrics import MazeMetrics

class Window:
    MARGIN = 10
    CELL_SIZE_DIVISOR = 4
    MIN_CELL_SIZE = 10

    def __init__(self, config_manager):
        self._width = config_manager.get("window_width")
        self._height = config_manager.get("window_height")
        self._num_rows = 0
        self._num_cols = 0
        self._cell_size = self.MIN_CELL_SIZE
        self._num_mazes = config_manager.get("num_mazes")
        self._style = "Backtrack"
        self._config_manager = config_manager

        self.__root = tk.Tk()
        self.__root.title("Maze Builder")
        self.__root.geometry(f"{self._width}x{self._height}")

        self.control_frame = tk.Frame(self.__root)
        self.control_frame.pack(side=tk.TOP, fill=tk.X)

        self.canvas_frame = tk.Frame(self.__root)
        self.canvas_frame.pack(fill=tk.BOTH, expand=1)

        self.__canvas = tk.Canvas(self.canvas_frame, bg="white", highlightthickness=0)
        self.__canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=1)

        self.scrollbar = tk.Scrollbar(self.canvas_frame, orient=tk.VERTICAL, command=self.__canvas.yview)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.__canvas.config(yscrollcommand=self.scrollbar.set)

        self.add_buttons()

        self.__running = False
        self.__root.protocol("WM_DELETE_WINDOW", self.close)

        self._mazes = []

    def redraw(self):
        self.__root.update_idletasks()
        self.__root.update()

    def wait_for_close(self):
        self.__running = True
        while self.__running:
            self.redraw()

    def close(self):
        self.__running = False

    def draw_line(self, line, fill_color="black"):
        return line.draw(self.__canvas, fill_color)

    def add_buttons(self):
        size_select_lbl = tk.Label(self.control_frame, text="Select maze creation style:")
        size_select_lbl.pack(side=tk.LEFT)

        # radio buttons for choosing style
        self.style_var = tk.StringVar(value="Backtrack") #default style
        styles = ["Backtrack", "Prim's", "Kruskal's"]
        for style in styles:
            btn = ttk.Radiobutton(self.control_frame, text=style, variable=self.style_var, value = style, command=self.update_style_and_create_mazes)
            btn.pack(side=tk.LEFT)
        
        # separator1
        separator1 = ttk.Separator(self.control_frame, orient='vertical')
        separator1.pack(side=tk.LEFT, fill=tk.Y, padx=10)

        # Selector for number of mazes
        num_mazes_lbl = tk.Label(self.control_frame, text="No. of mazes:")
        num_mazes_lbl.pack(side=tk.LEFT)
        self.num_mazes_entry = tk.Entry(self.control_frame, width=5)
        self.num_mazes_entry.pack(side=tk.LEFT)
        self.num_mazes_entry.insert(0, str(self._num_mazes))

        update_btn = ttk.Button(self.control_frame, text="Update", command=self.update_num_mazes)
        update_btn.pack(side=tk.LEFT)

        # separator2
        separator2 = ttk.Separator(self.control_frame, orient='vertical')
        separator2.pack(side=tk.LEFT, fill=tk.Y, padx=10)

        stats_btn = ttk.Button(self.control_frame, text="Stats", command=self._calc_and_show_average_stats)
        stats_btn.pack(side=tk.LEFT)

    def update_style_and_create_mazes(self):
        self._style = self.style_var.get()
        self._create_mazes()

    def update_num_mazes(self):
        try:
            self._num_mazes = int(self.num_mazes_entry.get())
            self._create_mazes()
            self._config_manager.set("num_mazes", self._num_mazes)
            self._config_manager.save_config()
        except ValueError:
            print("Invalid number of mazes")

    def _create_mazes(self, style=None):
        if style:
            self._style = style
        print(f"Creating {self._num_mazes} mazes in the style: {self._style}")
        self.__canvas.delete("all")
        self._mazes = []

        self._num_cols = 8
        self._num_rows = 6

        self._calculate_cell_size(self._width - 2 * self.MARGIN, self._height - 2 * self.MARGIN)

        x_position = self.MARGIN
        y_position = self.MARGIN

        for i in range(self._num_mazes):
            self._mazes.append(Maze(x_position, y_position, self._num_rows, self._num_cols, self._cell_size, self._cell_size, self.__root, self.__canvas, style=self._style))
            x_position += self._num_cols * self._cell_size + 10
            if x_position + self._num_cols * self._cell_size > self._width:
                x_position = self.MARGIN
                y_position += self._num_rows * self._cell_size + 10

            self._mazes[i].draw_shortest_path()

    def _calculate_cell_size(self, maze_width, maze_height):
        layout = find_best_rect(self._num_mazes)
        if layout:
            maze_rows, maze_columns, _ = layout
            cell_size_width = (self._width - (maze_columns + 1) * self.MARGIN) / (maze_columns * self._num_cols)
            cell_size_height = (self._height - (maze_rows + 1) * self.MARGIN) / (maze_rows * self._num_rows)
            self._cell_size = max(min(cell_size_height, cell_size_width), self.MIN_CELL_SIZE)
        else:
            self._cell_size = self.MIN_CELL_SIZE
    
    def _calc_and_show_average_stats(self):
        maze_description = f"Style:{self._style}\nNumber of mazes:{self._num_mazes}\n"

        average_maze_stats = MazeMetrics(0.0,0.0,0.0,0.0,0.0,0.0)
        if len(self._mazes) == 0:
            print("No mazes have been made yet")
            return
        for maze in self._mazes:
            average_maze_stats += maze.metrics
        average_maze_stats = average_maze_stats.div_metrics(self._num_mazes)
        average_maze_stats.show_metrics_window(self.__root, maze_description)