"""Visibility grid implementation for the fog-of-war example."""

from __future__ import annotations

from typing import List, Sequence, Tuple

from Game.BlockMap import BlockMap

GridPoint = Tuple[int, int]


class VisionGrid(object):
    """Keeps track of which tiles are currently visible to the players."""

    def __init__(self, gridSize: int, realSize: int, terrain: BlockMap):
        self.size = gridSize
        self.realSize = realSize
        self.values: List[int] = [0] * gridSize * gridSize
        self.terrain = terrain
        self.players = []

    def AddPlayer(self, player) -> None:
        self.players.append(player)

    def Clear(self) -> None:
        for i in range(len(self.values)):
            self.values[i] = 0

    def Update(self) -> None:
        self.Clear()
        self.CalculateVision()

    def CalculateVision(self) -> None:
        for player in self.players:
            player_pos = self._world_to_grid(player.x, player.y)
            circle_points = self.GetCirclePosition(player_pos, player.radius)
            for circle in circle_points:
                for point in self.GetOrthogonalLine(player_pos, circle):
                    if not self._is_inside_grid(point):
                        break
                    if self.terrain.blocks[point[0] + self.size * point[1]] == 1:
                        break
                    self.values[point[0] + self.size * point[1]] = 1

    def GetCirclePosition(self, center: GridPoint, radius: int) -> List[GridPoint]:
        """Return a list of points along the perimeter of a circle."""

        points: set[GridPoint] = set()
        current_radius = max(radius, 1)

        for _ in range(2):
            x = 0
            y = current_radius
            d = 3 - 2 * current_radius

            while y >= x:
                candidates = (
                    (center[0] + x, center[1] + y),
                    (center[0] - x, center[1] + y),
                    (center[0] + x, center[1] - y),
                    (center[0] - x, center[1] - y),
                    (center[0] + y, center[1] + x),
                    (center[0] - y, center[1] + x),
                    (center[0] + y, center[1] - x),
                    (center[0] - y, center[1] - x),
                )
                points.update(candidates)

                x += 1
                if d > 0:
                    y -= 1
                    d += 4 * (x - y) + 10
                else:
                    d += 4 * x + 6

            current_radius -= 1

        return list(points)

    def GetLinePositions(self, p0: GridPoint, p1: GridPoint, upperBounds: Sequence[int] | None = None) -> List[GridPoint]:
        """Return points for the line between ``p0`` and ``p1``.

        The method remains available for compatibility, but the fog of war logic
        relies on ``GetOrthogonalLine`` which better fits tile-based movement.
        """

        del upperBounds
        points: List[GridPoint] = []
        dx = p1[0] - p0[0]
        dy = p1[1] - p0[1]
        N = max(abs(dx), abs(dy))

        if N == 0:
            return [p0]

        xstep = dx / N
        ystep = dy / N
        x = float(p0[0])
        y = float(p0[1])

        for _ in range(N + 1):
            point = (round(x), round(y))
            if not points or points[-1] != point:
                points.append(point)
            x += xstep
            y += ystep

        return points

    def GetOrthogonalLine(self, p0: GridPoint, p1: GridPoint) -> List[GridPoint]:
        dx = p1[0] - p0[0]
        dy = p1[1] - p0[1]

        nx = abs(dx)
        ny = abs(dy)

        sign_x = 0 if dx == 0 else (1 if dx > 0 else -1)
        sign_y = 0 if dy == 0 else (1 if dy > 0 else -1)

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

        return [tuple(point) for point in points]

    def _world_to_grid(self, x: float, y: float) -> GridPoint:
        scale = self.size / self.realSize
        return (round(x * scale), round(y * scale))

    def _is_inside_grid(self, point: Sequence[int]) -> bool:
        return 0 <= point[0] < self.size and 0 <= point[1] < self.size
