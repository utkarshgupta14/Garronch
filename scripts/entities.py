import pygame

class PhysicsEntity:
    def __init__(self, game, e_type, pos, size):
        self.game = game
        self.type = e_type
        self.pos = list(pos)
        self.size = size
        self.velocity = [0,0]
        self.collisions = {'up' : False, 'down' : False, 'right' : False, 'left' : False}

        self.action = ''
        self.anim_offset = (-3, -3)
        self.flip = False
        self.set_action('idle') 
        self.last_movement = [0, 0]

    def rect(self):
        return pygame.Rect(self.pos[0], self.pos[1], self.size[0], self.size[1])
    
    def set_action(self, action):
       if action != self.action:
           self.action = action
           self.animation = self.game.assets[self.type + '/' + action].copy()

    def update(self, tilemap, movement=(0,0)):
        self.collisions = {'up' : False, 'down' : False, 'right' : False, 'left' : False}

        frame_movement = (movement[0] + self.velocity[0], movement[1] + self.velocity[1])

        # checking collisions
        self.pos[0] += frame_movement[0]
        entity_rect = self.rect()
        for rect in tilemap.physics_rects_around(self.pos):
            if entity_rect.colliderect(rect):
                if frame_movement[0] > 0:
                    entity_rect.right = rect.left
                    self.collisions['right'] = True
                if frame_movement[0] < 0:
                    entity_rect.left = rect.right
                    self.collisions['left'] = True
                self.pos[0] = entity_rect.x

        self.pos[1] += frame_movement[1]
        entity_rect = self.rect()
        for rect in tilemap.physics_rects_around(self.pos):
            if entity_rect.colliderect(rect):
                if frame_movement[1] > 0:
                    entity_rect.bottom = rect.top
                    self.collisions['down'] = True
                if frame_movement[1] < 0:
                    entity_rect.top = rect.bottom
                    self.collisions['up'] = True
                self.pos[1] = entity_rect.y

        self.velocity[1] = min(5, self.velocity[1] + 0.1)

        if movement[0] > 0:
            self.flip = False
        if movement[0] < 0:
            self.flip = True

        self.last_movement = movement

        if self.collisions['down'] or self.collisions['up']:
            self.velocity[1] = 0

        # animation update
        self.animation.update()

    def render(self, surf, offset=(0, 0)):
        surf.blit(pygame.transform.flip(self.animation.img(), self.flip, False), (self.pos[0] - offset[0] + self.anim_offset[0], self.pos[1] - offset[1] + self.anim_offset[1]))

class Player(PhysicsEntity):
    def __init__(self, game,  pos, size):
        super().__init__(game, 'player', pos, size)
        self.air_time = 0
        self.jumps = 1
        self.wall_slide = False

    def update(self, tilemap, movement):
        super().update(tilemap, movement)

        self.air_time+=1
        if self.collisions['down']:
            self.air_time = 0
            self.jumps = 1
            
        self.wall_slide = False
        if(self.collisions['right'] or self.collisions['left']) and self.air_time>4:
            self.wall_slide = True
            self.velocity[1] = min(self.velocity[1], 0.5)  
            if self.collisions['right']:
                self.flip = False  
            else:
                self.flip = True
            self.set_action('wall_slide')
        elif self.air_time > 4:
            self.set_action('jump')
        elif movement[0] != 0:
            self.set_action('run')
        else:
            self.set_action('idle') 

        if self.velocity[0] > 0:
            self.velocity[0] = max(self.velocity[0]-0.1, 0)
        else:
            self.velocity[0] = min(self.velocity[0]+0.1, 0)

    def jump(self):
        if self.wall_slide:
            if self.flip and self.last_movement[0]<0:
                self.velocity[1] = -2.5
                self.velocity[0] = 3.5
                self.air_time = 5
                self.jumps = max(self.jumps-1, 0)
                return True
            
            elif not self.flip and self.last_movement[0]>0:
                self.velocity[1] = -2.5
                self.velocity[0] = -3.5
                self.air_time = 5
                self.jumps = max(self.jumps-1, 0)
                return True

        elif self.jumps>0:
            self.velocity[1] = -3
            self.air_time = 5
            self.jumps-=1
            return True