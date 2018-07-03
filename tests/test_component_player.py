import pytest

from ShallowOceanExpedition.components.player import Player
from ShallowOceanExpedition.utils.exceptions import Cheating


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


def test_Player_roll_counts_backwards(player):
    player.direction = -1
    rolls = []
    for _ in range(100):
        rolls.append(player.roll())
    assert set(rolls) == {-6, -5, -4, -3, -2}


def test_Player_roll_counts_with_tiles_backwards(player):
    player.direction = -1
    player.tiles = [(1,), (1,), (1,)]
    rolls = []
    for _ in range(100):
        rolls.append(player.roll())
    assert set(rolls) == {-3, -2, -1, 0}


class MockTile:
    def __init__(self, level):
        self.level = (level,) if level else None


def test_Player_collect_tile(player):
    assert player.tiles == []

    player.collect_tile(MockTile(1))
    assert len(player.tiles) == 1

    with pytest.raises(ValueError):
        player.collect_tile(MockTile(None))


def test_Player_drop_tile(player):
    with pytest.raises(ValueError):
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


@pytest.mark.parametrize('tiles', [
    [],
    [MockTile(1)],
    [MockTile(1), MockTile(2)]
])
def test_Player_kill(player, tiles):
    assert player.tiles == []
    player.tiles = tiles
    assert not player.killed

    assert player.kill() == tiles
    assert player.killed
    assert player.tiles == tiles

    with pytest.raises(Cheating):
        player.kill()


def test_Player_end_round():
    pass

# todo: finish covering functions and add more weird cases where positions get weird
# todo: add some validation to properties eg position must be positive, direction restricted, n_turn positive, etc
