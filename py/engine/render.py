import pygame as pg
from dataclasses import dataclass

class Renderer:
    def render() -> None: ...

@dataclass
class ScreenData:
    cellPoints: list[list[tuple[int, int]]]
    cellRects: list[list[pg.Rect]]
    screen: pg.surface.Surface


class MazeRenderer(Renderer):
    def __init__(self, data: ScreenData) -> None:
        self.sd = data

    def render() -> None:
        ...