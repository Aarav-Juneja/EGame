import pygame
import constants
import attack
import lines

attacks_info = {
    'slash': {
        'duration': 3,
        'stunnable': True,
        'invincible': False
    },
    'upslash': {
        'duration': 3,
        'stunnable': True,
        'invincible': False
    },
    'downslash': {
        'duration': 3,
        'stunnable': True,
        'invincible': False
    },
    'dive': {
        'duration': 1,
        'stunnable': False,
        'invincible': True
    },
    'shockwave': {
        'duration': 4,
        'stunnable': True,
        'invincible': True
    },
    'divestart': {
        'duration': 2,
        'stunnable': True,
        'invincible': False
    },
    'shriek': {
        'duration': 9,
        'stunnable': True,
        'invincible': False
    },
    'dash': {
        'duration': 3,
        'stunnable': False,
        'invincible': True
    }
}

class Player:
    def __init__(self, keybindings= constants.keybindings, color="red"):
        self.keybindings = keybindings
        self.x = 40
        self.y = 40
        self.dy = 0
        self.dx = 0
        self.width = 30
        self.height = 30
        self.color = color
        self.stun = 0
        self.air = 999
        self.space_frames = 0
        self.jumps = 0
        self.attack = ''
        self.attack_cool = 0
        self.dir = 1
        self.invincible = False

        self.collisions = lines.Collisons()

        self.stock = 3

        self.attack_manager = attack.AttackManager(self.x, self.y, self.width, self.height)

    # Use update for items that are continous
    # Use key_pressed for one time items
    def update(self):
        keys = pygame.key.get_pressed()
        self.key_y = keys[self.keybindings['UP']] - keys[self.keybindings['DOWN']]
        self.key_x = keys[self.keybindings['RIGHT']] - keys[self.keybindings['LEFT']]

        if (self.stun < 0 and self.attack not in constants.attacks.keys()):
            if keys[self.keybindings['JUMP']]:
                if self.space_frames > 0:
                    self.dy = 11
                elif self.jumps > 0:
                    self.dy = 8
                    self.jumps -= 1
                self.space_frames -= 1
            else:
                self.space_frames = 0
            if (self.attack_cool <= 0):
                # Help them lose by prioritizing reg attacks over special ones
                if (keys[self.keybindings['ATTACK']]):
                    if (self.key_y == 1):
                        self.attack = 'upslash'
                    elif (self.key_y == -1 and self.air > 0):
                        self.attack = 'downslash'
                    else:
                        self.attack = 'slash'
                elif (keys[self.keybindings['SPECIAL']]):
                    if (bool(self.key_x)):
                        self.attack = 'dash'
                    elif (self.air > 0 and self.key_y == -1):
                        self.attack = 'divestart'
                    elif (self.key_y == 1):
                        self.attack = 'shriek'
                if (self.attack):
                    self.attack_cool = 0
        self.update2()
        # self.attack_manager.update(self.x, self.y, self.attack, self.attack_cool, self.dir)
        self.attack_manager.update2(self)


    def update2(self):
        # If the attack is over
        if (self.attack and self.attack_cool == attacks_info[self.attack]['duration'] or 
            (self.stun > 0 and attacks_info[self.attack]['stunnable'])):
            # Keep going until you hit the ground
            if (self.attack == 'dive' and self.air > 1):
                self.attack_cool = 1
            else:
                # Limit attacks for next 2 frames
                self.attack_cool = 2
                self.attack = ''
                # Shockwave once down
                if (self.attack == 'dive'):
                    self.attack_cool = 0
                    self.attack = 'shockwave'
                # Start the dive if you're still in the start phase
                elif (self.attack == 'divestart'):
                    self.attack = 'dive'
                    self.attack_cool = 0
        elif (self.attack):
            self.attack_cool += 1
        else:
            self.attack_cool -= 1
        self.stun -= 1
        if (self.stun > 0):
            self.dx *= .85
            if (self.dy > 0):
                self.dy *= .85
        else:
            self.dx = self.key_x * 6
        
        controlling_attack = self.attack in constants.attacks.keys()
        if (controlling_attack and constants.attacks[self.attack]['x']):
            self.dx = constants.attacks[self.attack]['x'][self.attack_cool] * self.dir
        if (controlling_attack and constants.attacks[self.attack]['y']):
            self.dy = constants.attacks[self.attack]['y'][self.attack_cool]
        elif not self.invincible:
            self.dy += constants.gravity
        if (self.attack):
            self.invincible = attacks_info[self.attack]['invincible']
        if (self.y > 480 or self.y < 0):
            self.x = constants.default_coords['x']
            self.y = constants.default_coords['y']
            self.dy = 0
            self.stun = 0
            self.percent = 0
            self.stock -= 1

        self.move()

        self.air += 1
        if (self.key_x != 0):
            self.dir = self.key_x
    
    def move(self):
        # Start y logic
        # Get basic box collsions
        self.collisions.update_in_bounding(self.x, self.y + (self.dy if self.dy > 0 else 0), self.width, self.height + abs(self.dy))
        for _ in range(30):
            self.y -= self.dy / 30
            # Fully check if the lines are colliding
            colliding = self.collisions.find_collisions(self.x, self.y, self.width, self.height)
            if (colliding):
                self.move_out_of_collision(0, self.dy)
                break
        # Start x logic
        # Get basic box collsions
        self.collisions.update_in_bounding(self.x + (self.dx if self.dx > 0 else 0), self.y, self.width + abs(self.dx), self.height)
        for _ in range(30):
            self.x += self.dx / 30
            # Fully check if the lines are colliding
            colliding = self.collisions.find_collisions(self.x, self.y, self.width, self.height)
            if (colliding):
                self.move_out_of_collision(self.dx, 0)
                break

    def move_out_of_collision(self, dx, dy):
        for _ in range(30):
            self.y += dy / 10
            self.x -= dx / 10

            # Reenumerate if we're actually colliding
            self.collisions.update_in_bounding(dx, dy, self.width, self.height)
            colliding = self.collisions.find_collisions(self.x, self.y, self.width, self.height)
            if (not colliding):
                if (abs(dx) > 0):
                    self.dx = 0
                if (abs(dy) > 0):
                    if (dy < 0):
                        self.air = 0
                        self.jumps = constants.max_jumps
                    else:
                        self.air = 99
                    self.dy = 0
                return
        

    def key_pressed(self, key):
        if (key == constants.keybindings['JUMP']):
            self.space_frames = 3
    
    def render(self, DISPLAYSURF):
        self.attack_manager.render(DISPLAYSURF)
        pygame.draw.rect(DISPLAYSURF, pygame.Color("red"), (self.x, self.y, self.width, self.height))