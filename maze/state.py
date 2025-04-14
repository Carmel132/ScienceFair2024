from maze.logger import LoggerGroup
from random import seed, shuffle

AXIAL_DIRECTIONS = [(0, 1), (1, 0), (0, -1), (-1, 0)]  # Right, down, left, up


# Holds maze data
class MazeState:
    def __init__(
        self, _width, _height, *, _logger: LoggerGroup = LoggerGroup()
    ) -> None:
        self.height = _height
        self.width = _width
        self.logger = _logger
        self.cells = [
            [0 if i % 2 and j % 2 else 1 for j in range(1 + 2 * self.width)]
            for i in range(1 + 2 * self.height)
        ]
        self.usingLog = _logger is not None

    # (x, y)
    def __getitem__(self, loc: tuple[int, int]) -> int:
        val = self.cells[loc[1]][loc[0]]
        self.logger.getCell(self, loc, val)
        return val

    def __setitem__(self, loc: tuple[int, int], val: int) -> None:
        if self.usingLog:
            self.logger.setCell(self, loc, self[loc], val)
        self.cells[loc[1]][loc[0]] = val

    def __repr__(self) -> str:
        return "\n".join(map(lambda row: " ".join(map(str, row)), self.cells))

    def hasAdjacent(self, point: tuple[int, int], val: int) -> bool:
        for direction in AXIAL_DIRECTIONS:
            if self[(point[0] + direction[0], point[1] + direction[1])] == val:
                return True
        return False


# Uses a breadth-first algorithm to generate random maze walls
class MazeGeneratorFactory:
    def __init__(self, _m: MazeState, _seed: int) -> None:
        seed(_seed)
        self.m = _m

    @staticmethod
    def isValidMove(
        next: tuple[int, int], _width: int, _height: int, _visited: list[list[int]]
    ):
        return (
            next[0] >= 0
            and next[0] < _width
            and next[1] >= 0
            and next[1] < _height
            and not _visited[next[0]][next[1]]
        )

    def generate(self) -> MazeState:
        directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]
        self.m.logger.newPhase("GenerateMaze")
        visited = [
            [0 for j in range(1 + 2 * self.m.width)]
            for i in range(1 + 2 * self.m.height)
        ]

        stack = [(0, 0)]
        visited[0][0] = 1

        while len(stack) != 0:
            currentCell = stack.pop()
            shuffle(directions)
            for direction in directions:
                n = (currentCell[0] + direction[0], currentCell[1] + direction[1])
                if MazeGeneratorFactory.isValidMove(
                    n, self.m.width, self.m.height, visited
                ):
                    self.m[
                        (
                            2 * currentCell[0] + 1 + direction[0],
                            2 * currentCell[1] + 1 + direction[1],
                        )
                    ] = 0

                    visited[n[0]][n[1]] = 1
                    stack.append(currentCell)
                    stack.append(n)
                    self.m.logger.endStep(self.m)
                    break
        return self.m


class Path:
    def __init__(self, maze: MazeState) -> None:
        self.maze = maze
        self.path: list[tuple[int, int]] = []

    def add(self, pos: tuple[int, int]) -> None:
        self.path.append(pos)
        self.maze.logger.addToPath(self.maze, pos)

    def remove(self, i=-1) -> None:
        self.path.pop(i)
        self.maze.logger.removeFromPath(self.maze, i)
    def clear(self):
        self.path.clear()
        self.maze.logger.clearPath(self.maze)