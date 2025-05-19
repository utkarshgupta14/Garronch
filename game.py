import sys
import pygame

class Game():
    def __init__(self):
        pygame.init()

        pygame.display.set_caption('Garronch')
        self.screen = pygame.display.set_mode((600, 480))

        self.clock = pygame.time.Clock()

        self.bg_color = (14, 150, 170)

        self.img = pygame.image.load("data/images/clouds/cloud_1.png")
        self.img_pos = [270, 220]
        self.img.set_colorkey((0,0,0))

        self.movement = [False, False, False, False]

        self.collision_area = pygame.Rect(400, 350, 100, 50)
    
    def run(self):
        while True:
            self.screen.fill(self.bg_color)

            img_r = pygame.Rect(*self.img_pos, *self.img.get_size())
            if img_r.colliderect(self.collision_area):
                pygame.draw.rect(self.screen, (0, 200, 200), self.collision_area)
            else:
                pygame.draw.rect(self.screen, (14, 170, 190), self.collision_area)

            self.img_pos[1] += (self.movement[1] - self.movement[0]) * 8
            self.img_pos[0] += (self.movement[3] - self.movement[2]) * 10
            self.screen.blit(self.img, self.img_pos)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        self.movement[0] = True
                    if event.key == pygame.K_DOWN:
                        self.movement[1] = True
                    if event.key == pygame.K_LEFT:
                        self.movement[2] = True
                    if event.key == pygame.K_RIGHT:
                        self.movement[3] = True
                    
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_UP:
                        self.movement[0] = False
                    if event.key == pygame.K_DOWN:
                        self.movement[1] = False
                    if event.key == pygame.K_LEFT:
                        self.movement[2] = False
                    if event.key == pygame.K_RIGHT:
                        self.movement[3] = False

            pygame.display.update()
            self.clock.tick(60)


Game().run()