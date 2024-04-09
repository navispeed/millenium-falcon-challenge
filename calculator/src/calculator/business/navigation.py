import functools
import itertools
import json
from dataclasses import dataclass

from calculator.src.calculator.business.routes import Routes
from calculator.src.calculator.models.empire import Empire
from calculator.src.calculator.models.falcon import Falcon


@dataclass
@functools.total_ordering
class NavigationResult:
    path: list[str]
    duration: int
    odds: float

    def __lt__(self, other):
        return (self.odds, self.duration) < (other.odds, other.duration)


class Navigation:
    def __init__(self, empire_json: str, falcon: Falcon, route: Routes):
        self.empire: Empire = json.loads(empire_json)
        self.falcon = falcon
        self.route = route

    @staticmethod
    def bounty_formula(count: int):
        for k in range(1, count + 1):
            yield (9 ** (k - 1)) / (10 ** k)

    def find_route(self) -> list[NavigationResult]:
        routes = []
        self._find_route(self.falcon["departure"], self.empire["countdown"], self.falcon["autonomy"], [], routes)
        return list(sorted(map(self._path_to_result, routes), reverse=True))

    def _path_to_result(self, route: list[str]):
        odds, duration = self._compute_cost(route)
        return NavigationResult(route, duration, odds)

    def _find_route(self, current: str, remaining_days: int, current_fuel: int, path: list[str],
                    final_paths: list[list[str]]):
        path = path + [current]
        if remaining_days <= 0 or current_fuel < 0:
            return False
        planet_around = self.route.get_planet_around(current)
        planet_reachable = [idx for idx, weight in enumerate(planet_around) if
                            0 < weight <= current_fuel and weight <= remaining_days] + [
                               self.route.get_planet_id(current)]

        if self.route.get_planet_id(self.falcon["arrival"]) in planet_reachable:
            correct_path = path + [self.falcon["arrival"]]
            final_paths.append(correct_path)
            return True
        choice: int

        for choice in planet_reachable:
            # We don't want to come back to a previous planet
            if self.route.get_planet_name(choice) in path and choice != self.route.get_planet_id(current):
                continue
            self._find_route(self.route.get_planet_name(choice), remaining_days - planet_around[choice],
                             current_fuel - planet_around[choice] if self.route.get_planet_id(current) != choice else
                             self.falcon["autonomy"],
                             path, final_paths)
        return True  # TODO Keep it ?

    def _compute_cost(self, paths: list[str]) -> tuple[float, int]:
        bounty_per_planet = {planet: set(map(lambda v: v["day"], i)) for planet, i in
                             itertools.groupby(self.empire["bounty_hunters"], key=lambda x: x["planet"])}
        day = -1
        current = self.falcon["departure"]
        bounty_count = 0
        for planet in paths:
            day += self.route.get_trip_weight(current, planet)
            if planet in bounty_per_planet and day in bounty_per_planet[planet]:
                bounty_count += 1
            current = planet
        return 100 - 100 * sum(Navigation.bounty_formula(bounty_count)), day
