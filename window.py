import tkinter as tk
from tkinter import ttk
from maze import Maze

class Window:
    MARGIN = 10
    CELL_SIZE_DIVISOR = 4
    MIN_CELL_SIZE = 10
    MAX_WINDOW_HEIGHT = 600
    MIN_WINDOW_WIDTH = 700

    def __init__(self, config_manager):
        self._width = config_manager.get("window_width")
        self._height = config_manager.get("window_height")
        self._num_rows = 0
        self._num_cols = 0
        self._cell_size = 0
        self._num_mazes = config_manager.get("num_mazes")
        self._config_manager = config_manager

        self.__root = tk.Tk()
        self.__root.title("Maze Solver")

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

        styles = ["Backtrack", "Prim's", "Kruskal's"]
        for style in styles:
            btn = ttk.Button(self.control_frame, text=style, command=lambda s=style: self._create_mazes(s))
            btn.pack(side=tk.LEFT)
        
        num_mazes_lbl = tk.Label(self.control_frame, text="Number of mazes:")
        num_mazes_lbl.pack(side=tk.LEFT)
        self.num_mazes_entry = tk.Entry(self.control_frame, width=5)
        self.num_mazes_entry.pack(side=tk.LEFT)
        self.num_mazes_entry.insert(0, str(self._num_mazes))

        update_btn = ttk.Button(self.control_frame, text="Update", command=self.update_num_mazes)
        update_btn.pack(side=tk.LEFT)

    def update_num_mazes(self):
        try:
            self._num_mazes = int(self.num_mazes_entry.get())
            self._create_mazes("Backtrack")  # You can change the default style if needed
        except ValueError:
            print("Invalid number of mazes")


    def _create_mazes(self, style):
        self.__canvas.delete("all")
        self._mazes = []

        self._num_cols = 8
        self._num_rows = 6

        self._calculate_cell_size(self._width - 2 * self.MARGIN, self._height - 2 * self.MARGIN)
        self._adjust_window_size()

        x_position = self.MARGIN
        y_position = self.MARGIN

        for i in range(self._num_mazes):
            self._mazes.append(Maze(x_position, y_position, self._num_rows, self._num_cols, self._cell_size, self._cell_size, self.__root, self.__canvas, style=style))
            x_position += self._num_cols * self._cell_size + 10
            if x_position + self._num_cols * self._cell_size > self._width:
                x_position = self.MARGIN
                y_position += self._num_rows * self._cell_size + 10

            self._mazes[i].draw_shortest_path()

    def _calculate_cell_size(self, maze_width, maze_height):
        cell_size = maze_width / self._num_cols
        if cell_size * self._num_rows < maze_height:
            self._cell_size = max(cell_size / self.CELL_SIZE_DIVISOR, self.MIN_CELL_SIZE)
        else:
            self._cell_size = max(maze_height / self._num_rows / self.CELL_SIZE_DIVISOR, self.MIN_CELL_SIZE)
        print(f"Cell size: {cell_size}")

    def _adjust_window_size(self):
        num_mazes_per_row = (self._width - self.MARGIN) // (self._num_cols * self._cell_size + 10)
        num_rows_of_mazes = (self._num_mazes + num_mazes_per_row - 1) // num_mazes_per_row

        required_width = max(self.MIN_WINDOW_WIDTH, int(num_mazes_per_row * (self._num_cols * self._cell_size + 10) + self.MARGIN))
        required_height = int(num_rows_of_mazes * (self._num_rows * self._cell_size + 10) + self.MARGIN)

        self.__root.update_idletasks()
        control_frame_height = self.control_frame.winfo_height()
        total_required_height = required_height + control_frame_height

        self.__root.geometry(f"{required_width}x{total_required_height}")
        self.__canvas.config(width=required_width, height=required_height)

        self._config_manager.set("window_width", required_width)
        self._config_manager.set("window_height", total_required_height)
        self._config_manager.save_config()