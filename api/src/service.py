import json
import os.path

from calculator.business.routes import Routes
from calculator.business.navigation import Navigation, NavigationResult
from calculator.models.empire import Empire
from calculator.models.falcon import Falcon


class Service:
    def __init__(self, falcon_json_location: str):
        assert os.path.exists(falcon_json_location)
        with open(falcon_json_location, "r") as fp:
            self.__falcon: Falcon = json.load(fp)
        print(self.__falcon["routes_db"], falcon_json_location)
        self.__routes = Routes(self.__falcon["routes_db"], falcon_json_location)

    def navigate(self, empire: Empire) -> NavigationResult:
        routes = Navigation(empire, self.__falcon, self.__routes).find_route()
        if len(routes) == 0:
            return NavigationResult([], -1, 0.)
        return routes[0]

    def route(self) -> tuple[list[list[int]], list[str]]:
        return self.__routes.matrix, self.__routes.planets
