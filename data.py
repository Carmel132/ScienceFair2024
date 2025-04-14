
from maze.algorithms import (
    RightHandRule,
    Tremaux,
    BreadthFirst,
    DepthFirst,
    AStar,
    Dijkstra,
    RecursiveBacktracking,
    GreedyBestFirstSearch,
)
from maze.state import MazeState, MazeGeneratorFactory
import timeit
import time
import matplotlib.pyplot as plt
from sys import setrecursionlimit
setrecursionlimit(10**6)
def generateMaze(size) -> MazeState:
    return MazeGeneratorFactory(MazeState(size[0], size[1]), time.time()).generate().cells



import time
import tracemalloc
import heapq
import random
from collections import deque

# Helper function: Check if cell (r, c) is within bounds and open.
def is_valid(maze, r, c):
    rows, cols = len(maze), len(maze[0])
    return 0 <= r < rows and 0 <= c < cols and maze[r][c] == 0

# Define directions in order: North, East, South, West.
directions = [(-1, 0), (0, 1), (1, 0), (0, -1)]

#####################################
# 1. RIGHT HAND RULE
#####################################
def solve_right_hand(maze):
    rows, cols = len(maze), len(maze[0])
    start = (1, 1)
    goal = (rows - 2, cols - 2)
    r, c = start
    # Start by moving East (direction index 1).
    curr_dir = 1  
    path = [start]
    
    # Maximum iterations to avoid infinite loop.
    for _ in range(10000):
        if (r, c) == goal:
            return path
        
        # Relative directions in order: right, forward, left, back.
        right = (curr_dir + 1) % 4
        forward = curr_dir
        left = (curr_dir - 1) % 4
        back = (curr_dir + 2) % 4
        order = [right, forward, left, back]
        
        moved = False
        for ndir in order:
            dr, dc = directions[ndir]
            nr, nc = r + dr, c + dc
            if is_valid(maze, nr, nc):
                r, c = nr, nc
                curr_dir = ndir
                path.append((r, c))
                moved = True
                break
        if not moved:
            # No valid move found, dead end.
            return path
    return path  # Fallback if iteration limit reached

#####################################
# 2. TRÉMAUX ALGORITHM (Simplified DFS with marking)
#####################################
def solve_tremaux(maze):
    rows, cols = len(maze), len(maze[0])
    start = (1, 1)
    goal = (rows - 2, cols - 2)
    visited = {}  # (r, c) -> count of visits
    
    def dfs(r, c, path):
        if (r, c) == goal:
            return path
        visited[(r, c)] = visited.get((r, c), 0) + 1
        # Try all four directions in random order.
        nbrs = []
        for dr, dc in directions:
            nr, nc = r + dr, c + dc
            if is_valid(maze, nr, nc) and visited.get((nr, nc), 0) < 2:
                nbrs.append((nr, nc))
        random.shuffle(nbrs)
        for nr, nc in nbrs:
            if (nr, nc) not in path or visited.get((nr, nc), 0) < 1:
                res = dfs(nr, nc, path + [(nr, nc)])
                if res is not None:
                    return res
        return None
    
    result = dfs(start[0], start[1], [start])
    return result if result is not None else []

#####################################
# 3. BREADTH-FIRST SEARCH (BFS)
#####################################
def solve_breadth_first(maze):
    rows, cols = len(maze), len(maze[0])
    start = (1, 1)
    goal = (rows - 2, cols - 2)
    queue = deque([(start, [start])])
    visited = set([start])
    
    while queue:
        (r, c), path = queue.popleft()
        if (r, c) == goal:
            return path
        for dr, dc in directions:
            nr, nc = r + dr, c + dc
            if is_valid(maze, nr, nc) and (nr, nc) not in visited:
                visited.add((nr, nc))
                queue.append(((nr, nc), path + [(nr, nc)]))
    return []

#####################################
# 4. DEPTH-FIRST SEARCH (DFS)
#####################################
def solve_depth_first(maze):
    rows, cols = len(maze), len(maze[0])
    start = (1, 1)
    goal = (rows - 2, cols - 2)
    stack = [(start, [start])]
    visited = set()
    while stack:
        (r, c), path = stack.pop()
        if (r, c) == goal:
            return path
        if (r, c) in visited:
            continue
        visited.add((r, c))
        for dr, dc in directions:
            nr, nc = r + dr, c + dc
            if is_valid(maze, nr, nc):
                stack.append(((nr, nc), path + [(nr, nc)]))
    return []

#####################################
# 5. A* SEARCH
#####################################
def solve_astar(maze):
    rows, cols = len(maze), len(maze[0])
    start = (1, 1)
    goal = (rows - 2, cols - 2)
    def heuristic(a, b):
        # Manhattan distance
        return abs(a[0] - b[0]) + abs(a[1] - b[1])
    
    open_set = []
    heapq.heappush(open_set, (heuristic(start, goal), 0, start, [start]))
    cost_so_far = {start: 0}
    
    while open_set:
        f, cost, current, path = heapq.heappop(open_set)
        if current == goal:
            return path
        r, c = current
        for dr, dc in directions:
            nr, nc = r + dr, c + dc
            neighbor = (nr, nc)
            if is_valid(maze, nr, nc):
                new_cost = cost + 1
                if neighbor not in cost_so_far or new_cost < cost_so_far[neighbor]:
                    cost_so_far[neighbor] = new_cost
                    priority = new_cost + heuristic(neighbor, goal)
                    heapq.heappush(open_set, (priority, new_cost, neighbor, path + [neighbor]))
    return []

#####################################
# 6. DIJKSTRA'S ALGORITHM
#####################################
def solve_dijkstra(maze):
    rows, cols = len(maze), len(maze[0])
    start = (1, 1)
    goal = (rows - 2, cols - 2)
    open_set = []
    heapq.heappush(open_set, (0, start, [start]))
    distances = {start: 0}
    
    while open_set:
        cost, current, path = heapq.heappop(open_set)
        if current == goal:
            return path
        r, c = current
        for dr, dc in directions:
            nr, nc = r + dr, c + dc
            neighbor = (nr, nc)
            if is_valid(maze, nr, nc):
                new_cost = cost + 1
                if new_cost < distances.get(neighbor, float('inf')):
                    distances[neighbor] = new_cost
                    heapq.heappush(open_set, (new_cost, neighbor, path + [neighbor]))
    return []

#####################################
# 7. RECURSIVE BACKTRACKING
#####################################
def solve_recursive_backtracking(maze):
    rows, cols = len(maze), len(maze[0])
    start = (1, 1)
    goal = (rows - 2, cols - 2)
    visited = set()
    
    def backtrack(r, c, path):
        if (r, c) == goal:
            return path
        visited.add((r, c))
        for dr, dc in directions:
            nr, nc = r + dr, c + dc
            if is_valid(maze, nr, nc) and (nr, nc) not in visited:
                res = backtrack(nr, nc, path + [(nr, nc)])
                if res is not None:
                    return res
        return None
    
    result = backtrack(start[0], start[1], [start])
    return result if result is not None else []

#####################################
# 8. GREEDY BEST-FIRST SEARCH
#####################################
def solve_greedy_best_first_search(maze):
    rows, cols = len(maze), len(maze[0])
    start = (1, 1)
    goal = (rows - 2, cols - 2)
    def heuristic(a, b):
        return abs(a[0] - b[0]) + abs(a[1] - b[1])
    
    open_set = []
    heapq.heappush(open_set, (heuristic(start, goal), start, [start]))
    visited = set()
    
    while open_set:
        h, current, path = heapq.heappop(open_set)
        if current == goal:
            return path
        if current in visited:
            continue
        visited.add(current)
        r, c = current
        for dr, dc in directions:
            nr, nc = r + dr, c + dc
            neighbor = (nr, nc)
            if is_valid(maze, nr, nc) and neighbor not in visited:
                heapq.heappush(open_set, (heuristic(neighbor, goal), neighbor, path + [neighbor]))
    return []

#####################################
# Wrapper: Measure execution time and peak memory usage.
#####################################
def measure_algorithm(solver, maze):
    tracemalloc.start()
    start_time = time.perf_counter()
    result_path = solver(maze)
    end_time = time.perf_counter()
    current, peak_memory = tracemalloc.get_traced_memory()
    tracemalloc.stop()
    return {
        "result_path": result_path,
        "time_seconds": end_time - start_time,
        "peak_memory_bytes": peak_memory
    }
solvers = {
        "RightHandRule": solve_right_hand,
        "Tremaux": solve_tremaux,
        "BreadthFirst": solve_breadth_first,
        "DepthFirst": solve_depth_first,
        "AStar": solve_astar,
        "Dijkstra": solve_dijkstra,
        "RecursiveBacktracking": solve_recursive_backtracking,
        "GreedyBestFirstSearch": solve_greedy_best_first_search
    }
import time
import tracemalloc

# Assume that these functions already exist from your codebase:
#   generateMaze(sz: tuple[int, int]) -> List[List[int]]
#   solvers: dict[str, function] 
#   measure_algorithm(solver, maze) -> dict with keys "result_path", "time_seconds", "peak_memory_bytes"

def measure_algorithm(solver, maze):
    """
    Measures the execution time and peak memory usage of the given solver when run on the maze.
    
    Parameters:
        solver (function): the maze solving function.
        maze (list[list[int]]): the maze input.
    
    Returns:
        dict: with keys:
            "result_path": the returned path from the solver,
            "time_seconds": execution time in seconds,
            "peak_memory_bytes": peak memory used during execution in bytes.
    """
    tracemalloc.start()
    start_time = time.perf_counter()
    result_path = solver(maze)
    end_time = time.perf_counter()
    current, peak_memory = tracemalloc.get_traced_memory()
    tracemalloc.stop()
    return {
        "result_path": result_path,
        "time_seconds": end_time - start_time,
        "peak_memory_bytes": peak_memory
    }

def benchmark_algorithms(sizes: list[tuple[int, int]], iterations: int = 100):
    """
    Runs each maze solving algorithm for each maze size the specified number of iterations,
    measures the execution time and memory usage, and returns the average for each algorithm.
    
    Parameters:
        sizes (list[tuple[int, int]]): List of maze sizes. Each size is a tuple (rows, columns).
        iterations (int): Number of times to run each algorithm for a given maze.
    
    Returns:
        dict: Nested dictionary with average time and memory usage.
              Format:
              { maze_size: { solver_name: {"avg_time": ..., "avg_memory": ...}, ... }, ... }
    """
    # The dictionary that will hold our averaged benchmark data.
    overall_results = {}
    
    for sz in sizes:
        # Generate a maze for the current size. (You could also generate a new maze every iteration if desired.)
        maze = generateMaze(sz)
        overall_results[sz] = {}
        
        # For each solver function in our solvers dictionary.
        for solver_name, solver in solvers.items():
            total_time = 0.0
            total_memory = 0
            # Run the algorithm several times.
            for _ in range(iterations):
                maze = generateMaze(sz)
                stats = measure_algorithm(solver, maze)
                total_time += stats["time_seconds"]
                total_memory += stats["peak_memory_bytes"]
            # Average the metrics.
            avg_time = total_time / iterations
            avg_memory = total_memory / iterations
            overall_results[sz][solver_name] = {"avg_time": avg_time, "avg_memory": avg_memory}
            print(f"Size {sz} - {solver_name}: Average time = {avg_time:.6f} s, Average peak memory = {avg_memory:.0f} bytes")
    
    return overall_results
import csv
def save_results_to_csv(results: dict, filename: str = "benchmark_results.csv"):
    """
    Saves the benchmark results to a CSV file with columns:
    MazeSize, Solver, Average_Time, Average_Memory.
    """
    with open(filename, mode="w", newline="") as csvfile:
        fieldnames = ["MazeSize", "Solver", "Average_Time", "Average_Memory"]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for maze_size, solvers_data in results.items():
            # Convert maze size tuple to a readable string, e.g., "10x10"
            maze_size_str = f"{maze_size[0]}x{maze_size[1]}"
            for solver_name, stats in solvers_data.items():
                writer.writerow({
                    "MazeSize": maze_size_str,
                    "Solver": solver_name,
                    "Average_Time": f"{stats['avg_time']:.6f}",
                    "Average_Memory": f"{stats['avg_memory']:.0f}"
                })
xx = [(30, 30)]#[(3, 3), (5, 5), (6, 6), (8, 8), (10, 10), (15, 15), (20, 20), (30, 30), (40, 40), (60, 60), (80, 80), (100, 100)]

# Example usage:
if __name__ == "__main__":
    # Suppose xx is your list of sizes. For example:
    benchmark_results = benchmark_algorithms(xx, iterations=100)
    save_results_to_csv(benchmark_results, filename="temp30.csv")
import pandas as pd
import matplotlib.pyplot as plt

def parse_maze_size(size_str):
    """
    Parse the maze size string (e.g., "10x10") and return a tuple (rows, cols).
    We will use the horizontal dimension (cols) as our x axis.
    """
    parts = size_str.lower().split("x")
    if len(parts) == 2:
        try:
            rows = int(parts[0])
            cols = int(parts[1])
            return rows, cols
        except ValueError:
            pass
    return None, None

# Read the CSV file into a pandas DataFrame
df = pd.read_csv("benchmark_results.csv")

# Create new columns for rows and columns.
df[['rows', 'cols']] = df['MazeSize'].apply(
    lambda s: pd.Series(parse_maze_size(s))
)

# For the x-axis, we use the maze's horizontal dimension (cols).
df['x_size'] = df['cols']

# Convert the Average_Time and Average_Memory columns to numeric types.
df['Average_Time'] = pd.to_numeric(df['Average_Time'], errors='coerce')
df['Average_Memory'] = pd.to_numeric(df['Average_Memory'], errors='coerce')

# Get the unique solver names.
solvers = df['Solver'].unique()

# --- Plot Average Time ---
ax = plt.figure(figsize=(10, 6))
for solver in solvers:
    # Subset the data for each solver
    solver_data = df[df['Solver'] == solver].sort_values(by='x_size')
    plt.plot(solver_data['x_size'], solver_data['Average_Time'],
             marker='o', label=solver)
plt.xlabel("Maze X Size (columns)")
plt.ylabel("Average Time (seconds)")
plt.title("Maze Solving Time by Algorithm")
plt.legend(title="Algorithm")
plt.grid(True)
plt.tight_layout()
plt.yscale('log')
plt.show()

# --- Plot Average Memory ---
plt.figure(figsize=(10, 6))
for solver in solvers:
    solver_data = df[df['Solver'] == solver].sort_values(by='x_size')
    plt.plot(solver_data['x_size'], solver_data['Average_Memory'],
             marker='o', label=solver)
plt.xlabel("Maze Size")
plt.ylabel("Average Memory (bytes)")
plt.title("Maze Solving Memory Usage by Algorithm")
plt.legend(title="Algorithm")
plt.grid(True)
plt.tight_layout()
plt.yscale('log')
plt.show()