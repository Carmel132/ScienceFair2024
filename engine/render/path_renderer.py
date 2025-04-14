from .screen_data import ScreenData
from maze.state import MazeState
import pygame as pg

class PathRenderer:
    def __init__(self, _screenData: ScreenData, _path: list[tuple[int,int]]) -> None:
        self.screenData = _screenData
        self.path = _path
    def render(self) -> None:
        for loc in self.path:
            pg.draw.rect(
                self.screenData.screen,
                (0, 0, 255),
                self.screenData.cellRects[loc[0]][loc[1]],
            )