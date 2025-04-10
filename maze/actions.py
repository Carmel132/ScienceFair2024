# Defines basic operation on MazeState
from dataclasses import dataclass
from enum import Enum
from engine.render.action_renderer import ActionRenderer

import pygame as pg


class MazeAction:
    def run(self, maze): ...
    def reverse(self, maze): ...

    def getRenderer(self) -> ActionRenderer:
        return ActionRenderer()

    class ActionTypes(Enum):
        SETCELL = 1
        STEPDIVIDER = 2
        GETCELL = 3
        ADDTOPATH = 4
        PHASEDIVIDER = 5
        REMOVEFROMPATH = 6

        def __repr__(self) -> str:
            return self.name

    TYPE: ActionTypes

    def __repr__(self) -> str:
        return ", ".join(f"{key}={repr(item)}" for (key, item) in self.__dict__.items())


# Action for modifying cell value
@dataclass(repr=False)
class SetCell(MazeAction):
    loc: tuple[int, int]
    old: int
    new: int

    TYPE: MazeAction.ActionTypes = MazeAction.ActionTypes.SETCELL

    def run(self, maze):
        maze.cells[self.loc[1]][self.loc[0]] = self.new

    def reverse(self, maze):
        maze.cells[self.loc[1]][self.loc[0]] = self.old

    def __repr__(self) -> str:
        return super().__repr__()


class StepDivider(MazeAction):
    TYPE: MazeAction.ActionTypes = MazeAction.ActionTypes.STEPDIVIDER

    def __repr__(self) -> str:
        return "---"


@dataclass(repr=False)
class PhaseDivider(MazeAction):
    name: str
    TYPE: MazeAction.ActionTypes = MazeAction.ActionTypes.PHASEDIVIDER

    def __repr__(self) -> str:
        return ">>> " + self.name


@dataclass(repr=False)
class GetCell(MazeAction):
    loc: tuple[int, int]
    val: int
    TYPE: MazeAction.ActionTypes = MazeAction.ActionTypes.GETCELL

    def __repr__(self) -> str:
        return super().__repr__()

    def __post_init__(self) -> None:
        self.renderer = GetCellRenderer(self)

    def getRenderer(self):
        return self.renderer


@dataclass(repr=False)
class AddToPath(MazeAction):
    loc: tuple[int, int]

    TYPE: MazeAction.ActionTypes = MazeAction.ActionTypes.ADDTOPATH

    def __repr__(self) -> str:
        return super().__repr__()


@dataclass(repr=False)
class RemoveFromPath(MazeAction):
    i: int

    TYPE: MazeAction.ActionTypes = MazeAction.ActionTypes.REMOVEFROMPATH


class GetCellRenderer(ActionRenderer):
    def __init__(self, _action: GetCell):
        self.action = _action

    def start(self, _screenData) -> None:
        self.screenData = _screenData

    def frame(self) -> None:
        pg.draw.rect(
            self.screenData.screen,
            (255, 0, 0),
            self.screenData.cellRects[self.action.loc[0]][self.action.loc[1]],
        )
