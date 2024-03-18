import pygame
import constants

def draw(DISPLAYSURF, atck_thresh):
    for i, item in enumerate(constants.connections):
        if (i >= atck_thresh):
            color = "red"
        else:
            color = "blue"
        draw_item(DISPLAYSURF, item, color)

# Stupid func
# What's the diff between the top one and the bottom one?
def draw_items(DISPLAYSURF, connections, vertices, color = "red"):
    for item in connections:
        draw_item(DISPLAYSURF, item, color, vertices)

# Takes in tuple with vertices and a vertice list
def draw_item(DISPLAYSURF, item, color = "red", vertices = constants.transformed_vertices):
    start_point = (vertices[item[0]-1]['x'], vertices[item[0]-1]['y'])
    end_point = (vertices[item[1]-1]['x'], vertices[item[1]-1]['y'])
    pygame.draw.aaline(DISPLAYSURF, pygame.Color(color), start_point, end_point)

def is_bounding_box(a, b):
    # right edge of b; right edge of a; top edge of b; top edge of a 
    return (a['x'] < b['x'] + b['width'] and a['x'] + a['width'] > b['x'] and a['y'] < b['y'] + b['height'] and a['y'] + a['height'] > b['y'])

def line_box_collision(line, box):
    line2 = {
        'x': line[0]['x'],
        'y': line[0]['y'],
        'width': line[1]['x'] - line[0]['x'],
        'height': line[1]['y'] - line[0]['y']
    }
    return is_bounding_box(line2, box)

class Collisons():
    def __init__(self):
        self.inbounding = []

    def update_in_bounding(self, x, y, w, h):
        for line in constants.connections:
            line2 = [
                constants.transformed_vertices[line[0]-1],
                constants.transformed_vertices[line[1]-1]
            ]
            if (line_box_collision(line2, {'x': x, 'y': y, 'width': w, 'height': h})):
                self.inbounding.append(line)
    
    def find_collisions(self, x, y, w, h):
        for item in self.inbounding:
            if (colliding(item, x, y, w, h)):
                return True
        return False

# 1. checks if in bounding box, 2. finds intersection for all for faces of box
# 3. checks if intersection within box
def colliding(connection, x, y, w, h):
    v1 = constants.transformed_vertices[connection[0]-1]
    v2 = constants.transformed_vertices[connection[1]-1]
    in_bounding_box = line_box_collision([v1, v2], {'x': x, 'y': y, 'width': w, 'height': h})
    if (not in_bounding_box):
        return False

    l_w = v2['x'] - v1['x']
    l_h = v2['y'] - v1['y']
    if (not l_w or not l_h):
        return in_bounding_box
    # x check(left to right) * h / w + y
    tmp = (x - v1['x']) * l_h / l_w + v1['y']
    # y check(top to bottom) * w / h + x
    tmp1 = (y - v1['y']) * l_w / l_h + v1['x']
    if (tmp <= y and tmp >= y - h):
        return True
    if (tmp1 >= x and tmp1 <= x + h):
        return True
    # x check(right to right) * h / w + y
    tmp = (x + h - v1['x']) * l_h / l_w + v1['y']
    # y check(bottom to bottom) * w / h + x
    tmp1 = (y - h - v1['y']) * l_w / l_h + v1['x']
    if (tmp <= y and tmp >= y - h):
        return True
    if (tmp1 >= x and tmp1 <= x + h):
        return True
    return False