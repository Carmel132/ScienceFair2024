from logger import Logger, LoggerGroup, StateLogger
from random import seed, shuffle


class MazeState:
    def __init__(_, _height, _width, _logger: LoggerGroup) -> None:
        _.height = _height
        _.width = _width
        _.logger = _logger
        _.cells = [
            [0 if i % 2 and j % 2 else 1 for j in range(1 + 2 * _.width)]
            for i in range(1 + 2 * _.height)
        ]

    def __getitem__(_, loc: tuple[int, int]) -> int:
        return _.cells[loc[0]][loc[1]]

    def __setitem__(_, loc: tuple[int, int], val: int) -> None:
        _.logger.setCell(_, loc, _[loc], val)
        _.cells[loc[0]][loc[1]] = val

    def __repr__(_) -> str:
        return "\n".join(map(lambda row: " ".join(map(str, row)), _.cells))


# Uses a breadth-first algorithm to generate random maze walls
class MazeGeneratorFactory:
    directions = [(1, 0), (0, -1), (-1, 0), (0, 1)]  # Right, down, left, up

    def __init__(_, _m: MazeState, _seed: int) -> None:
        seed(_seed)
        _.m = _m
        _.directions = MazeGeneratorFactory.directions

    @staticmethod
    def isValidMove(
        next: tuple[int, int], _height: int, _width: int, _visited: list[list[int]]
    ):
        return (
            next[0] >= 0
            and next[0] < _width
            and next[1] >= 0
            and next[1] < _height
            and not _visited[next[0]][next[1]]
        )

    def generate(_) -> MazeState:
        visited = [
            [0 for j in range(1 + 2 * _.m.width)] for i in range(1 + 2 * _.m.height)
        ]

        stack = [(0, 0)]
        visited[0][0] = 1

        while len(stack) != 0:
            currentCell = stack.pop()
            shuffle(_.directions)
            for direction in _.directions:
                n = (currentCell[0] + direction[0], currentCell[1] + direction[1])
                if MazeGeneratorFactory.isValidMove(n, _.m.height, _.m.width, visited):
                    _.m[
                        (
                            2 * currentCell[0] + 1 + direction[0],
                            2 * currentCell[1] + 1 + direction[1],
                        )
                    ] = 0

                    visited[n[0]][n[1]] = 1
                    stack.append(currentCell)
                    stack.append(n)
                    break
        return _.m
