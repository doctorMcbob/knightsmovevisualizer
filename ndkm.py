"""
I made the knights move visual synthesizer a while back and I had a dream last night
  My dream was a nightmare that I wont get into, but in the end of the dream I was running
  away scrambling for something else to think about and I had a vision...

The following is the knights move color visualizer where the nights can move in n dimensions.

Rather then creating an n-dimensional array (which i could do with the utils from my petri dish) I will
  store positions in sets.

I am thinking a list of sets where index 0 is the starting cell, index 1 is one move away,
  index 2 is 2 moves away, and so on. This means that when adding a cell I will have to look
  at all the sets in the array up to that point....

Anyways lets see how it preforms, and then maybe I change it to an array for faster indexing if
  it seems like this approach sucks.

-wesley, Happy new year 2025

UPDATE: yeah okay so its insanely slow after just 12 iterations its slowing down so much.

I think im going to make an n dimensional array of the drawable map so to speak
  so if the window is only going to show 200 by 200, it should make a 200n "cube"
then we will track the numbers there that are for lookups, and we can then only track
  the deepest knight moves for iteration.
I think that should work?
hmm the problem is then the knights off the array dont stop duplicating...
I adjusted the logic so the knight cannot move off the board, im deciding that isnt
  a violation of mathematical purity considering in regular chess the knight cannot
  leave the board either (so there)
"""
from itertools import permutations, combinations
import pygame
from pygame.locals import *
from copy import deepcopy
import printer

pygame.init()


def ndimensional_array(n, dimensions, filler=None):
    i = 0

    lastlayer = [filler,] * dimensions[i]
    while i < len(dimensions)-1:#i > 0: 
        i +=1 #-= 1
        copy = deepcopy(lastlayer)
        lastlayer = [deepcopy(copy) for _ in range(dimensions[i])]
    return lastlayer

def getAt(multiarray, position):
    axis = len(position)-1
    head = multiarray
    try:
        while axis > 0:
            if position[axis] < 0: return None
            head = head[position[axis]]
            axis -= 1
        if position[axis] < 0: return None
        return head[position[axis]]
    except IndexError:
        return None

def setAt(multiarray, position, value):
    axis = len(position)-1
    head = multiarray
    while axis > 0:
        head = head[position[axis]]
        axis -= 1
    head[position[axis]] = value

try:
    PW = int(input("pixel width (default 4): "))
except ValueError:
    PW = 4

try:
    size = int(input("size (default 115): "))
except ValueError:
    size = 115
W, H = size, size

SCREEN = pygame.display.set_mode((PW * W, PW * H))
HEL16 = pygame.font.SysFont("Helvetica", 16)
dimensions = int(input("dimensions: "))
def make_new(n): return { tuple(W//2 for _ in range(n)) }
HEAD = make_new(dimensions)
BOARD = ndimensional_array(dimensions, tuple(W for _ in range(dimensions)))
number = 0
d1 = int(input("d1: "))
d2 = int(input("d2: "))

setAt(BOARD, tuple(W//2 for _ in range(dimensions)), number)

colalt = 0
def number_to_rgb(number):
    # Use prime numbers to generate a pseudo-random sequence
    prime1 = 37
    prime2 = 71
    prime3 = 29

    #number -= 1  # Adjust to 0-indexed
    red = (colalt + number * prime1) % 256
    green = (colalt + number * prime2) % 256
    blue = (colalt + number * prime3) % 256

    return red, green, blue

def draw_plane(dest, pw, axis1, axis2, idxs):
    """
    a little weird here. imagine a 4 dimensional point as (x, y, z, a)
      axis1 and axis2 are telling us the axis of the plane we are drawing
      idxs will be the indexes across other axis that we are indexed to

    for example, to draw the x, y axis of the 3rd index of the z axis and 1st of the a axis
      we would do (dest, pw, 0, 1, (0, 0, 3, 1))
    so idxs is a tuple of numbers the length of the number of axis we are dealing with,
      and the indexes of idx at the axis1 or axis2 will be ignored.
    """
    dest.fill((255, 255, 255))
    w = dest.get_width() // pw
    h = dest.get_height() // pw
    
    for x in range(w):
        for y in range(h):
            rect = pygame.Rect((x*pw, y*pw), (pw, pw))

            pos = tuple(idxs[i] if i not in (axis1, axis2) else (x if i == axis1 else y) for i in range(len(idxs)))
            number = getAt(BOARD, pos)
            if number is not None:
                rgb = number_to_rgb(number)
                pygame.draw.rect(dest, rgb, rect)

def knight_moves(pos):
    n = len(pos)

    for axis_pair in combinations(range(n), 2):
        for delta1, delta2 in [
                (d1, d2),
                (d2, d1),
                (-d1, d2),
                (d2, -d1),
                (d1, -d2),
                (-d2, d1),
                (-d1, -d2),
                (-d2, -d1),
        ]:
            new_pos = list(pos)
            new_pos[axis_pair[0]] += delta1
            new_pos[axis_pair[1]] += delta2
            if any(d > W or d < 0 for d in new_pos): continue
            yield tuple(new_pos)

def update_board():
    global HEAD, number
    new = set()
    number += 1
    skipped = 0
    for pos in HEAD:
        for new_pos in knight_moves(pos):
            num = getAt(BOARD, new_pos)
            if num is None:
                try:
                    setAt(BOARD, new_pos, number)
                except IndexError:
                    skipped += 1
                    continue
                new.add(new_pos)
    HEAD = new

go = False
indexers = list(W//2 for _ in range(dimensions))
axis1 = 0
axis2 = 1
while __name__ == "__main__":
    draw_plane(SCREEN, PW, 0, 1, tuple(indexers))
    wait = True
    while wait:
        pygame.display.update()
        if go:
            update_board()
            wait = False

        for e in pygame.event.get():
            if e.type == KEYDOWN:
                if e.key == K_ESCAPE: quit()
            
                if e.key == K_SPACE:
                    if not go:
                        update_board()
                    wait = False
                    go = False

                if e.key == K_RETURN:
                    go = True
                    wait = False

                if e.key == K_UP:
                    indexers[2] += 1
                    indexers[2] %= W
                    wait = False

                if e.key == K_DOWN:
                    indexers[2] -= 1
                    indexers[2] %= W
                    wait = False

                if e.key == K_LEFT:
                    axis1 -= 1
                    axis2 -= 1
                    axis1 %= dimensions
                    axis2 %= dimensions
                    wait = False

                if e.key == K_RIGHT:
                    axis1 += 1
                    axis2 += 1
                    axis1 %= dimensions
                    axis2 %= dimensions
                    wait = False

                if e.key == K_w and dimensions > 3:
                    indexers[3] += 1
                    indexers[3] %= W
                    wait = False

                if e.key == K_s and dimensions > 3:
                    indexers[3] -= 1
                    indexers[3] %= W
                    wait = False

                if e.key == K_a and dimensions > 4:
                    indexers[4] += 1
                    indexers[4] %= W
                    wait = False

                if e.key == K_d and dimensions > 4:
                    indexers[4] -= 1
                    indexers[4] %= W
                    wait = False

                if e.key == K_PERIOD:
                    for i in range(W):
                        indexers[2] = i
                        draw_plane(SCREEN, PW, 0, 1, tuple(indexers))
                        printer.save_surface(SCREEN)
                        pygame.display.update()
                    printer.save_em()
                    fname = printer.make_gif(
                        f"ndkm-{d1}x{d2}-d{dimensions}-x{axis1}y{axis2}-{'.'.join([str(i) for i in indexers])}.gif",
                        fps=8)
                    printer.clear_em()
                    print("Saved gif as", fname)
