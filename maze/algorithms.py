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
