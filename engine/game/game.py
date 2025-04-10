from render.screen_data import ScreenData
from maze.state import MazeState
from render.maze_renderer import MazeRenderer
from player.action_group import MazeActionPlayer
import pygame as pg


class Game:
    def __init__(self):
        pass
    
    def run() -> None:
        pg.init()
        screen = pg.display.set_mode()
        maze = MazeState(6, 6)
        rend = MazeRenderer(ScreenData.generateScreenData(screen, maze), maze)
        act = MazeActionPlayer(maze, maze.logger.log)
        
        while True:
            # Events
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    return
                if event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE:
                    return
                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_LEFT:
                        act.prev()
                    if event.key == pg.K_RIGHT:
                        act.next()

            # Render
            rend.render()
            pg.display.update()
