# Defines basic operation on MazeState
from dataclasses import dataclass, field
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
        CLEARPATH = 7

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
    path: list[tuple[int, int]] = field(repr=False, init=False)
    TYPE: MazeAction.ActionTypes = MazeAction.ActionTypes.ADDTOPATH

    def run(self, maze):
        self.path.append(self.loc)

    def reverse(self, maze):
        self.path.pop()

    def __repr__(self) -> str:
        return super().__repr__()


@dataclass(repr=False)
class RemoveFromPath(MazeAction):
    i: int
    path: list[tuple[int, int]] = field(repr=False, init=False)
    TYPE: MazeAction.ActionTypes = MazeAction.ActionTypes.REMOVEFROMPATH

    # TODO: Make the [RemoveFromPath] class store what it removes so that it can reverse the action
    def run(self, maze):
        self.storeRemoved = self.path.pop(self.i)
    def reverse(self, maze):
        try:
            self.path.append(self.i, self.storeRemoved)
        except AttributeError:
            print("Tried to undo remove when nothing to undo")

@dataclass(repr=False)
class ClearPath(MazeAction):
    path: list[tuple[int, int]] = field(repr=False, init=False)
    TYPE: MazeAction.ActionTypes = MazeAction.ActionTypes.CLEARPATH
    def run(self, maze):
        print(2)
        from copy import deepcopy
        self.storePath = deepcopy(self.path)
        self.path.clear()
    def reverse(self, maze):
        try:
            self.path.extend(self.storePath)
        except AttributeError:
            pass

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
