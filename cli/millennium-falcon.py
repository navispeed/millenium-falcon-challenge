import argparse
import json
import os
import sys

from calculator.business.navigation import Navigation
from calculator.business.routes import Routes
from calculator.models.empire import Empire
from calculator.models.falcon import Falcon

parser = argparse.ArgumentParser(
    prog='Millennium Falcon odds calculator',
    description='Given the spaceship status and empire data,'
                ' compute the odds based '
                'of all available paths.',
    epilog='May the force be with you')

parser.add_argument('falcon_file')
parser.add_argument('empire_file')

args = parser.parse_args()

if __name__ == '__main__':
    assert os.path.exists(args.falcon_file)
    assert os.path.exists(args.empire_file)
    with open(args.falcon_file, "r") as fp:
        falcon: Falcon = json.load(fp)
    with open(args.empire_file, "r") as fp:
        empire: Empire = json.load(fp)

    routes = Routes(falcon["routes_db"], args.falcon_file)

    try:
        path_found = Navigation(empire, falcon, routes).find_route()
    except RecursionError:
        print("Too many path were found, try to lower the countdown")
        sys.exit(-1)
    if len(path_found) == 0:
        print("No routes available")
        sys.exit(-1)
    print(path_found[0].odds)
