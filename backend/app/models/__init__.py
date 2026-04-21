# from .airspace import Airspace
# from .designated_point import DesignatedPoint
from .airport_heliport import AirportHeliport
from .base import ElevatedPoint, Point
from .runway import Runway
from .runway_centreline_point import RunwayCentrelinePoint
from .runway_direction import RunwayDirection

All_Tables = [
    AirportHeliport,
    # Airspace,
    # DesignatedPoint,
    ElevatedPoint,
    Point,
    Runway,
    RunwayCentrelinePoint,
    RunwayDirection,
]
