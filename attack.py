import pygame
import lines
import constants
import attack_connections
import attack_vertices

hasframes = ['shockwave', 'shriek']

class AttackManager:
    def __init__(self, x, y, w, h):
        # connect, vertice, update, hit
        self.x = x
        self.y = y
        self.width = w
        self.height = h
        self.attack = ''
        self.attack_cool = 0
        self.dir = 1

    def render(self, DISPLAYSURF):
        if (not self.attack):
            return
        frame_specific = self.attack in hasframes
        connection_group = attack_connections.connections[self.attack] if not frame_specific else attack_connections.connections[self.attack][self.attack_cool]
        vertice_group = attack_vertices.vertices[self.attack] if not frame_specific else attack_vertices.vertices[self.attack][self.attack_cool]
        reg_vertices = [{'x': vertex[0], 'y': vertex[1]} for vertex in vertice_group]
        transformed_vertices = [{'x': self.dir * vertex['x'], 'y': -vertex['y']} for vertex in reg_vertices]
        moved_vertices = [{'x': self.x + self.width / 2 + vertex['x'], 'y': self.y + self.height / 2 + vertex['y']} for vertex in transformed_vertices]
        lines.draw_items(DISPLAYSURF, connection_group, moved_vertices, "red")

    def update(self, x, y, attack, cool, dir):
        self.x = x
        self.y = y
        self.attack = attack
        self.attack_cool = cool
        self.dir = dir

    def update2(self, player):
        self.x = player.x
        self.y = player.y
        self.attack = player.attack
        self.attack_cool = player.attack_cool
        self.dir = player.dir

"""
Functions and their usage:
add attack:
* push attack to connections
* push vertices to updateverticeidx
* push properties to hitproperties
update level:
* Update vertices with updateverticeidx
clearthingies:
* clear all attack data
"""