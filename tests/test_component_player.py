import pytest

from ShallowOceanExpedition.components.player import Player


class MockStrategy:
    player_name = 'player'


def test_Player_is_home():
    player = Player(MockStrategy())
    assert not player.is_home

    player.position = 1
    assert not player.is_home

    player.direction = -1
    assert not player.is_home

    player.position = 0
    assert player.is_home

    with pytest.raises(AttributeError):
        player.is_home = True


def test_Player_roll_counts():
    player = Player(MockStrategy())
    rolls = []
    for _ in range(100):
        rolls.append(player.roll())
    assert set(rolls) == {6, 5, 4, 3, 2}


def test_Player_roll_counts_with_tiles():
    player = Player(MockStrategy())
    player.tiles = [(1,), (1,), (1,)]
    rolls = []
    for _ in range(100):
        rolls.append(player.roll())
    assert set(rolls) == {3, 2, 1, 0}


def test_Player_roll_counts_backwards():
    player = Player(MockStrategy())
    player.direction = -1
    rolls = []
    for _ in range(100):
        rolls.append(player.roll())
    assert set(rolls) == {-6, -5, -4, -3, -2}


def test_Player_roll_counts_with_tiles_backwards():
    player = Player(MockStrategy())
    player.direction = -1
    player.tiles = [(1,), (1,), (1,)]
    rolls = []
    for _ in range(100):
        rolls.append(player.roll())
    assert set(rolls) == {-3, -2, -1, 0}


class MockTile:
    pass


def test_Player_collect_tile():
    player = Player(MockStrategy())
    assert player.tiles == []

    player.collect_tile(MockTile())
    assert len(player.tiles) == 1
