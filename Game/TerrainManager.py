from random import random
import math


class Terrain(object):

    blocks = []
    def __init__(self, gridSize, gamePos):
        self.size = gridSize
        self.GenerateMap(gamePos)

    def GenerateMap(self, gamePos):
        size = self.size * self.size
        self.blocks = [0] * size

        for i in range(size):
            if(random() < 0.5):
                self.blocks[i] = 1

    def GetHeight(self, i):
        return self.blocks[i[0] + (self.size * i[1])]



class Part(object):
    def __init__(self):
        self.players = []


class VisionGrid(object):
    players = []
    def __init__(self, gridSize, terrain: Terrain):
        self.size = gridSize
        self.values = [None] * gridSize * gridSize
        self.terrain = terrain

    def AddPlayer(self, player):
        self.players.append(player)

    def Clear(self):
        self.values = [None] * self.size * self.size

    def Update(self):
        self.Clear()
        self.CalculateVision()

    def CalculateVision(self):
        for player in self.players:
            circlePoints = self.GetCirclePosition([round(player.x * 128/500), round(player.y *128/500)], player.radius, [])
            print("circle points")
            print(circlePoints)
            for circle in circlePoints:
                lines = self.GetLinePositions([round(player.x*128/500), round(player.y*128/500)], circle, [])
                print("lines : ")
                print(lines)
                for line in lines:
                    if self.terrain.blocks[line[0] + 128 * line[1]] == 1:
                        break
                    self.values[line[0] + 128 * line[1]] = 1


    def GetCirclePosition(self, center, radius, upperBounds):
        points = []

        i = 0
        while i <= 1:
            x = 0
            y = radius
            d = 3-2*radius

            while(y >= x):
                p = [center[0] + x, center[1] + y]
                if p not in points:
                  points.append(p)

                p = [center[0] - x, center[1] + y]
                if p not in points:
                  points.append(p)

                p = [center[0] + x, center[1] - y]
                if p not in points:
                  points.append(p)

                p = [center[0] - x, center[1] - y]
                if p not in points:
                  points.append(p)

                p = [center[0] + y, center[1] + x]
                if p not in points:
                  points.append(p)

                p = [center[0] - y, center[1] + x]
                if p not in points:
                  points.append(p)

                p = [center[0] + y, center[1] - x]
                if p not in points:
                  points.append(p)

                p = [center[0] - y, center[1] - x]
                if p not in points:
                    points.append(p)

                x+=1

                if(d>0):
                  y-=1
                  d = d +4 *(x-y)+10
                else:
                  d = d + 4 * x + 6

            i += 1
            radius -= 1

        return points

    def GetLinePositions(self, p0, p1, upperBounds):
        points = []
        dx = p1[0] - p0[0]
        dy = p1[1] - p0[1]
        N = max(abs(dx), abs(dy))

        divN = 0

        if N != 0:
            divN = 1/N

        xstep = dx * divN
        ystep = dy * divN
        x = p0[0]
        y = p0[1]

        step = 0
        while step <= N:

            point = [round(x), round(y)]
            if point not in points:
                points.append(point)

            step += 1
            x += xstep
            y += ystep

        return points

