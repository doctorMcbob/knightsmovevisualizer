import pygame as pg
from pygame.locals import *
pg.init()
import time
import printer

PW = 16
W, H = 151, 151
SCREEN = pg.display.set_mode((PW * W, PW * H + 16))
HEL16 = pg.font.SysFont("Helvetica", 16)

d1 = 1
d2 = 2

offx = 0
offy = 0
LIM = 5

GRID_STATE = {
    (0, 0): 1
}

colalt = 0

last = set()
last.add((0, 0))

def number_to_rgb(number):
    # Use prime numbers to generate a pseudo-random sequence
    prime1 = 37
    prime2 = 71
    prime3 = 29

    number -= 1  # Adjust to 0-indexed
    red = (colalt + number * prime1) % 256
    green = (colalt + number * prime2) % 256
    blue = (colalt + number * prime3) % 256

    return red, green, blue

def draw_grid(dest, pw):
    global colalt
    dest.fill((255, 255, 255))
    for x in range(dest.get_width() // pw):
        for y in range((dest.get_height() - 16) // pw):
            rect2 = pg.Rect((x * pw, y * pw), (pw, pw))

            if (x+offx, y+offy) in GRID_STATE:
                n = GRID_STATE[(x+offx, y+offy)]
                r, g, b = number_to_rgb(n)
                pg.draw.rect(dest, (r, g, b), rect2)
            else:
                pg.draw.rect(dest, (255, 255, 255), rect2)
    dest.blit(
            HEL16.render(f"d1 {d1} d2 {d2}", 0, (0,0,0)),
            (0, dest.get_height() - 16)
    )
    #colalt += 1

def knight_moves(x, y):
    yield x + d2, y + d1
    yield x + d1, y + d2
    yield x - d2, y + d1
    yield x - d1, y + d2
    yield x + d2, y - d1
    yield x + d1, y - d2
    yield x - d2, y - d1
    yield x - d1, y - d2

def update_grid(n, draw=False):
    spots = set()
    for key in last:
        if key not in GRID_STATE:
            print(key, GRID_STATE.keys())
            quit()
        v = GRID_STATE[key]
        if v == n:
            x, y = key
            for square in knight_moves(x, y):
                if square not in GRID_STATE:
                    GRID_STATE[square] = n + 1
                    spots.add(square)
                    if draw:
                        draw_grid(SCREEN, PW)
                        pg.display.update()
                        draw = pg.key.get_mods() & KMOD_SHIFT
                        for e in pg.event.get():
                            if e.type == KEYDOWN and e.key == K_q: quit()
                            handle_window_events(e)
    return spots

def handle_window_events(e):
    global PW, offx, offy

    if e.type == KEYDOWN and e.key == K_m: PW = max(1, PW // 2)
    if e.type == KEYDOWN and e.key == K_n: PW = PW * 2

    if e.type == KEYDOWN and e.key == K_l: offx += 1 + (15 if (pg.key.get_mods() & KMOD_SHIFT) else 0)
    if e.type == KEYDOWN and e.key == K_j: offx -= 1 + (15 if (pg.key.get_mods() & KMOD_SHIFT) else 0)
    if e.type == KEYDOWN and e.key == K_k: offy += 1 + (15 if (pg.key.get_mods() & KMOD_SHIFT) else 0)
    if e.type == KEYDOWN and e.key == K_i: offy -= 1 + (15 if (pg.key.get_mods() & KMOD_SHIFT) else 0)

    if e.type == KEYDOWN and e.key == K_c: # center
        offx = 0-SCREEN.get_width() // PW // 2
        offy = 0-SCREEN.get_height() // PW // 2


def is_prime(n):
    if n <= 1: return False
    for i in range(2, int(n**0.5) + 1):
        if n % i == 0: return False
    return True


def next_prime():
    prime = 2
    while True:
        if is_prime(prime):
            yield prime
        prime += 1

n = 1
while __name__ == "__main__":
    draw_grid(SCREEN, PW)
    pg.display.update()
    for e in pg.event.get():
        if e.type == KEYDOWN and e.key == K_q: quit()

        if e.type == KEYDOWN and e.key == K_LEFT: d1 -= 1
        if e.type == KEYDOWN and e.key == K_RIGHT: d1 += 1 
        if e.type == KEYDOWN and e.key == K_UP: d2 += 1
        if e.type == KEYDOWN and e.key == K_DOWN: d2 -= 1

        if e.type == KEYDOWN and e.key == K_SPACE:
            c = 0
            while c < LIM:
                pg.event.pump()
                last = update_grid(n, draw = not (pg.key.get_mods() & KMOD_SHIFT) )
                n += 1
                print(c, n)
                c += 1
        
        handle_window_events(e)

        if e.type == KEYDOWN and e.key == K_RETURN: 
            fname = f"km:{d1}_{d2}:{str(int(time.time()))}.png"
            pg.image.save(SCREEN, fname)
            print("Saved to ", fname)

        if e.type == KEYDOWN and e.key == K_r: 
            GRID_STATE = {
                (0, 0): 1
            }
            n = 1
            d1 = 1
            d2 = 2
            last = set()
            last.add((0, 0))

            offx = 0
            offy = 0


        if e.type == KEYDOWN and e.key == K_p:
            prime = next_prime()
            d1 = next(prime)

            for i in range(90):
                d2 = next(prime)
                n = 1
                GRID_STATE = {
                    (0, 0): 1
                }
                last = set()
                last.add((0, 0))
                n = 1
                
                while n < LIM:
                    last = update_grid(n)
                    n+=1

                LIM += 10
                draw_grid(SCREEN, PW)
                pg.display.update()
                printer.save_surface(SCREEN)

            printer.save_em()
            printer.make_gif("2prime30fps.gif", 30)
            printer.make_gif("2prime20fps.gif", 20)
            printer.make_gif("2prime10fps.gif", 10)
            printer.clear_em()
