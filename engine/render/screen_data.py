from dataclasses import dataclass
import pygame as pg


@dataclass
class ScreenData:
    cellPoints: list[list[tuple[int, int]]]
    cellRects: list[list[pg.Rect]]
    screen: pg.Surface

    # Number of cells in grid
    cellWidth: int
    cellHeight: int
    cellEdge: int
