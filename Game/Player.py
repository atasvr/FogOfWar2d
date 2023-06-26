from Engine.GameObject import GameObject
import pygame
from Engine.EngineTime import EngineTime


class Player(GameObject):
    speed = 300
    def BeginPlay(self):
        print("begin play player")

    def Update(self):
        keys = pygame.key.get_pressed()
        screensize = pygame.display.get_surface().get_size()
        width = screensize[0]
        height = screensize[1]

        print("x :" + str(self.x) + "y : " + str(self.y) )

        if keys[pygame.K_a] and self.x > 0:
            self.x -= self.speed * EngineTime.deltaTime

        if keys[pygame.K_d] and self.x < width - 10:
            self.x += self.speed * EngineTime.deltaTime

        if keys[pygame.K_w] and self.y > 0:
            self.y -= self.speed * EngineTime.deltaTime

        if keys[pygame.K_s] and self.y < height - 10:
            self.y += self.speed * EngineTime.deltaTime

    def Render(self):
        pygame.draw.rect(pygame.display.get_surface(), (255, 0, 0),
                         (self.x, self.y, 10, 10))
