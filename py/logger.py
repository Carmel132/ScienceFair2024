from copy import deepcopy
from dataclasses import dataclass
from enum import Enum


class MazeAction:
    def run(self, maze): ...
    def reverse(self, maze): ...
    class ActionTypes(Enum):
        SETCELL = 1

        def __repr__(self) -> str:
            return self.name

    TYPE: ActionTypes

    def __repr__(self) -> str:
        return ", ".join(f"{key}={repr(item)}" for (key, item) in self.__dict__.items())


def MazeActionClass(cls):
    originalRepr = cls.__repr__ if hasattr(cls, "__repr__") else None

    class Wrapped(cls):
        def __repr__(self) -> str:
            return (
                super().__repr__() if originalRepr else super(Wrapped, self).__repr__()
            )

    return Wrapped


@MazeActionClass
@dataclass
class SetCell(MazeAction):
    loc: tuple[int, int]
    old: int
    new: int

    TYPE: MazeAction.ActionTypes = MazeAction.ActionTypes.SETCELL

    def run(self, maze):
        maze.cells[self.loc[0]][self.loc[1]] = self.new

    def reverse(self, maze):
        maze.cells[self.loc[0]][self.loc[1]] = self.old

    def __repr__(self) -> str:
        return super().__repr__()


class Logger:
    def setCell(self, maze, loc: tuple[int, int], old: int, new: int): ...


class StateLogger(Logger):
    def __init__(self) -> None:
        self.log: list[MazeAction] = []

    def setCell(self, maze, loc: tuple[int, int], old: int, new: int):
        self.log.append(SetCell(loc, old, new))


class LoggerGroup(Logger):
    def __init__(self, *_logs) -> None:
        self.log = []
        self.logs = _logs
        for log in self.logs:
            log.log = self.log

    def setCell(self, maze, loc: tuple[int, int], old: int, new: int):
        for log in self.logs:
            log.setCell(maze, loc, old, new)


s = SetCell((1, 1), 1, 1)
print(s)
