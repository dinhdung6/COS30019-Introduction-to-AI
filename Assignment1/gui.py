import tkinter as tk
from search_utilities import AdventurerNode
import time

class PathVisualizer(tk.Tk):
    def __init__(self, grid, start, goals, path, traversed, start_time):
        super().__init__()
        self.title("Robot Navigation")
        self.cell_size = 25
        self.grid = grid
        self.start = start
        self.goals = goals
        self.path = path
        self.traversed = traversed
        self.start_time = start_time
        self.canvas_width = self.cell_size * grid.cols
        self.canvas_height = self.cell_size * grid.rows
        self.geometry(f"{self.canvas_width}x{self.canvas_height}")
        self.canvas = tk.Canvas(self, width=self.canvas_width, height=self.canvas_height)
        self.canvas.pack()
        self.draw_grid()
        self.path_index = 0
        self.traversed_index = 0
        self.animate_path()

    def draw_grid(self):
        for row in range(self.grid.rows):
            for col in range(self.grid.cols):
                x0, y0 = col * self.cell_size, row * self.cell_size
                x1, y1 = x0 + self.cell_size, y0 + self.cell_size
                color = self.get_color(col, row)
                self.canvas.create_rectangle(x0, y0, x1, y1, fill=color, outline="black")

    def get_color(self, col, row):
        if (col, row) == self.start:
            return "red"
        for goal in self.goals:
            if (col, row) == goal:
                return "green"
        if self.grid.grid_map[row][col] == 1:
            return "gray"
        return "white"

    def animate_path(self):
        if self.traversed_index < len(self.traversed):
            self.draw_traversed()
        elif self.path_index < len(self.path):
            self.draw_path()
        else:
            self.end_time = time.time()
            print(f"Time taken: {self.end_time - self.start_time:.6f} seconds")

    def draw_traversed(self):
        node = self.traversed[self.traversed_index]
        if (node[0], node[1]) != self.start and (node[0], node[1]) not in self.goals:
            x0, y0 = node[0] * self.cell_size, node[1] * self.cell_size
            x1, y1 = x0 + self.cell_size, y0 + self.cell_size
            self.canvas.create_rectangle(x0, y0, x1, y1, fill="yellow", outline="black")
        self.traversed_index += 1
        self.after(200, self.animate_path)

    def draw_path(self):
        node = self.path[self.path_index]
        x0, y0 = node[0] * self.cell_size, node[1] * self.cell_size
        x1, y1 = x0 + self.cell_size, y0 + self.cell_size
        self.canvas.create_rectangle(x0, y0, x1, y1, fill="red", outline="black")
        self.path_index += 1
        self.after(100, self.animate_path)

def run_gui(grid, start, goals, path, traversed, start_time):
    visualizer = PathVisualizer(grid, start, goals, path, traversed, start_time)
    visualizer.mainloop()
