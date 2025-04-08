from .state import MazeState, Path, MazeGeneratorFactory
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
