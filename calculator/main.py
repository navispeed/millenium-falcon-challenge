import json

from calculator.src.calculator.business import Navigation
from calculator.src.calculator.business import Routes
from calculator.src.calculator.models.empire import Empire
from calculator.src.calculator.models import Falcon

LOCATION = "./"

with open(f"{LOCATION}/empire.json", "r") as fp:
    empire: Empire = json.loads(fp.read())

with open(f"{LOCATION}/millennium-falcon.json", "r") as fp:
    falcon: Falcon = json.loads(fp.read())


# Routes("./examples/example3/universe.db")
with open(f"{LOCATION}/empire.json", "r") as fp:
    print(Navigation(fp.read(), falcon, Routes(falcon["routes_db"])).find_route())

#
#
# def find_route(current: str, dest: str, remaining_days: int, current_fuel: int, path: list[str],
#                final_paths: list[list[str]]):
#     path = path + [current]
#     if remaining_days <= 0 or current_fuel < 0:
#         return False
#     reach = matrix[planet_to_index[current]]
#     possible = [idx for idx, weight in enumerate(reach) if 0 < weight <= current_fuel and weight <= remaining_days] + [
#         planet_to_index[current]]
#     if planet_to_index[dest] in possible:
#         correct_path = path + [dest]
#         final_paths.append(correct_path)
#         print("Found it", path + [dest])
#         return True
#     choice: int
#     for choice in possible:
#         if planets[choice] in path and choice != planet_to_index[current]:
#             continue
#         find_route(planets[choice], dest, remaining_days - reach[choice],
#                    current_fuel - reach[choice] if planet_to_index[current] != choice else falcon[
#                        "autonomy"],
#                    path, final_paths)
#     return True  # TODO Keep it ?
#
#
# def bounty_formula(count: int):
#     for k in range(1, count + 1):
#         yield (9 ** (k - 1)) / (10 ** k)
#
#
# print(sum(bounty_formula(1)), sum(bounty_formula(2)), sum(bounty_formula(3)))
#
#
# def compute_cost(paths: list[str]) -> tuple[float, int]:
#     bounty_per_planet = {planet: set(map(lambda v: v["day"], i)) for planet, i in
#                          itertools.groupby(empire["bounty_hunters"], key=lambda x: x["planet"])}
#     day = -1
#     current = falcon["departure"]
#     bounty_count = 0
#     for planet in paths:
#         day += matrix[planet_to_index[current]][planet_to_index[planet]]
#         if planet in bounty_per_planet and day in bounty_per_planet[planet]:
#             bounty_count += 1
#         current = planet
#     return 100 - 100 * sum(bounty_formula(bounty_count)), day
#
#
# all_paths = []
# find_route(falcon["departure"], falcon["arrival"], empire["countdown"], falcon["autonomy"], [], all_paths)
# for path in all_paths:
#     print(path, compute_cost(path))
