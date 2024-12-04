import tkinter as tk
import subprocess
import time
import ast
from search_utilities import ExpeditionGrid

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
        self.canvas_width = self.cell_size * self.grid.cols
        self.canvas_height = self.cell_size * self.grid.rows
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
        if (col, row) in self.goals:
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
        self.after(500, self.animate_path)  # Increased delay to 500ms for better visibility

    def draw_path(self):
        node = self.path[self.path_index]
        x0, y0 = node[0] * self.cell_size, node[1] * self.cell_size
        x1, y1 = x0 + self.cell_size, y0 + self.cell_size
        self.canvas.create_rectangle(x0, y0, x1, y1, fill="red", outline="black")  # Final path in red
        self.path_index += 1
        self.after(500, self.animate_path)  # Increased delay to 500ms for better visibility

def run_simulation(use_jumps):
    jump_flag = 'true' if use_jumps else 'false'
    try:
        result = subprocess.run(['python', 'search.py', 'RobotNav-test.txt', 'astar', jump_flag], check=True, capture_output=True, text=True)
        output = result.stdout
        grid, start, goals, path, traversed = parse_output(output)
        start_time = time.time()
        run_gui(grid, start, goals, path, traversed, start_time)
    except subprocess.CalledProcessError as e:
        print(f"Failed to run simulation: {e.stderr}")

def parse_output(output):
    lines = output.split('\n')
    grid = None
    start = None
    goals = []
    path = []
    traversed = []
    for line in lines:
        if line.startswith('Parsed grid dimensions:'):
            dims = line.split(': ')[1]
            dims = dims.split(' x ')
            grid = ExpeditionGrid(int(dims[0]), int(dims[1]))
        elif line.startswith('Parsed start:'):
            start = ast.literal_eval(line.split(': ')[1])
        elif line.startswith('Parsed goals:'):
            goals = ast.literal_eval(line.split(': ')[1])
        elif line.startswith('Grid after placing obstacles:'):
            grid_start = lines.index(line) + 1
            for i in range(grid.rows):
                row = list(map(int, lines[grid_start + i].strip()))
                grid.grid_map[i] = row
        elif line.startswith('Path found:'):
            path = ast.literal_eval(line.split(': ')[1])
        elif line.startswith('Current Node:'):
            node = line.split(': ')[1].split(', ')[0]
            node = ast.literal_eval(node)
            traversed.append(node)
    return grid, start, goals, path, traversed

def run_gui(grid, start, goals, path, traversed, start_time):
    visualizer = PathVisualizer(grid, start, goals, path, traversed, start_time)
    visualizer.mainloop()

if __name__ == "__main__":
    root = tk.Tk()
    root.title("Robot Navigation Controller")
    tk.Button(root, text="Run without Jumps", command=lambda: run_simulation(False)).pack()
    tk.Button(root, text="Run with Jumps", command=lambda: run_simulation(True)).pack()
    root.mainloop()
