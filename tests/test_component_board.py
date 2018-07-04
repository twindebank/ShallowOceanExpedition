import pytest

from ShallowOceanExpedition.components.board import Board


class MockStrategy:
    pass


def test_Board_init():
    with pytest.raises(ValueError):
        Board([])
    with pytest.raises(ValueError):
        Board([MockStrategy()])
