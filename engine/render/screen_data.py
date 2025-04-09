from dataclasses import dataclass
import pygame as pg

from maze.state import MazeState

# Padding about the border of the rendered maze so as to not cover an entire axis
SCREEN_BORDER_PADDING: int = 20


@dataclass
class ScreenData:
    cellPoints: list[list[tuple[int, int]]]
    cellRects: list[list[pg.Rect]]
    screen: pg.Surface

    # Number of cells in grid
    cellWidth: int
    cellHeight: int
    cellEdge: int

    @staticmethod
    def generateCellPoints(
        centerOffset: tuple[int, int], cellWidth: int, cellHeight: int, cellEdge: int
    ) -> list[list[tuple[int, int]]]:
        return list(
            map(
                lambda x: list(
                    map(
                        lambda y: (
                            centerOffset[0] + x * cellEdge,
                            centerOffset[1] + y * cellEdge,
                        ),
                        range(cellHeight),
                    )
                ),
                range(cellWidth),
            )
        )

    @staticmethod
    def generateCellRects(
        cellPoints: list[list[tuple[int, int]]], cellEdge: int
    ) -> list[list[pg.Rect]]:
        return list(
            map(
                lambda cellRow: list(
                    map(
                        lambda p: pg.Rect(p[0], p[1], cellEdge + 1, cellEdge + 1),
                        cellRow,
                    )
                ),
                cellPoints,
            )
        )

    @staticmethod
    def generateScreenData(screen: pg.Surface, maze: MazeState):
        cellWidth = 1 + 2 * maze.width
        cellHeight = 1 + 2 * maze.height

        dx = min(
            (screen.get_height() - 2 * SCREEN_BORDER_PADDING) / cellHeight,
            (screen.get_width() - 2 * SCREEN_BORDER_PADDING) / cellWidth,
        )
        centerOffset = (
            screen.get_width() - cellWidth * dx - SCREEN_BORDER_PADDING,
            screen.get_height() - cellHeight * dx - SCREEN_BORDER_PADDING,
        )
        cellPoints = ScreenData.generateCellPoints(
            centerOffset, cellWidth, cellHeight, dx
        )
        return ScreenData(
            cellPoints,
            ScreenData.generateCellRects(cellPoints, dx),
            screen,
            cellWidth,
            cellHeight,
            dx,
        )
