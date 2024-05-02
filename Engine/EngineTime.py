import pygame

class EngineTime:
    deltaTime = 0
    getTicksLastFrame = 0
    def Update(self):
        # delta time hesaplaması
        t = pygame.time.get_ticks()
        print("delta time : " + str(EngineTime.deltaTime))
        EngineTime.deltaTime = (t - self.getTicksLastFrame) / 1000.0
        self.getTicksLastFrame = t


