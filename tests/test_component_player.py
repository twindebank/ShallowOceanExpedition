from unittest.mock import patch

import pytest

from ShallowOceanExpedition.components.player import Player
from ShallowOceanExpedition.utils.exceptions import Cheating, RuleViolation


class MockStrategy:
    player_name = 'player'


@pytest.fixture()
def player():
    return Player(MockStrategy())


def test_Player_is_home(player):
    assert not player.is_home

    player.position = 1
    assert not player.is_home

    player.direction = -1
    assert not player.is_home

    player.position = 0
    assert player.is_home

    with pytest.raises(AttributeError):
        player.is_home = True


def test_Player_roll_counts(player):
    rolls = []
    for _ in range(100):
        rolls.append(player.roll())
    assert set(rolls) == {6, 5, 4, 3, 2}


def test_Player_roll_counts_with_tiles(player):
    player.tiles = [(1,), (1,), (1,)]
    rolls = []
    for _ in range(100):
        rolls.append(player.roll())
    assert set(rolls) == {3, 2, 1, 0}


class MockTile:
    def __init__(self, level):
        self.level = (level,) if level else None
        self.value = level


def test_Player_collect_tile(player):
    assert player.tiles == []

    player.collect_tile(MockTile(1))
    assert len(player.tiles) == 1

    with pytest.raises(RuleViolation):
        player.collect_tile(MockTile(None))


def test_Player_drop_tile(player):
    with pytest.raises(RuleViolation):
        player.drop_tile(None)

    tile = MockTile(1)
    player.tiles = [tile]
    with pytest.raises(ValueError):
        player.drop_tile((2,))

    assert player.drop_tile((1,)) == tile
    assert player.tiles == []

    tile1, tile11, tile2 = MockTile(1), MockTile(1), MockTile(2)
    player.tiles = [tile1, tile11, tile2]

    assert player.drop_tile((1,)) in [tile1, tile11]
    assert player.tiles in [[tile1, tile2], [tile11, tile2]]


def test_Player_count_tiles(player):
    assert player.tiles == []
    assert player.count_tiles() == 0
    player.collect_tile(MockTile(1))
    assert player.count_tiles() == 1


def test_Player_summarise_tiles(player):
    assert player.summarise_tiles() == {}

    player.tiles = [MockTile(1), MockTile(2)]
    assert player.summarise_tiles() == {(1,): 1, (2,): 1}

    player.tiles = [MockTile(1), MockTile(2), MockTile(1)]
    assert player.summarise_tiles() == {(1,): 2, (2,): 1}


def test_Player_change_direction(player):
    assert player.direction == 1
    player.change_direction()
    assert player.direction == -1
    with pytest.raises(Cheating):
        player.change_direction()


@patch('ShallowOceanExpedition.components.player.Player.clear_player')
@pytest.mark.parametrize('tiles', [
    [],
    [MockTile(1)],
    [MockTile(1), MockTile(2)]
])
def test_Player_kill(mock_clear_player, player, tiles):
    assert player.tiles == []
    player.tiles = tiles
    assert player.kill() == tiles
    assert mock_clear_player.called

    player.back_home = True
    with pytest.raises(Cheating):
        player.kill()


def test_Player_clear_player(player):
    bank = player.bank
    assert player.tiles == []
    assert player.position == 0
    assert player.direction == 1
    assert player.n_turn == 0
    assert not player.back_home
    assert player.deaths == []

    player.tiles = [MockTile(1), MockTile(2), MockTile(1)]
    player.position = 10
    player.direction = -1
    player.n_turn = 4
    player.back_home = True

    player.clear_player()

    assert player.back_home

    assert player.tiles == []
    assert player.position == 0
    assert player.direction == 1
    assert player.n_turn == 0
    assert player.deaths == [False]
    assert player.bank == bank

    player.tiles = [MockTile(1), MockTile(2), MockTile(1)]
    player.position = 10
    player.direction = -1
    player.n_turn = 4
    player.back_home = False

    player.clear_player()

    assert not player.back_home

    assert player.tiles == []
    assert player.position == 0
    assert player.direction == 1
    assert player.n_turn == 0
    assert player.deaths == [False, True]
    assert player.bank == bank


def test_Player_reached_home(player):
    assert player.bank == 0

    player.back_home = True
    with pytest.raises(Cheating):
        player.reached_home()

    player.tiles = [MockTile(1), MockTile(2), MockTile(1)]
    player.back_home = False

    player.reached_home()
    assert player.bank == 4
    assert player.back_home

    player.tiles = [MockTile(5), MockTile(2), MockTile(1)]
    player.back_home = False

    player.reached_home()
    assert player.bank == 12
    assert player.back_home


def test_Player_get_tile_values(player):
    player.tiles = [MockTile(1), MockTile(2), MockTile(1)]
    with pytest.raises(Cheating):
        player.get_tile_values()
    player.back_home = True
    assert player.get_tile_values() == 4

    player.tiles = []
    assert player.get_tile_values() == 0

# todo: finish covering functions and add more weird cases where positions get weird
# todo: add some validation to properties eg position must be positive, direction restricted, n_turn positive, etc
