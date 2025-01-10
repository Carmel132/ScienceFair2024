from dataclasses import dataclass
from enum import Enum


# Defines basic operation on MazeState
class MazeAction:
    def run(self, maze): ...
    def reverse(self, maze): ...
    class ActionTypes(Enum):
        SETCELL = 1
        STEPDIVIDER = 2

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


# Action for modifying cell value
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


@MazeActionClass
class StepDivider(MazeAction):
    TYPE: MazeAction.ActionTypes = MazeAction.ActionTypes.STEPDIVIDER

    def __repr__(self) -> str:
        return "---"


# Basic logger interface
class Logger:
    def setCell(self, maze, loc: tuple[int, int], old: int, new: int): ...
    def endStep(self, maze): ...


# Logger that tracks the state of the Maze
class StateLogger(Logger):
    def __init__(self) -> None:
        self.log: list[MazeAction] = []

    def setCell(self, maze, loc: tuple[int, int], old: int, new: int):
        self.log.append(SetCell(loc, old, new))


class StepLogger(Logger):
    def __init__(self) -> None:
        self.log: list[MazeAction] = []

    def endStep(self, maze):
        self.log.append(StepDivider())


# Holds Logger objects, then calls their respective methods
class LoggerGroup(Logger):
    def __init__(self, *_logs) -> None:
        self.log = []
        self.logs = _logs
        for log in self.logs:
            log.log = self.log

    def setCell(self, maze, loc: tuple[int, int], old: int, new: int):
        for log in self.logs:
            log.setCell(maze, loc, old, new)

    def endStep(self, maze):
        for log in self.logs:
            log.endStep(maze)
