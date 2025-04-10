from maze.actions import (
    MazeAction,
    GetCell,
    RemoveFromPath,
    SetCell,
    StepDivider,
    AddToPath,
    PhaseDivider,
)


# Basic logger interface
class Logger:
    def setCell(self, maze, loc: tuple[int, int], old: int, new: int): ...
    def getCell(self, maze, loc: tuple[int, int], val: int): ...
    def endStep(self, maze): ...
    def addToPath(self, maze, loc: tuple[int, int]): ...
    def removeFromPath(self, maze, i: int): ...
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
    def __init__(self, _path: list[tuple[int, int]]) -> None:
        self.log: list[MazeAction] = []
        self.path = _path

    def addToPath(self, maze, loc: tuple[int, int]):
        a = AddToPath(loc)
        a.path = self.path
        self.log.append(a)

    def removeFromPath(self, maze, i: int = -1):
        a = RemoveFromPath(i)
        a.path = self.path
        self.log.append(a)


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

    def removeFromPath(self, maze, i: int) -> None:
        for log in self.logs:
            log.removeFromPath(maze, i)

    def newPhase(self, name: str) -> None:
        for log in self.logs:
            log.newPhase(name)
