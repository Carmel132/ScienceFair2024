from maze.logger import (
    LoggerGroup,
    StateLogger,
    StepLogger,
    PathLogger,
    MazeAction,
    PhaseLogger,
)


from maze.state import MazeState, MazeGeneratorFactory
from maze.algorithms import RightHandRule

s = LoggerGroup(PhaseLogger(), StateLogger(), PathLogger(), StepLogger())
m = MazeState(6, 5, _logger=s)
MazeGeneratorFactory(m, 4).generate()
RightHandRule(m).run()

print(s.log)

from engine.render.screen_data import ScreenData
from maze.state import MazeState
from engine.render.maze_renderer import MazeRenderer
import pygame as pg


class Game:
    def __init__(self):
        pass

    def run(self) -> None:
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
Game().run()