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
        self.__routes = Routes(self.__falcon["routes_db"], falcon_json_location)

    def navigate(self, empire: Empire) -> list[NavigationResult]:
        return Navigation(empire, self.__falcon, self.__routes).find_route()
