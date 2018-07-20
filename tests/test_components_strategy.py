import pytest
from pytest import fixture

from ShallowOceanExpedition.components.strategy import DefaultStrategy


@fixture
def strategy():
    return DefaultStrategy('test')


def test_DefaultStrategy_decide_direction(strategy):
    board = {"round_number": 0}
    player = {
        "turn_number": 0,
        "changed_direction": False
    }
    changed = strategy.decide_direction(player, board, {})
    assert not changed

    board = {"round_number": 1}
    player = {
        "turn_number": 0,
        "changed_direction": False
    }
    changed = strategy.decide_direction(player, board, {})
    assert not changed

    board = {"round_number": 2}
    player = {
        "turn_number": 0,
        "changed_direction": False
    }
    changed = strategy.decide_direction(player, board, {})
    assert not changed

    board = {"round_number": 0}
    player = {
        "turn_number": 1,
        "changed_direction": False
    }
    changed = strategy.decide_direction(player, board, {})
    assert not changed

    board = {"round_number": 1}
    player = {
        "turn_number": 1,
        "changed_direction": False
    }
    changed = strategy.decide_direction(player, board, {})
    assert not changed

    board = {"round_number": 2}
    player = {
        "turn_number": 1,
        "changed_direction": False
    }
    changed = strategy.decide_direction(player, board, {})
    assert not changed

    board = {"round_number": 0}
    player = {
        "turn_number": 2,
        "changed_direction": False
    }
    changed = strategy.decide_direction(player, board, {})
    assert not changed

    board = {"round_number": 1}
    player = {
        "turn_number": 2,
        "changed_direction": False
    }
    changed = strategy.decide_direction(player, board, {})
    assert not changed

    board = {"round_number": 2}
    player = {
        "turn_number": 2,
        "changed_direction": False
    }
    changed = strategy.decide_direction(player, board, {})
    assert changed

    board = {"round_number": 3}
    player = {
        "turn_number": 2,
        "changed_direction": False
    }
    with pytest.raises()
    changed = strategy.decide_direction(player, board, {})
    assert changed