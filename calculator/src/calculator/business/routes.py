import sqlite3
from collections import namedtuple
from copy import deepcopy

from calculator.utils.path_util import resolve_path

type Route = namedtuple("Route", ["src", "dst", "weigh"])
type Location = int | str


class Routes:
    def __init__(self, database_path: str, current_directory: str):
        with sqlite3.connect(resolve_path(database_path, current_directory)) as db:
            routes: list[Route] = db.cursor().execute("SELECT * FROM routes").fetchall()

        self.__planets: list[str] = list(set([src for src, _, _ in routes]) | set([dest for _, dest, _ in routes]))
        # noinspection PyTypeChecker
        self.__planet_to_index: dict[str, int] = dict([(routes, idx) for idx, routes in enumerate(self.__planets)])
        self.__matrix: list = []

        for _ in self.__planets:
            self.__matrix.append([0] * len(self.__planets))

        for planet in self.__planets:
            idx = self.__planet_to_index[planet]
            self.__matrix[idx][idx] = 1

        for src, dest, weigh in routes:
            assert weigh > 0
            self.__matrix[self.__planet_to_index[src]][self.__planet_to_index[dest]] = weigh
            self.__matrix[self.__planet_to_index[dest]][self.__planet_to_index[src]] = weigh

    @property
    def matrix(self):
        matrix = deepcopy(self.__matrix)
        for i in range(len(matrix)):
            matrix[i][i] = 0
        return matrix

    @property
    def planets(self):
        return self.__planets

    def get_planet_around(self, current_location: Location) -> list[int]:
        idx = self.get_planet_id(current_location)
        return self.__matrix[idx]

    def get_planet_id(self, location: Location) -> int:
        match location:
            case int():
                return location
            case str():
                return self.__planet_to_index[location]
            case _:
                raise TypeError("current_location must be an integer or an str")

    def get_planet_name(self, location: Location) -> str:
        match location:
            case int():
                return self.__planets[location]
            case str():
                return location
            case _:
                raise TypeError("current_location must be an integer or an str")

    def get_trip_weight(self, src: Location, dest: Location) -> int:
        return self.__matrix[self.get_planet_id(src)][self.get_planet_id(dest)]
