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
df = pd.read_csv("benchmark_results_2.csv")

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
markers = ['o', "v", "s", "*", "D", "p", "X", "1"]
for solver, marker in zip(solvers, markers):
    # Subset the data for each solver
    solver_data = df[df['Solver'] == solver].sort_values(by='x_size')
    plt.plot(solver_data['x_size'], solver_data['Average_Time'],
             marker=marker, label=solver, markersize=10)
plt.xlabel("Maze Size")
plt.ylabel("Average Time (seconds)")
plt.title("Maze Solving Time by Algorithm")
plt.legend(title="Algorithm")
plt.grid(True)
plt.tight_layout()
plt.yscale('log')
plt.show()

# --- Plot Average Memory ---
plt.figure(figsize=(10, 6))
for solver, marker in zip(solvers, markers):
    solver_data = df[df['Solver'] == solver].sort_values(by='x_size')
    plt.plot(solver_data['x_size'], solver_data['Average_Memory'],
             marker=marker, label=solver, markersize = 10)
plt.xlabel("Maze Size")
plt.ylabel("Average Memory (bytes)")
plt.title("Maze Solving Memory Usage by Algorithm")
plt.legend(title="Algorithm")
plt.grid(True)
plt.tight_layout()
plt.yscale('log')
plt.show()