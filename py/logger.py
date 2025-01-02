from typing import override
from copy import deepcopy


class Logger:
    def setCell(_, maze, loc: tuple[int, int], old: int, new: int): ...


class StateLogger(Logger):
    def __init__(_) -> None:
        _.log = []

    def setCell(_, maze, loc: tuple[int, int], old: int, new: int):
        _.log.append(deepcopy(maze.cells))
