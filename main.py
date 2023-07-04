import pygame
from Game.Player import Player
from Engine.EngineTime import EngineTime
from Game.BlockMap import BlockMap
from Game.VisionGrid import VisionGrid, GridPart
import time


pygame.init()

gridSize = 256
realSize = 1000

win = pygame.display.set_mode((realSize, realSize))
pygame.display.set_caption("FogOfWar")

run = True

players = []
blockMap = BlockMap(gridSize, 0)
visionGrid = VisionGrid(gridSize, realSize, blockMap)


for i in range(1):
    player0 = Player("test", True, 10 * (i % 50), 10 * round(i / 2))
    if i > 30:
        player0.radius = 2

    player0.BeginPlay()
    players.append(player0)
    visionGrid.players.append(player0)

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
            if blockMap.blocks[x + y * gridSize] == 1:
                color = (0,0,0)

            pygame.draw.rect(win, color, (size * x, size * y, size, size))


visionUpdateTime = 0

# oyun döngüsü
while run:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    DrawBackground()

    before = time.time()
    if pygame.time.get_ticks() > visionUpdateTime:
        visionGrid.Update()
        visionUpdateTime = pygame.time.get_ticks() + 100

    for player0 in players:
        player0.Update()
        player0.Render()

    EngineTime.Update(EngineTime)

    pygame.display.update()

pygame.quit()
