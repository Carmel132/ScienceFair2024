from .state import MazeState, Path, MazeGeneratorFactory, AXIAL_DIRECTIONS
from .logger import LoggerGroup, StateLogger, StepLogger, PathLogger


class Algorithm:
    def run(self) -> None: ...


class RightHandRule(Algorithm):
    directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]

    def __init__(self, _maze) -> None:
        self.maze: MazeState = _maze
        self.path: Path = Path(_maze)

    def run(self) -> None:
        self.maze.logger.newPhase("RightHandRule")
        pos = (1, 1)
        currentDir = 0
        end = (self.maze.width * 2 - 1, self.maze.height * 2 - 1)
        self.path.add(pos)

        while pos != end:
            newDir = (currentDir + 1) % 4
            newPos = (
                pos[0] + RightHandRule.directions[newDir][0],
                pos[1] + RightHandRule.directions[newDir][1],
            )

            if self.maze[newPos] == 0:
                pos = newPos
                currentDir = newDir
                self.path.add(pos)
            else:
                newPos = (
                    pos[0] + RightHandRule.directions[currentDir][0],
                    pos[1] + RightHandRule.directions[currentDir][1],
                )
                if self.maze[newPos] == 0:
                    pos = newPos
                    self.path.add(pos)
                else:
                    currentDir = (currentDir - 1) % 4
            self.maze.logger.endStep(self.maze)


class Tremaux(Algorithm):
    directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]

    def __init__(self, _maze) -> None:
        self.maze: MazeState = _maze
        self.path: Path = Path(_maze)
        # Dictionary to store the number of times each cell is visited.
        # Keys are positions (x, y) and values are counts.
        self.marks = {}

    def run(self) -> None:
        self.maze.logger.newPhase("Tremaux")

        # Starting at the entrance (for example, (1,1)) and setting the exit.
        pos = (1, 1)
        end = (self.maze.width * 2 - 1, self.maze.height * 2 - 1)
        self.path.add(pos)
        # Mark the start cell as visited once.
        self.marks[pos] = 1

        while pos != end:
            # Gather valid adjacent positions.
            candidates = []
            for d in AXIAL_DIRECTIONS:
                newPos = (pos[0] + d[0], pos[1] + d[1])
                if self.maze[newPos] == 0:  # check if it is a passage
                    # Get current mark count; unvisited cells have 0.
                    count = self.marks.get(newPos, 0)
                    # We only consider cells visited less than 2 times.
                    if count < 2:
                        candidates.append((count, newPos))

            if candidates:
                # Choose candidate with the lowest mark count (i.e. prefer unvisited)
                candidates.sort(key=lambda x: x[0])
                chosen = candidates[0][1]
                # Increase the mark for the chosen cell.
                self.marks[chosen] = self.marks.get(chosen, 0) + 1
                pos = chosen
                self.path.add(pos)
            else:
                self.path.remove()
                # Backtrack to the previous position.
                pos = self.path.path[-1]

            self.maze.logger.endStep(self.maze)


class BreadthFirst(Algorithm):
    directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]

    def __init__(self, _maze) -> None:
        self.maze: MazeState = _maze
        self.path: Path = Path(_maze)

    def run(self) -> None:
        self.maze.logger.newPhase("BreadthFirst")

        # Define starting and ending positions. Assume the maze is indexed such that
        # (1,1) is the start and (maze.width * 2 - 1, maze.height * 2 - 1) is the exit.
        start = (1, 1)
        end = (self.maze.width * 2 - 1, self.maze.height * 2 - 1)

        # Initialize the queue for the BFS and mark the start as visited.
        queue = [start]
        visited = {start: True}
        # Predecessor dictionary to reconstruct the path later.
        predecessor = {start: None}

        found = False
        # Process the queue until it's empty or the end is found.
        while queue and not found:
            current = queue.pop(0)
            if current == end:
                found = True
                break

            # Explore all neighboring positions.
            for d in BreadthFirst.directions:
                new_pos = (current[0] + d[0], current[1] + d[1])
                # Check if the new position is within maze bounds and is accessible.
                if self.maze[new_pos] == 0 and new_pos not in visited:
                    visited[new_pos] = True
                    predecessor[new_pos] = current
                    queue.append(new_pos)

            # Log the state after each step.
            self.maze.logger.endStep(self.maze)

        # Reconstruct the path from end to start using the predecessor links.
        solution_path = []
        node = end
        while node is not None:
            solution_path.append(node)
            node = predecessor[node]
        solution_path.reverse()

        # Add each node of the solution to the path.
        for pos in solution_path:
            self.path.add(pos)
