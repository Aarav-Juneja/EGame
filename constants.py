import pygame

keybindings = {
    'UP': pygame.K_UP,
    'DOWN': pygame.K_DOWN,
    'LEFT': pygame.K_LEFT,
    'RIGHT': pygame.K_RIGHT,
    'JUMP': pygame.K_l,
    'ATTACK': pygame.K_k,
    'SPECIAL': pygame.K_j,
}

gravity = -1

X = 480
Y = 360

max_jumps = 3

vertices = [
    {'x': -100, 'y': -60},
    {'x': 100, 'y': -60},
    {'x': -80, 'y': -80},
    {'x': 80, 'y': -80},
    {'x': -160, 'y': 0},
    {'x': -50, 'y': 0},
    {'x': 160, 'y': 0},
    {'x': 50, 'y': 0},
    {'x': -55, 'y': 60},
    {'x': 55, 'y': 60},
]

transform_vertices = lambda vertices: [{'x': vertex['x'] + X/2, 'y': -vertex['y'] + Y/2} for vertex in vertices]

transformed_vertices = transform_vertices(vertices)

default_coords = {
    'x': 40,
    'y': 40,
}

hasframes = ['shockwave', 'shriek']

connections = [
    (1,2),
    (1,3),
    (2,4),
    (3,4),
    (5,6),
    (7,8),
    (9,10)
]

pygame.font.init()

fonts = {'freesansbold32': pygame.font.Font('freesansbold.ttf', 32)}

attacks = {
    'dive': {
        'x': [0],
        'y': [-20],
    },
    'shockwave': {
        'x': [0,0,0,0],
        'y': [0,0,0,0],
    },
    'divestart': {
        'x': [0,0],
        'y': [0,0],
    },
    'shriek': {
        'x': [0,0,0,0,0,0,0,0,0],
        'y': [0,0,0,0,0,0,0,0,0],
    },
    'dash': {
        'x': [17,17,17],
        'y': [0,0,0],
    },
}