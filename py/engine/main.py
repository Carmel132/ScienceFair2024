import pygame as pg

WHITE = (255, 255, 255)
BLUE = (0, 0, 255)


def main():
    pg.init()
    screen = pg.display.set_mode()
    rs = [pg.Rect((20, 20), (20, 20)), pg.Rect((30, 30), (20, 20))]
    i = 0
    while True:
        # get input
        for event in pg.event.get():
            if event.type == pg.QUIT:
                return
            if event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE:
                return
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_LEFT:
                    i -= 1
                elif event.key == pg.K_RIGHT:
                    i += 1

        screen.fill(WHITE)

        pg.draw.rect(screen, BLUE, rs[i])
        pg.display.update()


main()
