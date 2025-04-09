from .screen_data import ScreenData
from maze.state import MazeState
import pygame as pg


class MazeRenderer:
    def __init__(self, _screenData: ScreenData, _maze: MazeState) -> None:
        self.screenData = _screenData
        self.height = _screenData.screen.get_height()
        self.width = _screenData.screen.get_width()
        self.maze = _maze

    def render(self) -> None:
        for i in range(1 + 2 * self.maze.width):
            for j in range(1 + 2 * self.maze.height):
                pathAroundOddEntry = (i % 2 and j % 2) and not self.maze.hasAdjacent(
                    (i, j), 0
                )
                if self.maze[(i, j)] or pathAroundOddEntry:
                    pg.draw.rect(
                        self.screenData.screen,
                        (255, 255, 255),
                        self.screenData.cellRects[i][j],
                    )
