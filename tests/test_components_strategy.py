import pytest
from pytest import fixture

from ShallowOceanExpedition.components.strategy import DefaultStrategy
from ShallowOceanExpedition.utils.exceptions import RuleViolation


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
    with pytest.raises(RuleViolation):
        strategy.decide_direction(player, board, {})


def test_DefaultStrategy_tile_collect(strategy):
    board = {"round_number": 0}
    player = {
        "turn_number": 0,
        "changed_direction": False
    }
    drop = strategy.tile_collect(player, board, {})
    assert not drop

    board = {"round_number": 1}
    player = {
        "turn_number": 0,
        "changed_direction": False
    }
    drop = strategy.tile_collect(player, board, {})
    assert not drop

    board = {"round_number": 2}
    player = {
        "turn_number": 0,
        "changed_direction": False
    }
    drop = strategy.tile_collect(player, board, {})
    assert not drop

    board = {"round_number": 0}
    player = {
        "turn_number": 1,
        "changed_direction": False
    }
    drop = strategy.tile_collect(player, board, {})
    assert not drop

    board = {"round_number": 1}
    player = {
        "turn_number": 1,
        "changed_direction": False
    }
    drop = strategy.tile_collect(player, board, {})
    assert not drop

    board = {"round_number": 2}
    player = {
        "turn_number": 1,
        "changed_direction": False
    }
    drop = strategy.tile_collect(player, board, {})
    assert drop

    board = {"round_number": 0}
    player = {
        "turn_number": 2,
        "changed_direction": False
    }
    drop = strategy.tile_collect(player, board, {})
    assert drop

    board = {"round_number": 1}
    player = {
        "turn_number": 2,
        "changed_direction": False
    }
    drop = strategy.tile_collect(player, board, {})
    assert drop

    board = {"round_number": 2}
    player = {
        "turn_number": 2,
        "changed_direction": False
    }
    drop = strategy.tile_collect(player, board, {})
    assert drop

    board = {"round_number": 3}
    player = {
        "turn_number": 2,
        "changed_direction": False
    }
    with pytest.raises(RuleViolation):
        strategy.tile_collect(player, board, {})


def test_DefaultStrategy_tile_drop(strategy):
    # dont drop
    board = {"oxygen": 11}
    player = {
        "tiles": {},
        "position": 5
    }
    do, tile = strategy.tile_drop(player, board, {})
    assert not do
    assert not tile

    # do drop
    board = {"oxygen": 5}
    player = {
        "tiles": {(3,): 2, (2,): 1, (4,): 1},
        "position": 6
    }
    do, tile = strategy.tile_drop(player, board, {})
    assert do
    assert tile == (2,)

    # do drop with multi tiles
    board = {"oxygen": 5}
    player = {
        "tiles": {(3, 1, 3): 2, (2, 1): 1, (4, 3): 1},
        "position": 6
    }
    do, tile = strategy.tile_drop(player, board, {})
    assert do
    assert tile == (2, 1)
