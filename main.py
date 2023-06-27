import pygame
from Game.Player import Player
from Engine.EngineTime import EngineTime
import math

from Game.TerrainManager import VisionGrid,Part,Terrain

pygame.init()

win = pygame.display.set_mode((500,
                               500))

pygame.display.set_caption("FogOfWar")

run = True
getTicksLastFrame = 0

player = Player("test", True, 1, 6)

terrain = Terrain(128, 0)
visionGrid = VisionGrid(128, terrain)
visionGrid.players.append(player)
visionGrid.CalculateVision()
def DrawBackground():
    pygame.draw.rect(win, (0, 0, 0), (0,0,500,500))
    size = 500/128
    for x in range(128):
        for y in range(128):
            color = (255,255,255)
            #playerPos = [(player.x + 5)/size, (player.y + 5)/size]
            #rectPos = [x +0.5, y+0.5]
            if visionGrid.values[x + y * 128] is not None:
                color = (0,255,0)
            if terrain.blocks[x + y * 128] == 1:
                color = (0,0,0)

            pygame.draw.rect(win, color, (size * x, size * y, size, size))



# oyun döngüsü
while run:

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            run = False


    DrawBackground()
    visionGrid.Update()
    player.Update()
    player.Render()

    # delta time hesaplaması
    t = pygame.time.get_ticks()
    EngineTime.deltaTime = (t - getTicksLastFrame) / 1000.0
    getTicksLastFrame = t

    pygame.display.update()

pygame.quit()
