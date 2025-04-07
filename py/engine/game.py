import render
from render import pg
class Game:
    def __init__(self):
        pass
    def run() -> None:
        pg.init()
        screen = pg.display.set_mode()
        while True:
            # Events
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    return
                if event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE:
                    return
            # Physics

            # Render
            pg.display.update()
