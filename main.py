import pygame
from Game.Player import Player
from Engine.EngineTime import EngineTime

pygame.init()

win = pygame.display.set_mode((500, 500))

pygame.display.set_caption("FogOfWar")

x = 200
y = 200

width = 10
height = 10

vel = 200

run = True

getTicksLastFrame = 0

player = Player("test", True, 1, 6)

# oyun döngüsü
while run:

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            run = False

    pygame.draw.rect(win, (255, 255, 255), (0, 0, 500, 500))

    player.Update()
    player.Render()

    # delta time hesaplaması
    t = pygame.time.get_ticks()
    EngineTime.deltaTime = (t - getTicksLastFrame) / 1000.0
    getTicksLastFrame = t

    pygame.display.update()

pygame.quit()
