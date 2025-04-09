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
from engine.player.action_group import MazeActionPlayer
import pygame as pg
from engine.player.log_groups import generatePhasePlayer

f = generatePhasePlayer(m, m.logger.log)
print(1)


class Game:
    def __init__(self):
        pass

    def run(self) -> None:
        pg.init()
        screen = pg.display.set_mode((800, 800))
        maze = MazeState(6, 5)
        rend = MazeRenderer(ScreenData.generateScreenData(screen, maze), maze)
        act = MazeActionPlayer(maze, *m.logger.log)
        while True:
            # Events
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    return
                if event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE:
                    return
                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_RIGHT:
                        act.next()
                    if event.key == pg.K_LEFT:
                        act.prev()

            # Render
            pg.display.flip()
            screen.fill((0, 0, 0))
            rend.render()
            pg.display.update()


Game().run()
