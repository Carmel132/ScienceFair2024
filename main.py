from maze.logger import (
    LoggerGroup,
    StepLogger,
    PathLogger,
    PathLogger,
    MazeAction,
    PhaseLogger,
    StateLogger,
)
from sys import setrecursionlimit

setrecursionlimit(10**6)
from maze.state import MazeState, MazeGeneratorFactory
from maze.algorithms import (
    RightHandRule,
    Tremaux,
    BreadthFirst,
    DepthFirst,
    AStar,
    Dijkstra,
    RecursiveBacktracking,
    GreedyBestFirstSearch,
    GaussianWalkers,
    QLearning,
)

path: list[tuple[int, int]] = []
s = LoggerGroup(PhaseLogger(), StateLogger(), PathLogger(path), StepLogger())

sz = (50, 50)

m = MazeState(sz[0], sz[1], _logger=s)
MazeGeneratorFactory(m, 2).generate()
Tremaux(m).run()
s.clearPath(m)
s.endStep(m)
RightHandRule(m).run()

s.clearPath(m)
AStar(m).run()
# print(s.log)
from engine.render.generate_screen_data import generateScreenData
from maze.state import MazeState
from engine.render.maze_renderer import MazeRenderer
import pygame as pg
from engine.player.log_groups import generatePhasePlayer
from engine.render.path_renderer import PathRenderer


class Game:
    def __init__(self):
        pass

    def run(self) -> None:
        pg.init()
        screen = pg.display.set_mode((800, 800))
        pg.display.set_caption("Maze")

        maze = MazeState(sz[0], sz[1])
        screenData = generateScreenData(screen, maze)
        rend = MazeRenderer(screenData, maze)
        pathRend = PathRenderer(screenData, path)
        act = generatePhasePlayer(maze, m.logger.log)

        # act.getCurrent().getCurrent().getRenderer().start(screenData)

        def onUp():
            ...
            # act.getCurrent().end()

            # act.getCurrent().getCurrent().getCurrent().getRenderer().start(screenData)

        def onRight():
            # act.getCurrent().getCurrent().end()
            act.next()
            # act.getCurrent().getCurrent().getCurrent().getRenderer().start(screenData)

            # Events

        while True:
            # Events
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    return
                if event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE:
                    return
                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_RIGHT:
                        # onRight()
                        act.next()
                        # print(path)
                    if event.key == pg.K_LEFT:
                        act.prev()
                    if event.key == pg.K_UP:
                        onUp()
            onRight()
            # Render
            # pg.display.flip()
            screen.fill((0, 0, 0))
            rend.render()
            pathRend.render()
            act.getCurrent().getCurrent().getRenderer().frame()
            pg.display.update()


Game().run()
