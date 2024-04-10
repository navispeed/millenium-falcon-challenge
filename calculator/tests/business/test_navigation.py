import unittest.mock

import pytest

from calculator.business.navigation import Navigation, NavigationResult
from calculator.business.routes import Routes
from calculator.models.empire import Empire
from calculator.models.falcon import Falcon

type MockedRoutes = unittest.mock.Mock | Routes


@pytest.fixture
def mocked_routes() -> MockedRoutes:
    # 1 -> A
    # 2 -> B
    # 3 -> C

    # A (1) -> B (1) -> C

    mock: MockedRoutes = unittest.mock.Mock()

    items = ["A", "B", "C"]
    mapping = {"A": 0, "B": 1, "C": 2}
    matrix = {"A": [1, 1, 0], "B": [1, 1, 1], "C": [0, 1, 1]}
    set_matrix(items, matrix, mock)

    mock.get_planet_id.side_effect = lambda planet_name: mapping[planet_name]
    mock.get_planet_name.side_effect = lambda planet_id: items[planet_id]
    mock.get_trip_weight.return_value = 1
    return mock


def set_matrix(items: list[str], matrix: dict[str | int, list[int]], mock: MockedRoutes):
    for idx, k in enumerate(items):
        matrix[idx] = matrix[k]
    mock.get_planet_around.side_effect = lambda planet_id_or_name: matrix[planet_id_or_name]


def test_basic(mocked_routes):
    """
    Test a basic path (A -> B)
    :param mocked_routes:
    :return:
    """
    navigation = Navigation(Empire(countdown=10, bounty_hunters=[]),
                            Falcon(autonomy=3, departure="A", arrival="B", routes_db=""), route=mocked_routes)
    assert ([NavigationResult(path=['A', 'B'], duration=1, odds=1)] == navigation.find_route())


def test_basic_reverse(mocked_routes):
    """
    Test a basic path (B -> A)
    :param mocked_routes:
    :return:
    """
    navigation = Navigation(Empire(countdown=10, bounty_hunters=[]),
                            Falcon(autonomy=3, departure="B", arrival="A", routes_db=""), route=mocked_routes)
    assert ([NavigationResult(path=['B', 'A'], duration=1, odds=1)] == navigation.find_route())


def test_long_path(mocked_routes):
    """
    Test a basic path (A -> B -> C)
    :param mocked_routes:
    :return:
    """
    navigation = Navigation(Empire(countdown=10, bounty_hunters=[]),
                            Falcon(autonomy=3, departure="A", arrival="C", routes_db=""), route=mocked_routes)
    assert NavigationResult(path=['A', 'B', 'C'], duration=2, odds=1) == navigation.find_route()[0]


@pytest.mark.parametrize("arr, expected_result", [
    ([NavigationResult(path=[], duration=2, odds=1.), NavigationResult(path=[], duration=1, odds=1.)],  # input 1
     [NavigationResult(path=[], duration=1, odds=1.), NavigationResult(path=[], duration=2, odds=1.)]),  # res 1
    ([NavigationResult(path=[], duration=2, odds=1.), NavigationResult(path=[], duration=1, odds=0.5)],  # input 2
     [NavigationResult(path=[], duration=2, odds=1.), NavigationResult(path=[], duration=1, odds=0.5)])  # res 2
])
def test_sort(arr, expected_result):
    assert expected_result == list(sorted(arr, reverse=True))


@pytest.mark.parametrize("count, expected_result", [
    (0, 0),
    (1, 0.1),
    (2, 0.19),
    (3, 0.271)
])
def test_bounty_formula(count, expected_result):
    assert expected_result == sum(Navigation.bounty_formula(count))
