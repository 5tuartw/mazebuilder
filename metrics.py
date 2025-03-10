import tkinter as tk

class MazeMetrics:
    def __init__(self, shortest_path_length, dead_end_count, branching_factor, corridor_length, solution_path_length, maze_density):
        self.shortest_path_length = shortest_path_length
        self.dead_end_count = dead_end_count
        self.branching_factor = branching_factor
        self.corridor_length = corridor_length
        self.solution_path_length = solution_path_length
        self.maze_density = maze_density

    def __repr__(self):
        return (f"MazeMetrics(shortest_path_length={self.shortest_path_length}, "
                f"dead_end_count={self.dead_end_count}, branching_factor={self.branching_factor}, "
                f"corridor_length={self.corridor_length}, solution_path_length={self.solution_path_length}, "
                f"maze_density={self.maze_density})")
    
    def __add__(self, other):
        if not isinstance(other, MazeMetrics):
            return NotImplemented
        return MazeMetrics(
            shortest_path_length=self.shortest_path_length + other.shortest_path_length,
            dead_end_count=self.dead_end_count + other.dead_end_count,
            branching_factor=self.branching_factor + other.branching_factor,
            corridor_length=self.corridor_length + other.corridor_length,
            solution_path_length=self.solution_path_length + other.solution_path_length,
            maze_density=self.maze_density + other.maze_density
        )
    
    def div_metrics(self, number):
        return MazeMetrics(
            shortest_path_length=self.shortest_path_length/number,
            dead_end_count=self.dead_end_count/number,
            branching_factor=self.branching_factor/number,
            corridor_length=self.corridor_length/number,
            solution_path_length=self.solution_path_length/number,
            maze_density=self.maze_density/number
        )
    
    def show_metrics_window(self, parent, description):
        stats_window = tk.Toplevel(parent)
        stats_window.title("Maze Metrics")

        stats_frame = tk.Frame(stats_window)
        stats_frame.pack(padx=10, pady=10)

        metrics_text = (
            f"{description}\n"
            f"Shortest Path Length: {self.shortest_path_length:.2f}\n"
            f"Dead End Count: {self.dead_end_count:.2f}\n"
            f"Branching Factor: {self.branching_factor:.2f}\n"
            f"Corridor Length: {self.corridor_length:.2f}\n"
            f"Solution Path Length: {self.solution_path_length:.2f}\n"
            f"Maze Density: {self.maze_density:.2f}"
        )

        stats_label = tk.Label(stats_frame, text=metrics_text, justify=tk.LEFT)
        stats_label.pack()
