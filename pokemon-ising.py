import pygame
import random
import numpy as np
import sys

FPS = 11

CELL_SIZE = 10
HEIGHT = 100
WIDTH = 100
WINDOW_HEIGHT = HEIGHT * CELL_SIZE
WINDOW_WIDTH = WIDTH * CELL_SIZE

NORMAL = 0
FIGHT = 1
FLYING = 2
POISON = 3
GROUND = 4
ROCK = 5
BUG = 6
GHOST = 7
FIRE = 8
WATER = 9
GRASS = 10
ELECTR = 11
PSYCHC = 12
ICE = 13
DRAGON = 14
TYPES = list(range(15))

T = 1 # supereffective
O = 3 # normal
H = 5 # not effective
I = 9 # immune

TYPE_CHART = [
        [O,T,O,O,O,O,O,I,O,O,O,O,O,O,O], # normal
        [O,O,T,O,O,H,H,O,O,O,O,O,T,O,O], # fight
        [O,H,O,O,I,T,H,O,O,O,H,T,O,T,O], # flying
        [O,H,O,H,T,O,T,O,O,O,H,O,T,O,O], # poison
        [O,O,O,H,O,H,O,O,O,T,T,I,O,T,O], # ground
        [H,T,H,H,T,O,O,O,H,T,T,O,O,O,O], # rock
        [O,H,T,T,H,T,O,O,T,O,H,O,O,O,O], # bug
        [I,I,O,H,O,O,H,T,O,O,O,O,O,O,O], # ghost
        [O,O,O,O,T,T,H,O,H,T,H,O,O,O,O], # fire
        [O,O,O,O,O,O,O,O,H,H,T,T,O,H,O], # water
        [O,O,T,T,H,O,T,O,T,H,H,H,O,T,O], # grass
        [O,O,H,O,T,O,O,O,O,O,O,H,O,O,O], # electr
        [O,H,O,O,O,O,T,I,O,O,O,O,H,O,O], # psychc
        [O,T,O,O,O,T,O,O,T,O,O,O,O,H,O], # ice
        [O,O,O,O,O,O,O,O,H,H,H,H,O,T,T]  # dragon
    ]

COLORS = {
        NORMAL : (168,170,114),
        FIGHT : (196,44,23),
        FLYING : (168,138,246),
        POISON : (162,55,164),
        GROUND : (226,194,89),
        ROCK : (186,162,26),
        BUG : (168,188,0),
        GHOST : (112,84,156),
        FIRE : (244,128,0),
        WATER : (100,139,246),
        GRASS : (114,204,62),
        ELECTR : (250,211,0),
        PSYCHC : (254,82,134),
        ICE : (148,216,218),
        DRAGON : (112,13,255)
    }

def init_grid():
    return np.random.randint(0, 15, size=(HEIGHT,WIDTH))

def neighborhood(grid, point):
    neighbors = []
    for i in [-1,0,1]:
        for j in [-1,0,1]:
            if (i,j) != (0,0):
                x = (point[0] + i) % WIDTH
                y = (point[1] + j) % HEIGHT
                neighbors.append(grid[x,y])
    return neighbors

def fight(p_type, neighbors):
    bo = {'type':p_type, 'eff':I, 'num':0} # best opponent
    effs = TYPE_CHART[p_type] # effects
    for opponent in TYPES:
        num = len([x for x in neighbors if x == opponent])
        eff = effs[opponent]
        if num >= eff:
            if bo['eff'] == eff and bo['num'] == num:
                # if best and current opponents are the same choose randomly
                bo['type'] = random.choice([bo['type'], opponent])
            if bo['eff'] == eff and bo['num'] < num:
                # if they have the same strength but the current opponent has
                # a higher number of neighbors, choose the current opponent
                bo['type'] = opponent
                bo['num'] = num
            if bo['eff'] > eff:
                # if the current opponent has higher strength than the best
                # opponent, choose the current opponent
                bo['type'] = opponent
                bo['eff'] = eff
                bo['num'] = num
    return bo['type']

def update_grid(grid):
    for i in range(WIDTH):
        for j in range(HEIGHT):
            grid[j,i] = fight(grid[j,i], neighborhood(grid, (i,j)))
    return grid

def draw_grid(grid):
    for i in range(WIDTH):
        for j in range(HEIGHT):
            color = COLORS[grid[j,i]]
            x = j * CELL_SIZE
            y = i * CELL_SIZE
            rect = pygame.Rect(x, y, CELL_SIZE, CELL_SIZE)
            pygame.draw.rect(canvas, color, rect)

pygame.init()
clock = pygame.time.Clock()
canvas = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Pokemon Ising Model")
animate = True
exit = False

grid = init_grid()

export = False
counter = 0
if len(sys.argv) == 3:
    if sys.argv[1] == "--export": 
        export = True
        frame_name = sys.argv[2] + "/frame_{0:05d}.png"

while not exit:

    if export:
        pygame.image.save(canvas, frame_name.format(counter))
        counter += 1

    clock.tick(FPS)

    if animate:
        grid = update_grid(grid)
        draw_grid(grid)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit = True
        if event.type == pygame.KEYDOWN:
            if event.unicode == 'q':
                exit = True
            if event.unicode == ' ':
                animate = not animate
            if event.key == 1073741906: # Up arrow
                FPS = min(61, FPS + 5)
            if event.key == 1073741905: # Down arrow
                FPS = max(1, FPS - 5)

    pygame.display.update()
