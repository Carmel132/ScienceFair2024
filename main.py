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

from engine.render.generate_screen_data import generateScreenData
from maze.state import MazeState
from engine.render.maze_renderer import MazeRenderer
import pygame as pg
from engine.player.log_groups import generatePhasePlayer


class Game:
    def __init__(self):
        pass

    def run(self) -> None:
        pg.init()
        screen = pg.display.set_mode((800, 800))

        maze = MazeState(6, 5)
        screenData = generateScreenData(screen, maze)
        rend = MazeRenderer(screenData, maze)
        act = generatePhasePlayer(maze, m.logger.log)

        act.getCurrent().getCurrent().getCurrent().getRenderer().start(screenData)
        while True:
            # Events
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    return
                if event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE:
                    return
                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_RIGHT:
                        act.getCurrent().getCurrent().end()
                        act.next()
                        act.getCurrent().getCurrent().getCurrent().getRenderer().start(
                            screenData
                        )
                        print(act.getCurrent().getCurrent().actions)
                    if event.key == pg.K_LEFT:
                        act.prev()

            # Render
            pg.display.flip()
            screen.fill((0, 0, 0))
            rend.render()
            act.getCurrent().getCurrent().getCurrent().getRenderer().frame()
            pg.display.update()


Game().run()
