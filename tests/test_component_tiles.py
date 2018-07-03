import pytest

from ShallowOceanExpedition.components.tiles import Tile, TileStack


def test_Tile_value_fail():
    with pytest.raises(ValueError):
        Tile(0)

    with pytest.raises(ValueError):
        Tile(5)


def test_Tile_value_range():
    for _ in range(20):
        tile = Tile(1)
        assert tile.value in [0, 1, 2, 3, 4]

    for _ in range(20):
        tile = Tile(2)
        assert tile.value in [5, 6, 7, 8, 9]

    for _ in range(20):
        tile = Tile(3)
        assert tile.value in [10, 11, 12, 13, 14]

    for _ in range(20):
        tile = Tile(4)
        assert tile.value in [15, 16, 17, 18, 19]


def test_Tile_value_consistent():
    for level in [1, 2, 3, 4]:
        for _ in range(20):
            tile = Tile(level)
            assert tile._Tile__value is None
            value = tile.value
            assert tile._Tile__value is not None
            assert tile.value == value


def test_Tile_level():
    for level in [1, 2, 3, 4]:
        tile = Tile(level)
        assert isinstance(tile.level, tuple)
        assert tile.level == (level,)


def test_TileStack_empty_fail():
    with pytest.raises(ValueError):
        TileStack([])


class MockTile:
    def __init__(self, v):
        self.value = v
        self.level = (v,)


def test_TileStack_level_and_value():
    tilestack = TileStack([MockTile(1)])
    assert tilestack.level == (1,)
    assert tilestack._TileStack__value is None
    assert tilestack.value == 1
    assert tilestack._TileStack__value == 1

    tilestack = TileStack([MockTile(1), MockTile(2), MockTile(3)])
    assert tilestack.level == (1, 2, 3)
    assert tilestack._TileStack__value is None
    assert tilestack.value == 1 + 2 + 3
    assert tilestack._TileStack__value == 1 + 2 + 3


class MockMultiTile:
    def __init__(self, l):
        self.level = l
        self.value = sum(l)


def test_TileStack_multi():
    tilestack = TileStack([MockMultiTile((1, 2, 3))])
    assert tilestack.level == (1, 2, 3)
    assert tilestack._TileStack__value is None
    assert tilestack.value == 1 + 2 + 3
    assert tilestack._TileStack__value == 1 + 2 + 3

    tilestack = TileStack([MockMultiTile((1, 2, 3)), MockTile(1)])
    assert tilestack.level == (1, 2, 3, 1)
    assert tilestack._TileStack__value is None
    assert tilestack.value == 1 + 2 + 3 + 1
    assert tilestack._TileStack__value == 1 + 2 + 3 + 1

    tilestack = TileStack([MockMultiTile((1, 2, 3)), MockMultiTile((1, 2, 3))])
    assert tilestack.level == (1, 2, 3, 1, 2, 3)
    assert tilestack._TileStack__value is None
    assert tilestack.value == 1 + 2 + 3 + 1 + 2 + 3
    assert tilestack._TileStack__value == 1 + 2 + 3 + 1 + 2 + 3
