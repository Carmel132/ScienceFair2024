from render.screen_data import ScreenData
from state import MazeState
from render.maze_renderer import MazeRenderer
import pygame as pg


class Game:
    def __init__(self):
        pass

    def run() -> None:
        pg.init()
        screen = pg.display.set_mode()
        maze = MazeState(6, 6)
        rend = MazeRenderer(ScreenData.generateScreenData(screen, maze), maze)
        while True:
            # Events
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    return
                if event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE:
                    return

            # Render
            rend.render()
            pg.display.update()
