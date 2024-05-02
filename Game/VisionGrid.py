from Game.BlockMap import BlockMap



class GridPart(object):
    def __init__(self):
        self.players = []


class VisionGrid(object):
    players = []

    def __init__(self, gridSize, realSize, terrain: BlockMap):
        self.size = gridSize
        self.realSize = realSize
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
            circlePoints = self.GetCirclePosition(
                [round(player.x * self.size / self.realSize), round(player.y * self.size / self.realSize)],
                player.radius, [])
            # print("circle points")
            # print(circlePoints)
            for circle in circlePoints:
                # lines = self.GetLinePositions([round(player.x*128/500), round(player.y*128/500)], circle, [])
                points = self.GetOrthogonalLine(
                    [round(player.x * self.size / self.realSize), round(player.y * self.size / self.realSize)], circle)
                # print("lines : ")
                # print(lines)
                for point in points:
                    if point[0] < 0 or point[0] > self.size or point[1] < 0 or point[1] >= self.size:
                        break
                    if self.terrain.blocks[point[0] + self.size * point[1]] == 1:
                        break
                    self.values[point[0] + self.size * point[1]] = 1

    def GetCirclePosition(self, center, radius, upperBounds):
        points = []

        i = 0
        while i <= 1:
            x = 0
            y = radius
            d = 3 - 2 * radius

            while y >= x:
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

                x += 1

                if (d > 0):
                    y -= 1
                    d = d + 4 * (x - y) + 10
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
            divN = 1 / N

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

    def GetOrthogonalLine(self, p0, p1):
        dx = p1[0] - p0[0]
        dy = p1[1] - p0[1]

        nx = abs(dx)
        ny = abs(dy)

        sign_x = 1 if dx > 0 else -1
        sign_y = 1 if dy > 0 else -1

        p = [p0[0], p0[1]]
        points = [[p[0], p[1]]]

        ix = 0
        iy = 0

        while ix < nx or iy < ny:
            decision = (1 + 2 * ix) * ny - (1 + 2 * iy) * nx

            if decision < 0:
                p[0] += sign_x
                ix += 1
            else:
                p[1] += sign_y
                iy += 1

            points.append([p[0], p[1]])

        return points
