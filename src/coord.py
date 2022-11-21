import math

EARTH_RADIUS = 6371.008

class Coordinate:
    def __init__(self, coord: tuple[float, float]) -> None:
        self.latitude = coord[0]
        self.longitude = coord[1]

    def latitude(self) -> float:
        return self.latitude

    def longitude(self) -> float:
        return self.longitude

def distance(d1: Coordinate, d2: Coordinate) -> float:
    d1lat = math.radians(d1.latitude)
    d2lat = math.radians(d2.latitude)
    d1lon = math.radians(d1.longitude)
    d2lon = math.radians(d2.longitude)

    return math.acos(
        math.sin(d1lat) * math.sin(d2lat) +
        math.cos(d1lat) * math.cos(d2lat) *
        math.cos(d2lon - d1lon)
    ) * EARTH_RADIUS
