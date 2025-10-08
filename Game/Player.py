from __future__ import annotations

import pygame

from Engine.EngineTime import EngineTime
from Engine.GameObject import GameObject


class Player(GameObject):
    teamId = 0
    speed = 100
    radius = 20
    size = 8

    def BeginPlay(self) -> None:
        print("BeginPlay : " + self.name)

    def Update(self) -> None:
        keys = pygame.key.get_pressed()
        width, height = pygame.display.get_surface().get_size()

        if keys[pygame.K_a]:
            self.x = max(0, self.x - self.speed * EngineTime.deltaTime)

        if keys[pygame.K_d]:
            self.x = min(width - self.size, self.x + self.speed * EngineTime.deltaTime)

        if keys[pygame.K_w]:
            self.y = max(0, self.y - self.speed * EngineTime.deltaTime)

        if keys[pygame.K_s]:
            self.y = min(height - self.size, self.y + self.speed * EngineTime.deltaTime)

    def Render(self) -> None:
        surface = pygame.display.get_surface()
        self.render = pygame.draw.rect(surface, (255, 0, 0), (self.x, self.y, self.size, self.size))