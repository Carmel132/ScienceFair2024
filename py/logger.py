from dataclasses import dataclass
from enum import Enum


# Defines basic operation on MazeState
class MazeAction:
    def run(self, maze): ...
    def reverse(self, maze): ...

    class ActionTypes(Enum):
        SETCELL = 1
        STEPDIVIDER = 2
        GETCELL = 3
        ADDTOPATH = 4
        PHASEDIVIDER = 5

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


@MazeActionClass
@dataclass
class PhaseDivider(MazeAction):
    name: str
    TYPE: MazeAction.ActionTypes = MazeAction.ActionTypes.PHASEDIVIDER

    def __repr__(self) -> str:
        return ">>> " + self.name


@MazeActionClass
@dataclass
class GetCell(MazeAction):
    loc: tuple[int, int]
    val: int

    TYPE: MazeAction.ActionTypes = MazeAction.ActionTypes.GETCELL

    def __repr__(self) -> str:
        return super().__repr__()


@MazeActionClass
@dataclass
class AddToPath(MazeAction):
    loc: tuple[int, int]

    TYPE: MazeAction.ActionTypes = MazeAction.ActionTypes.ADDTOPATH

    def __repr__(self) -> str:
        return super().__repr__()


# Basic logger interface
class Logger:
    def setCell(self, maze, loc: tuple[int, int], old: int, new: int): ...
    def getCell(self, maze, loc: tuple[int, int], val: int): ...
    def endStep(self, maze): ...
    def addToPath(self, maze, loc: tuple[int, int]): ...
    def newPhase(self, name: str): ...


# Logger that tracks the state of the Maze
class StateLogger(Logger):
    def __init__(self) -> None:
        self.log: list[MazeAction] = []

    def setCell(self, maze, loc: tuple[int, int], old: int, new: int):
        self.log.append(SetCell(loc, old, new))

    def getCell(self, maze, loc: tuple[int, int], val: int):
        self.log.append(GetCell(loc, val))


class StepLogger(Logger):
    def __init__(self) -> None:
        self.log: list[MazeAction] = []

    def endStep(self, maze):
        self.log.append(StepDivider())


class PathLogger(Logger):
    def __init__(self) -> None:
        self.log: list[MazeAction] = []

    def addToPath(self, maze, loc: tuple[int, int]):
        self.log.append(AddToPath(loc))


class PhaseLogger(Logger):
    def __init__(self) -> None:
        self.log: list[MazeAction] = []

    def newPhase(self, name: str):
        self.log.append(PhaseDivider(name))


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

    def getCell(self, maze, loc: tuple[int, int], val: int):
        for log in self.logs:
            log.getCell(maze, loc, val)

    def endStep(self, maze):
        for log in self.logs:
            log.endStep(maze)

    def addToPath(self, maze, loc: tuple[int, int]) -> None:
        for log in self.logs:
            log.addToPath(maze, loc)

    def newPhase(self, name: str) -> None:
        for log in self.logs:
            log.newPhase(name)
