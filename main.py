import pygame
from Game.Player import Player
from Engine.EngineTime import EngineTime
import math

from Game.TerrainManager import VisionGrid,Part,Terrain

pygame.init()

gridSize = 256
realSize = 1000

win = pygame.display.set_mode((realSize, realSize))

pygame.display.set_caption("FogOfWar")

run = True
getTicksLastFrame = 0

players = []





terrain = Terrain(gridSize, 0)
visionGrid = VisionGrid(gridSize, realSize, terrain)


for i in range(100):

    player0 = Player("test", True, 10 * (i % 50), 10 * round(i / 2) )
    if i > 30:
        player0.radius = 2
    players.append(player0)
    visionGrid.players.append(player0)

visionGrid.CalculateVision()
def DrawBackground():
    pygame.draw.rect(win, (0, 0, 0), (0,0,realSize,realSize))
    size = realSize/gridSize
    for x in range(gridSize):
        for y in range(gridSize):
            color = (255,255,255)
            #playerPos = [(player.x + 5)/size, (player.y + 5)/size]
            #rectPos = [x +0.5, y+0.5]
            if visionGrid.values[x + y * gridSize] is not None:
                color = (0,255,0)
            if terrain.blocks[x + y * gridSize] == 1:
                color = (0,0,0)

            pygame.draw.rect(win, color, (size * x, size * y, size, size))


visionUpdateTime = 0
# oyun döngüsü
while run:

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            run = False


    DrawBackground()
    if pygame.time.get_ticks() > visionUpdateTime:
        visionGrid.Update()
        visionUpdateTime = pygame.time.get_ticks() + 500

    for player0 in players:
        player0.Update()
        player0.Render()



    # delta time hesaplaması
    t = pygame.time.get_ticks()
    print("delta time : " + str(EngineTime.deltaTime))
    EngineTime.deltaTime = (t - getTicksLastFrame) / 1000.0
    getTicksLastFrame = t

    pygame.display.update()

pygame.quit()
